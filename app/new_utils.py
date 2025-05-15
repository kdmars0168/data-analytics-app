"""
AI‑powered health data analysis wrapper.

This module upgrades the static `generate_analysis_summary()` rule‑based
function with an LLM‑powered alternative.  It calls an OpenAI chat model to
produce a JSON analysis string covering steps, sleep, mood and
recommendations.  If the API key is missing or any runtime/usage error
occurs, it gracefully falls back to the legacy rule‑based logic so your
product continues to deliver value even when AI capacity is unavailable.

Usage
-----
>>> from ai_analysis import generate_analysis_summary
>>> data = {"steps":[8670,10321,9500], "sleep":[6.5,7.2,7.9], "mood":[7,8,6]}
>>> summary = generate_analysis_summary(data)

Environment
-----------
Set the environment variable `OPENAI_API_KEY` with a valid key.
Install the OpenAI Python client: `pip install openai>=1.0.0`.
"""
from __future__ import annotations

import json
import os
from typing import Any, Dict, List

try:
    import openai  # type: ignore
except ImportError:  # pragma: no cover
    openai = None  # type: ignore


# ---------------------------------------------------------------------------
# Prompt engineering
# ---------------------------------------------------------------------------
_SYSTEM_PROMPT = (
    "You are a data‑driven wellness coach.  Given average daily steps, "
    "sleep hours, and a 1‑10 mood score you must return a JSON object with "
    "four keys: steps_analysis, sleep_patterns, mood_correlation, "
    "recommendations.  Use short, encouraging sentences and plain language. "
    "Do NOT include any additional keys or markdown.  Return valid JSON only."
)

_USER_TEMPLATE = (
    "Steps: {avg_steps:.0f}\n"
    "Sleep: {avg_sleep:.1f}\n"
    "Mood: {avg_mood:.1f}"
)

# ---------------------------------------------------------------------------
# Legacy rule‑based fallback (imported from original file or re‑declared)
# ---------------------------------------------------------------------------


def _legacy_rule_based(data: Dict[str, List[float]]) -> Dict[str, str]:
    """Copy of the original rule‑engine to guarantee continuity."""
    steps = data.get("steps", [])
    sleep = data.get("sleep", [])
    mood = data.get("mood", [])

    if not steps or not sleep or not mood:
        return {
            "steps_analysis": "No data available.",
            "sleep_patterns": "No data available.",
            "mood_correlation": "No data available.",
            "recommendations": (
                "Please upload your health data to receive analysis and insights."
            ),
        }

    avg_steps = sum(steps) / len(steps)
    avg_sleep = sum(sleep) / len(sleep)
    avg_mood = sum(mood) / len(mood)

    analysis: Dict[str, str] = {
        "steps_analysis": "",
        "sleep_patterns": "",
        "mood_correlation": "",
        "recommendations": "",
    }

    # Steps
    if avg_steps >= 10000:
        analysis["steps_analysis"] = (
            f"Your average daily step count is {avg_steps:.0f} steps, which is outstanding! "
            "You're highly active and maintaining excellent cardiovascular health."
        )
    elif 8000 <= avg_steps < 10000:
        analysis["steps_analysis"] = (
            f"Your average daily step count is {avg_steps:.0f} steps, which is very good. "
            "You meet the general fitness recommendation."
        )
    elif 5000 <= avg_steps < 8000:
        analysis["steps_analysis"] = (
            f"Your average daily step count is {avg_steps:.0f} steps. "
            "You're moderately active but could benefit by walking a bit more."
        )
    else:
        analysis["steps_analysis"] = (
            f"Your average daily step count is {avg_steps:.0f} steps, which is low. "
            "Consider integrating more walking into your routine to improve endurance."
        )

    # Sleep
    if 7 <= avg_sleep <= 9:
        analysis["sleep_patterns"] = (
            f"You're averaging {avg_sleep:.1f} hours of sleep, which is optimal. "
            "Maintain good sleep hygiene."
        )
    elif 6 <= avg_sleep < 7:
        analysis["sleep_patterns"] = (
            f"You're averaging {avg_sleep:.1f} hours of sleep, slightly below optimal. "
            "Try adding an extra hour for better performance."
        )
    elif avg_sleep < 6:
        analysis["sleep_patterns"] = (
            f"You're averaging {avg_sleep:.1f} hours of sleep, critically low. "
            "Prioritise sleep immediately to prevent health effects."
        )
    else:
        analysis["sleep_patterns"] = (
            f"You're averaging {avg_sleep:.1f} hours of sleep, above recommended. "
            "Oversleeping can sometimes signal underlying fatigue."
        )

    # Mood correlation
    if avg_mood >= 8:
        analysis["mood_correlation"] = (
            "Your mood scores are excellent, suggesting great mental balance."
        )
    elif 6 <= avg_mood < 8:
        analysis["mood_correlation"] = (
            "Your mood scores are moderate—occasional stress may be present."
        )
    elif 4 <= avg_mood < 6:
        analysis["mood_correlation"] = (
            "Mood is somewhat low. Improving sleep and social engagement could help."
        )
    else:
        analysis["mood_correlation"] = (
            "Mood scores are poor—consider relaxation practices or professional help."
        )

    # Recommendations
    rec: List[str] = []
    if avg_steps < 8000:
        rec.append("Set a daily steps goal and add small walks throughout the day.")
    if avg_sleep < 7:
        rec.append(
            "Improve sleep hygiene: consistent schedule, limit screens before bed."
        )
    elif avg_sleep > 9:
        rec.append("Investigate causes of oversleeping and address possible fatigue.")
    if avg_mood < 7:
        rec.append(
            "Engage in enjoyable activities; exercise and mindfulness boost mood."
        )

    analysis["recommendations"] = (
        "You're doing extremely well! Keep up healthy habits." if not rec else " ".join(rec)
    )

    return analysis


