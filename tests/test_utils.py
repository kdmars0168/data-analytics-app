import pytest
from app.utils import generate_analysis_summary

def test_empty_data_returns_no_data_messages():
    result = generate_analysis_summary({})
    assert result["steps_analysis"].startswith("⚠️ No data available")
    assert result["sleep_patterns"].startswith("⚠️ No data available")
    assert result["mood_correlation"].startswith("⚠️ No data available")
    assert result["recommendations"].startswith("📭 Please upload")

def test_excellent_activity_all_metrics():
    data = {
        "steps": [12500, 12000, 13000],
        "sleep": [8.0, 7.5, 9.0],
        "mood": [4.0, 4.0, 3.8]
    }
    result = generate_analysis_summary(data)
    assert "🚶‍♂️" in result["steps_analysis"]
    assert "🌙" in result["sleep_patterns"]
    assert "😄" in result["mood_correlation"]
    assert result["recommendations"].startswith("🌟 You're doing amazing")

def test_low_activity_and_mood():
    data = {
        "steps": [3000, 4000, 3500],
        "sleep": [5.5, 6.0, 6.2],
        "mood": [1.0, 1.5, 2.0]
    }
    result = generate_analysis_summary(data)
    assert "❗" in result["steps_analysis"] or "⚠️" in result["steps_analysis"]
    assert "⚠️" in result["sleep_patterns"] or "😕" in result["sleep_patterns"]
    assert "🚨" in result["mood_correlation"] or "😟" in result["mood_correlation"]
    assert "📌" in result["recommendations"]
    assert "• 👟" in result["recommendations"]
    assert "• 🛌" in result["recommendations"]
    assert "• 💡" in result["recommendations"]
