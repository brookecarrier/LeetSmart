import streamlit as st
from datetime import datetime
from scraper import get_solved_stats
from recommender import get_study_plan
import re

def parse_plan_and_projection(plan_text, current_easy, current_medium, current_hard):
    daily_plan = []
    projected_easy = current_easy
    projected_medium = current_medium
    projected_hard = current_hard

    total_easy = 0
    total_medium = 0
    total_hard = 0

    for line in plan_text.splitlines():
        line = line.strip()

        if line.lower().startswith("day"):
            daily_plan.append(line)

        elif "total easy" in line.lower() and "total medium" in line.lower() and "total hard" in line.lower():
            # Example: "Summary: Total Easy: 10, Total Medium: 20, Total Hard: 19"
            numbers = list(map(int, re.findall(r'\d+', line)))
            if len(numbers) >= 3:
                total_easy, total_medium, total_hard = numbers[:3]

    # Fallback if no daily plan lines detected
    if not daily_plan:
        daily_plan = plan_text.splitlines()

    # Add totals from plan to the user's current stats
    projected_easy = current_easy + total_easy
    projected_medium = current_medium + total_medium
    projected_hard = current_hard + total_hard

    projected = {
        "easy": projected_easy,
        "medium": projected_medium,
        "hard": projected_hard
    }

    return "\n".join(daily_plan), projected


st.set_page_config(page_title="LeetSmart Interview Prep")

st.title("LeetSmart")
st.header("Technical Interview Prep Planner")

username = st.text_input("Enter your LeetCode username")
interview_date = st.date_input("Enter your next technical interview date")

if username and interview_date:
    if st.button("Generate Study Plan"):
        with st.spinner("Fetching your stats and generating plan..."):
            try:
                # Fetch current stats
                stats = get_solved_stats(username)
                today = datetime.now().date()
                days_left = (interview_date - today).days

                if days_left <= 0:
                    st.error("Your interview date must be in the future!")
                else:
                    # Display current stats
                    st.subheader("📊 Your Current LeetCode Stats")
                    st.markdown(f"""
                    - 🟢 Easy: **{stats['easy']}**
                    - 🟠 Medium: **{stats['medium']}**
                    - 🔴 Hard: **{stats['hard']}**
                    - ✅ Total Solved: **{stats['easy'] + stats['medium'] + stats['hard']}**
                    """)

                    # Get AI plan
                    plan_raw, _ = get_study_plan(
                        stats["easy"], stats["medium"], stats["hard"], days_left
                    )

                    # Display AI plan
                    st.subheader("📅 Daily Study Plan")
                    st.text(plan_raw)

                    # Parse AI plan
                    plan, projected = parse_plan_and_projection(
                        plan_raw, stats["easy"], stats["medium"], stats["hard"]
                    )

                    # Display projected stats
                    st.subheader("🔮 Projected Stats After Plan")
                    st.markdown(f"""
                    - 🟢 Easy: **{projected['easy']}** (was {stats['easy']})
                    - 🟠 Medium: **{projected['medium']}** (was {stats['medium']})
                    - 🔴 Hard: **{projected['hard']}** (was {stats['hard']})
                    - ✅ Total Solved: **{projected['easy'] + projected['medium'] + projected['hard']}**
                    """)

                    st.caption("Powered by Groq AI.")

            except Exception as e:
                st.error(f"Error: {e}")
