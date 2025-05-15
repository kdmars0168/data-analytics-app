def generate_analysis_summary(data):
    steps = data.get('steps', [])
    sleep = data.get('sleep', [])
    mood = data.get('mood', [])

    if not steps or not sleep or not mood:
        return {
            "steps_analysis": "⚠️ No data available for the past 7 days.",
            "sleep_patterns": "⚠️ No data available for the past 7 days.",
            "mood_correlation": "⚠️ No data available for the past 7 days.",
            "recommendations": "📭 Please upload your health data to receive personalized analysis and recommendations."
        }

    # Calculate averages
    avg_steps = sum(steps) / len(steps) if steps else 0
    avg_sleep = sum(sleep) / len(sleep) if sleep else 0
    avg_mood = sum(mood) / len(mood) if mood else 0

    analysis = {}

    # 🟣 STEPS ANALYSIS
    if avg_steps >= 12000:
        analysis['steps_analysis'] = (
            f"🚶‍♂️ Over the past 7 days, you averaged **{avg_steps:.0f} steps/day** — exceptional! "
            "You're going above and beyond for your cardiovascular health. Keep crushing it! 💪"
        )
    elif 10000 <= avg_steps < 12000:
        analysis['steps_analysis'] = (
            f"🥇 You averaged **{avg_steps:.0f} steps/day** — excellent pace! "
            "You're meeting and exceeding recommended levels of daily movement. 👣"
        )
    elif 7500 <= avg_steps < 10000:
        analysis['steps_analysis'] = (
            f"👍 Your weekly average is **{avg_steps:.0f} steps/day** — solid work. "
            "You're hitting the general fitness goal. A little more can push you to elite levels. 🌟"
        )
    elif 5000 <= avg_steps < 7500:
        analysis['steps_analysis'] = (
            f"⚠️ You averaged **{avg_steps:.0f} steps/day** — not bad, but below the recommended 7,500. "
            "Try adding a short walk before or after work. 🚶"
        )
    else:
        analysis['steps_analysis'] = (
            f"❗ You averaged only **{avg_steps:.0f} steps/day** this week. "
            "Low activity levels may affect heart health, energy, and mood. Consider walking breaks and reducing sitting time. 🛋️➡️🚶"
        )

    # 🟡 SLEEP ANALYSIS
    if 7 <= avg_sleep <= 9:
        analysis['sleep_patterns'] = (
            f"🌙 You averaged **{avg_sleep:.1f} hours/night** — perfect! "
            "You're getting restorative sleep in the ideal range. 😴"
        )
    elif 6 <= avg_sleep < 7:
        analysis['sleep_patterns'] = (
            f"😕 You averaged **{avg_sleep:.1f} hours/night** — slightly under target. "
            "Try winding down earlier or reducing late-night screen time. 📴"
        )
    elif avg_sleep < 6:
        analysis['sleep_patterns'] = (
            f"⚠️ Only **{avg_sleep:.1f} hours/night** on average — too little sleep! "
            "Insufficient rest can harm memory, mood, and metabolism. Prioritize quality sleep. 🛏️"
        )
    elif avg_sleep > 9:
        analysis['sleep_patterns'] = (
            f"🛌 You slept **{avg_sleep:.1f} hours/night** — over the recommended range. "
            "Excess sleep might reflect fatigue, stress, or irregular habits. Consider tracking how you feel. 📝"
        )
    else:
        analysis['sleep_patterns'] = (
            f"❓ Sleep data seems inconsistent (avg: {avg_sleep:.1f} hours). Double-check your logs. 🕵️"
        )

    # 🔵 MOOD ANALYSIS (0–4 scale)
    if avg_mood >= 3.5:
        analysis['mood_correlation'] = (
            "😄 Your mood this week was excellent — steady and upbeat. "
            "You're in a great headspace! Keep doing what works. 🌈"
        )
    elif 2.5 <= avg_mood < 3.5:
        analysis['mood_correlation'] = (
            "🙂 Moderate mood scores. You might be juggling some stress or low energy. "
            "Make time for self-care, breaks, and people who recharge you. ☕🎧"
        )
    elif 1.5 <= avg_mood < 2.5:
        analysis['mood_correlation'] = (
            "😟 Your mood is leaning low. Physical activity, sunlight, and social support can help rebalance things. 🧘‍♂️🌤️👫"
        )
    else:
        analysis['mood_correlation'] = (
            "🚨 Very low mood scores this week. Please don’t ignore emotional well-being — reach out to a friend, journal your thoughts, or seek professional help if needed. 💬🧠"
        )

    # ✅ RECOMMENDATIONS
    tips = []

    # Steps
    if avg_steps < 7500:
        tips.append("👟 **Boost daily movement:** Try 10–15 min walks during lunch or after dinner.")

    # Sleep
    if avg_sleep < 7:
        tips.append("🛌 **Improve sleep hygiene:** Maintain a consistent bedtime and reduce screen time before sleep.")
    elif avg_sleep > 9:
        tips.append("🔍 **Reflect on oversleeping:** Track if you're feeling rested or fatigued despite sleeping long.")

    # Mood
    if avg_mood < 2.5:
        tips.append("💡 **Lift your mood:** Spend time outdoors, listen to music, or talk to someone you trust.")

    # If no tips needed
    if not tips:
        analysis['recommendations'] = (
            "🌟 You're doing amazing across all areas — keep thriving and enjoying the ride! 💖"
        )
    else:
        analysis['recommendations'] = "📌 Here are a few personalized tips for the coming week:\n\n• " + "\n• ".join(tips)

    return analysis
