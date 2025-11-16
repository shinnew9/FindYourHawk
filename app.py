import streamlit as st
from modules.match_engine import recommend
from modules.mindhawk import mindhawk_checkin
from modules.recruiter_module import add_opportunity

st.set_page_config(page_title="FindYourHawk", layout="wide")

st.title("🦅 FindYourHawk")
st.subheader("AI-Powered Opportunity Navigator for Lehigh Students")

tab1, tab2, tab3 = st.tabs(["Opportunities", "Recruiter Portal", "MINDHAWK"])

# ----------------------
# 1) Opportunity Finder
# ----------------------
with tab1:
    st.write("### Discover opportunities tailored to you")

    major = st.selectbox("Your Major", ["Computer Science", "BioEngineering", "Business", "Psychology", "Other"])
    interests = st.text_input("Your Interests (comma separated)")
    goal = st.text_input("Career / Research Goal (optional)")

    if st.button("Find Opportunities"):
        results = recommend(major, interests, goal)
        st.write(results)

# ----------------------
# 2) Recruiter Portal
# ----------------------
with tab2:
    st.write("### Post a new opportunity")
    add_opportunity()

# ----------------------
# 3) MINDHAWK
# ----------------------
with tab3:
    st.write("### How are you feeling today?")
    mindhawk_checkin()
