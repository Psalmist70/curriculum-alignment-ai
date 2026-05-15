import pandas as pd
from skill_library import SKILL_LIBRARY


# ==========================================
# LOAD DATASET
# ==========================================
df = pd.read_csv(
    "../datasets/job_dataset_cleaned.csv",
    encoding="latin1"
)

print("Original Shape:", df.shape)


# ==========================================
# KEEP IMPORTANT COLUMNS
# ==========================================
required_columns = [
    "job_title",
    "job_description"
]

df = df[required_columns]


# ==========================================
# REMOVE NULLS
# ==========================================
df = df.dropna()


# ==========================================
# REMOVE DUPLICATES
# ==========================================
df = df.drop_duplicates()


# ==========================================
# SKILL EXTRACTION
# ==========================================
def extract_skills(text):

    text = str(text).lower()

    found = []

    for skill in SKILL_LIBRARY:

        if skill in text:
            found.append(skill)

    return found


df["skills"] = df["job_description"].apply(
    extract_skills
)


# ==========================================
# REMOVE JOBS WITH NO SKILLS
# ==========================================
df = df[
    df["skills"].apply(len) > 0
]


# ==========================================
# CREATE COMBINED TEXT
# ==========================================
df["combined_text"] = (
    df["job_title"]
    + " "
    + df["job_description"]
)


# ==========================================
# REDUCE SIZE
# ==========================================
df = df.sample(
    n=min(15000, len(df)),
    random_state=42
)


# ==========================================
# SAVE CLEANED DATA
# ==========================================
df.to_csv(
    "processed_jobs.csv",
    index=False
)

print("Final Shape:", df.shape)

print("processed_jobs.csv saved.")