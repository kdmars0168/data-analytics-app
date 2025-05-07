def generate_analysis_summary(data):
    steps = data.get('steps', [])
    sleep = data.get('sleep', [])
    mood = data.get('mood', [])
    
    if not steps or not sleep or not mood:
        return {
            "steps_analysis": "No data available.",
            "sleep_patterns": "No data available.",
            "mood_correlation": "No data available.",
            "recommendations": "Please upload your health data to receive analysis and insights."
        }

    # Safely handle empty lists
    avg_steps = sum(steps) / len(steps) if steps else 0
    avg_sleep = sum(sleep) / len(sleep) if sleep else 0
    avg_mood = sum(mood) / len(mood) if mood else 0

    analysis = {
        "steps_analysis": "",
        "sleep_patterns": "",
        "mood_correlation": "",
        "recommendations": "",
    }

    # Steps Analysis
    if avg_steps >= 10000:
        analysis['steps_analysis'] = (
            f"Your average daily step count is {avg_steps:.0f} steps, which is outstanding! "
            "You're highly active and maintaining excellent cardiovascular health."
        )
    elif 8000 <= avg_steps < 10000:
        analysis['steps_analysis'] = (
            f"Your average daily step count is {avg_steps:.0f} steps, which is very good. "
            "You meet the general fitness recommendation."
        )
    elif 5000 <= avg_steps < 8000:
        analysis['steps_analysis'] = (
            f"Your average daily step count is {avg_steps:.0f} steps. "
            "You're moderately active but could greatly benefit by walking a bit more."
        )
    else:
        analysis['steps_analysis'] = (
            f"Your average daily step count is {avg_steps:.0f} steps, which is low. "
            "Consider integrating more walking into your daily routine to improve heart health and endurance."
        )

    # Sleep Patterns
    if 7 <= avg_sleep <= 9:
        analysis['sleep_patterns'] = (
            f"You're averaging {avg_sleep:.1f} hours of sleep per night, which is optimal. "
            "Keep maintaining good sleep hygiene."
        )
    elif 6 <= avg_sleep < 7:
        analysis['sleep_patterns'] = (
            f"You're averaging {avg_sleep:.1f} hours of sleep per night, which is slightly below optimal. "
            "Try to add an extra hour if possible for better cognitive performance."
        )
    elif avg_sleep < 6:
        analysis['sleep_patterns'] = (
            f"You're averaging {avg_sleep:.1f} hours of sleep per night, which is critically low. "
            "Prioritize sleep immediately to prevent negative health effects."
        )
    else:  # avg_sleep > 9
        analysis['sleep_patterns'] = (
            f"You're averaging {avg_sleep:.1f} hours of sleep per night, which is above the recommended amount. "
            "While good rest is important, oversleeping could sometimes signal underlying fatigue."
        )

    # Mood Correlation
    if avg_mood >= 8:
        analysis['mood_correlation'] = (
            "Your mood scores are excellent, suggesting great mental and emotional balance."
        )
    elif 6 <= avg_mood < 8:
        analysis['mood_correlation'] = (
            "Your mood scores are moderate. You might be experiencing occasional stress or tiredness."
        )
    elif 4 <= avg_mood < 6:
        analysis['mood_correlation'] = (
            "Your mood scores are somewhat low. Improving your sleep, physical activity, and social engagement could help."
        )
    else:
        analysis['mood_correlation'] = (
            "Your mood scores are poor. It's crucial to address emotional wellbeing — consider relaxation practices, support groups, or professional help."
        )

    # Recommendations
    recommendations = []

    if avg_steps < 8000:
        recommendations.append("Try setting a daily steps goal and take small walks throughout the day.")
    if avg_sleep < 7:
        recommendations.append("Improve sleep hygiene: maintain a regular sleep schedule, limit screens before bed, and relax before sleeping.")
    elif avg_sleep > 9:
        recommendations.append("Monitor why you might be oversleeping; address possible fatigue causes.")
    if avg_mood < 7:
        recommendations.append("Engage in activities you enjoy. Physical exercise, socializing, and mindful practices can boost mood.")

    if not recommendations:
        analysis['recommendations'] = "You're doing extremely well! Keep up your current healthy habits."
    else:
        analysis['recommendations'] = " ".join(recommendations)

    return analysis
