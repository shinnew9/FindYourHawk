import streamlit as st
import pandas as pd
from .constants import DATA_DIR, OPPORTUNITIES_CSV

def add_opportunity():
    DATA_DIR.mkdir(exist_ok=True)

    title = st.text_input("Position Title")
    desc = st.text_area("Description")
    skills = st.text_input("Required Skills")
    link = st.text_input("Application Link")

    if st.button("Submit Opportunity"):
        new_entry = pd.DataFrame([{
            "title": title,
            "description": desc,
            "skills": skills,
            "link": link,
        }])

        if OPPORTUNITIES_CSV.exists():
            df = pd.read_csv(OPPORTUNITIES_CSV)
            df = pd.concat([df, new_entry], ignore_index=True)
        else:
            df = new_entry

        df.to_csv(OPPORTUNITIES_CSV, index=False)
        st.success("Opportunity posted!")
