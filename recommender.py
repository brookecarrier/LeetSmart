import os
from dotenv import load_dotenv
import requests

load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

def get_study_plan(current_easy, current_medium, current_hard, days_until):
    if not api_key:
        return "Error: API key not found.", {}

    prompt = f"""
You are a LeetCode coach helping a user prepare for their technical interview in {days_until} days.
They have currently solved:
- {current_easy} Easy
- {current_medium} Medium
- {current_hard} Hard

Create a day-by-day study plan with daily tasks formatted as:

Day 1: Solve X Easy, Y Medium, Z Hard problems
Day 2: Solve ...

At the end, provide a summary line exactly in this format:
Summary: Total Easy: A, Total Medium: B, Total Hard: C

Do NOT include the user's current totals in the summary — only the problems they will add during the plan.

Then, provide a motivating sentence or two to keep the user focused!


Keep your response concise.
"""

    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {"role": "system", "content": "You are a helpful LeetCode coach."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        content = response.json()['choices'][0]['message']['content']
        return content, {}
    else:
        return f"Error: {response.status_code} – {response.text}", {}
