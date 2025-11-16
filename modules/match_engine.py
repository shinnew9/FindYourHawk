import pandas as pd
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI()

def recommend(major, interests, goal):
    df = pd.read_csv("data/opportunities.csv")

    # 1) 전공/레벨 기반 간단 필터 (너무 빡세진 않게)
    mask_major = df["target_majors"].fillna("").str.contains(major, case=False)
    filtered = df[mask_major] if mask_major.any() else df

    # 나중에 학부/대학원 구분하고 싶으면 level도 같이 필터링 가능:
    # if level in ["Undergraduate", "Graduate"]:
    #     mask_level = filtered["level"].fillna("").str.contains(level, case=False)
    #     if mask_level.any():
    #         filtered = filtered[mask_level]

    opportunities = filtered.to_dict(orient="records")

    prompt = f"""
You are matching internal Lehigh University opportunities to a student.

Student profile:
- Major: {major}
- Interests: {interests}
- Goal: {goal}

Here is a list of opportunities (JSON-like records):
{opportunities}

Choose the 3 best-matching opportunities and respond in **markdown**.
For each opportunity, show exactly this structure:

1. **Title** – (Type, Department)
   - Professor / Contact: Prof. NAME or ROLE
   - Why it's a fit: (2 short bullet points)
   - Website: URL
   - Skills: comma-separated list

If something is missing (e.g., professor or website), just write "N/A" but still show the field.
    """

    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
    )

    return resp.choices[0].message.content
