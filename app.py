import re
import streamlit as st
from dotenv import load_dotenv

from modules.match_engine import recommend
from modules.recruiter_module import add_opportunity
from modules.mindhawk import mindhawk_checkin

# Load environment variables (e.g., OPENAI_API_KEY from .env)
load_dotenv()

# Basic page config
st.set_page_config(
    page_title="FindYourHawk",
    layout="wide",
)


# ------------------------------------------------
# Global CSS for button styling (Lehigh Gold theme)
# ------------------------------------------------
st.markdown(
    """
    <style>
    .stButton>button {
        background-color: #C9A66B;      /* Lehigh Gold */
        color: #FFFFFF;
        border-radius: 6px;
        padding: 0.4rem 1.2rem;
        border: none;
        font-weight: 600;
    }
    .stButton>button:hover {
        background-color: #B08C57;      /* Darker gold on hover */
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# -----------------------------
# Mock Lehigh SSO + Profile
# -----------------------------

if "user_profile" not in st.session_state:
    st.title("🦅 FindYourHawk")
    st.subheader("Lehigh Single Sign-On (demo)")

    lehigh_email = st.text_input("Lehigh Email (e.g., abc123@lehigh.edu)")
    role = st.selectbox("I am a...", ["Student", "Staff / Faculty"])

    level = None
    major = None
    if role == "Student":
        level = st.selectbox("Student Type", ["Undergraduate", "Graduate"])
        major = st.selectbox(
            "Major",
            [
                "Computer Science",
                "Bioengineering",
                "Mechanical Engineering",
                "Business",
                "Psychology",
                "Other",
            ],
        )

    if st.button("Sign in (mock Duo verified)"):
        email = lehigh_email.strip()

        # Simple Lehigh email validation
        pattern = r"^[A-Za-z0-9._%+-]+@lehigh\.edu$"
        if not re.match(pattern, email):
            st.error(
                "Please enter a valid Lehigh email address "
                "(for example, abc123@lehigh.edu)."
            )
        else:
            st.session_state.user_profile = {
                "email": email,
                "role": role,
                "level": level,
                "major": major,
            }
            st.success(f"Signed in as {email}")
            st.rerun()

    # Do not render the rest of the app until the user is “signed in”
    st.stop()

# After this point, we know the user is “logged in”
profile = st.session_state.user_profile

# -----------------------------
# Sidebar navigation
# -----------------------------

with st.sidebar:
    # Logo at the top
    st.image("assets/FindYourHawk.png", width=140)

    st.markdown("### ☰ Menu")

    # Main opportunities & recruiting section
    st.markdown("**Opportunities & Recruiting**")
    nav_main = st.radio(
        "Navigate-main",
        ["Opportunities", "Recruiter Portal"],
        index=0,
        label_visibility="collapsed",
        key="nav_main_radio",  # unique key
    )

    st.markdown("---")

    # Separate section for well-being tools
    st.markdown("**Well-being tools**")
    use_mindhawk = st.checkbox(
        "Open MINDHAWK",
        value=False,              # default = unchecked
        key="mindhawk_checkbox",  # unique key
    )

# Decide which page is active
if use_mindhawk:
    page = "MINDHAWK"
else:
    page = nav_main


# -----------------------------
# Main content area
# -----------------------------

st.title("🦅 FindYourHawk")
st.caption("AI-Powered Opportunity Navigator for Lehigh Students")

# Optional small profile line under the header
st.write(
    f"Signed in as **{profile['email']}**"
    + (
        f" · {profile.get('level', '')} · {profile.get('major', '')}"
        if profile.get("level") and profile.get("major")
        else ""
    )
)

if page == "Opportunities":
    st.subheader("Discover opportunities tailored to you")

    major = st.selectbox(
        "Your Major",
        [
            "Computer Science",
            "Bioengineering",
            "Mechanical Engineering",
            "Business",
            "Psychology",
            "Other",
        ],
        index=0 if not profile.get("major") else
        [
            "Computer Science",
            "Bioengineering",
            "Mechanical Engineering",
            "Business",
            "Psychology",
            "Other",
        ].index(profile["major"])
        if profile["major"] in [
            "Computer Science",
            "Bioengineering",
            "Mechanical Engineering",
            "Business",
            "Psychology",
            "Other",
        ]
        else 0,
    )

    interests = st.text_input("Your Interests (comma separated)")
    goal = st.text_input("Career / Research Goal (optional)")

    if st.button("Find Opportunities"):
        results = recommend(major, interests, goal)
        # Model already returns markdown-formatted text
        st.markdown(results)

elif page == "Recruiter Portal":
    st.subheader("Post a new opportunity")
    add_opportunity()

elif page == "MINDHAWK":
    st.subheader("How are you feeling today?")
    mindhawk_checkin()
