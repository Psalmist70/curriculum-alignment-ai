import os
import numpy as np
import pandas as pd
import faiss


# ==================================================
# BASE PATH (DJANGO SAFE)
# ==================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")

JOB_PATH = os.path.join(DATA_DIR, "processed_jobs.csv")
FAISS_PATH = os.path.join(DATA_DIR, "faiss_index.index")


# ==================================================
# LOAD FAISS + JOB DATA ONCE (IMPORTANT)
# ==================================================
faiss_index = faiss.read_index(FAISS_PATH)
job_df = pd.read_csv(JOB_PATH, encoding="latin1")


# ==================================================
# SKILL LIBRARY
# ==================================================
SKILL_LIBRARY = [
    "python", "java", "c++", "javascript", "php",
    "sql", "machine learning", "data analysis",
    "django", "flask", "api", "git",
    "linux", "docker", "aws",
    "html", "css", "react",
    "communication", "teamwork", "problem solving"
]


# ==================================================
# SKILL EXTRACTION (FAST RULE-BASED)
# ==================================================
def extract_skills(text):
    text = str(text).lower()
    return [skill for skill in SKILL_LIBRARY if skill in text]


# ==================================================
# FAISS SEARCH FUNCTION
# ==================================================
def search_jobs(embeddings, top_k=1):

    embeddings = np.array(embeddings).astype("float32")

    distances, indices = faiss_index.search(
        embeddings,
        top_k
    )

    return distances, indices


# ==================================================
# GET JOB DETAILS FROM INDEX
# ==================================================
def get_job_by_index(idx):
    return job_df.iloc[idx]


# ==================================================
# MAIN PIPELINE (USED BY DJANGO VIEW)
# ==================================================
def run_alignment_analysis(df):

    results = []

    # --------------------------------------------------
    # COMBINE TEXT FOR EMBEDDING
    # --------------------------------------------------
    df["combined_text"] = (
        df["course_title"].astype(str)
        + " "
        + df["course_description"].astype(str)
    )

    # --------------------------------------------------
    # LOAD MODEL ON DEMAND (PREVENT RENDER CRASH)
    # --------------------------------------------------
    from sentence_transformers import SentenceTransformer
    model = SentenceTransformer("all-MiniLM-L6-v2")

    # --------------------------------------------------
    # CREATE EMBEDDINGS
    # --------------------------------------------------
    curriculum_embeddings = model.encode(
        df["combined_text"].tolist(),
        show_progress_bar=False
    )

    curriculum_embeddings = np.array(curriculum_embeddings).astype("float32")

    # --------------------------------------------------
    # FAISS SEARCH
    # --------------------------------------------------
    distances, indices = search_jobs(curriculum_embeddings, top_k=1)

    # --------------------------------------------------
    # PROCESS RESULTS
    # --------------------------------------------------
    for i, row in df.iterrows():

        job_idx = int(indices[i][0])
        score = float(1 / (1 + distances[i][0]))

        job = get_job_by_index(job_idx)

        curriculum_skills = list(set(extract_skills(row["combined_text"])))

        job_skills = job["skills"]

        # handle string or list safely
        if isinstance(job_skills, str):
            job_skills = job_skills.replace("[", "").replace("]", "")
            job_skills = job_skills.replace("'", "")
            job_skills = [s.strip() for s in job_skills.split(",") if s.strip()]

        missing_skills = list(set(job_skills) - set(curriculum_skills))
        missing_skills = [s.strip() for s in missing_skills if s]

        recommendations = [f"Learn {skill}" for skill in missing_skills]

        results.append({
            "course_name": row["course_title"],
            "matched_job": job["job_title"],
            "similarity_score": round(score, 4),
            "extracted_skills": curriculum_skills,
            "missing_skills": missing_skills,
            "recommendations": recommendations
        })

    return results