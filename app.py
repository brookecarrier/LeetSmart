import streamlit as st
from datetime import datetime
from scraper import get_solved_stats
from recommender import get_study_plan

def parse_plan_and_projection(plan_text, current_easy, current_medium, current_hard):
    daily_plan = []
    projected_easy = current_easy
    projected_medium = current_medium
    projected_hard = current_hard

    import re

    for line in plan_text.splitlines():
        line = line.strip()
        if line.lower().startswith("day"):
            daily_plan.append(line)
        elif line.lower().startswith("summary"):
            # Extract numbers from summary line
            numbers = list(map(int, re.findall(r'\d+', line)))
            if len(numbers) >= 3:
                # Add planned problems to current stats instead of replacing
                projected_easy = current_easy + numbers[0]
                projected_medium = current_medium + numbers[1]
                projected_hard = current_hard + numbers[2]

    # Fallback if no daily plan lines detected
    if not daily_plan:
        daily_plan = plan_text.splitlines()

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
                # Step 1: Fetch current stats
                stats = get_solved_stats(username)
                today = datetime.now().date()
                days_left = (interview_date - today).days

                if days_left <= 0:
                    st.error("Your interview date must be in the future!")
                else:
                    # Step 2: Display current stats
                    st.subheader("📊 Your Current LeetCode Stats")
                    st.markdown(f"""
                    - 🟢 Easy: **{stats['easy']}**
                    - 🟠 Medium: **{stats['medium']}**
                    - 🔴 Hard: **{stats['hard']}**
                    - ✅ Total Solved: **{stats['easy'] + stats['medium'] + stats['hard']}**
                    """)

                    # Step 3: Get raw AI plan
                    plan_raw, _ = get_study_plan(
                        stats["easy"], stats["medium"], stats["hard"], days_left
                    )

                    # Debug: Show raw AI output so you can inspect it
                    st.subheader("📅 Daily Study Plan")
                    st.text(plan_raw)

                    # Step 4: Parse AI output
                    plan, projected = parse_plan_and_projection(
                        plan_raw, stats["easy"], stats["medium"], stats["hard"]
                    )

                    # Step 5: Show cleaned study plan
                    #st.subheader("📅 AI-Generated Study Plan")
                    #st.markdown(plan)

                    # Step 6: Show projected stats
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
