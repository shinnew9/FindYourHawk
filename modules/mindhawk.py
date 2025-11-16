from openai import OpenAI
import streamlit as st

client = OpenAI()

def mindhawk_checkin():
    mood = st.text_area("Describe how you're feeling today:")

    if st.button("Analyze My Mood"):
        prompt = f"""
        Provide a short, safe well-being reflection for a student.
        Student message: {mood}

        Include:
        - Brief emotional summary
        - 2 simple coping suggestions
        - Encouraging statement
        - No medical or diagnostic language
        """

        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )
        st.write(resp.choices[0].message.content)