# ---------------------------------------------------------------------------
# Unified public API
# ---------------------------------------------------------------------------

def generate_analysis_summary(
    data: Dict[str, List[float]],
    *,
    model: str = "gpt-4o-mini",
    temperature: float = 0.7,
) -> Dict[str, str]:
    """Return health analysis via LLM or fallback.

    Parameters
    ----------
    data : dict
        Expect keys "steps", "sleep", "mood" with numeric lists.
    model : str, optional
        OpenAI chat model ID (default ``gpt-4o-mini``).
    temperature : float, optional
        Sampling temperature for the LLM.

    Returns
    -------
    dict[str, str]
        Structured analysis with four narrative strings.
    """

    # Basic validation & averages
    steps, sleep, mood = (data.get(k, []) for k in ("steps", "sleep", "mood"))
    if not steps or not sleep or not mood or not openai or not os.getenv("OPENAI_API_KEY"):
        return _legacy_rule_based(data)

    avg_steps = sum(steps) / len(steps)
    avg_sleep = sum(sleep) / len(sleep)
    avg_mood = sum(mood) / len(mood)

    user_prompt = _USER_TEMPLATE.format(
        avg_steps=avg_steps, avg_sleep=avg_sleep, avg_mood=avg_mood
    )

    try:
        client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        response = client.chat.completions.create(
            model=model,
            temperature=temperature,
            messages=[
                {"role": "system", "content": _SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt},
            ],
            response_format={"type": "json_object"},
            timeout=15,  # seconds
        )

        raw_json = response.choices[0].message.content  # type: ignore[attr-defined]
        parsed: Dict[str, str] = json.loads(raw_json)

        # Sanity check for required keys
        expected = {"steps_analysis", "sleep_patterns", "mood_correlation", "recommendations"}
        if not expected.issubset(parsed):
            raise ValueError("LLM response missing keys")
        return parsed

    except Exception:  # pragma: no cover
        # Log the exception as needed (omitted here) and fallback
        return _legacy_rule_based(data)
