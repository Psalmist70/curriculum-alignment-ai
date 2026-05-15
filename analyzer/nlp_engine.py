import os
import numpy as np
import pandas as pd
import faiss
from sklearn.feature_extraction.text import TfidfVectorizer

# ==================================================
# BASE PATH
# ==================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")

JOB_PATH = os.path.join(DATA_DIR, "processed_jobs.csv")
FAISS_PATH = os.path.join(DATA_DIR, "faiss_index.index")
JOB_EMBEDDINGS_PATH = os.path.join(DATA_DIR, "job_embeddings.npy")

# ==================================================
# GLOBALS (LAZY LOADED)
# ==================================================
faiss_index = None
job_df = None
job_embeddings = None
vectorizer = None

# ==================================================
# LOAD ENGINE SAFELY (CRITICAL FIX)
# ==================================================
def load_engine():
    global faiss_index, job_df, job_embeddings, vectorizer

    if faiss_index is None:
        faiss_index = faiss.read_index(FAISS_PATH)

    if job_df is None:
        job_df = pd.read_csv(JOB_PATH, encoding="latin1")

    # Load embeddings (optional but now not heavily used)
    if job_embeddings is None:
        job_embeddings = np.load(JOB_EMBEDDINGS_PATH, mmap_mode="r")

    # Lightweight NLP fallback (NO TRANSFORMERS)
    if vectorizer is None:
        vectorizer = TfidfVectorizer(max_features=3000)
        text_data = (
            job_df["description"].fillna("").astype(str) + " " +
            job_df["skills"].fillna("").astype(str)
        )
        vectorizer.fit(text_data)


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

def extract_skills(text):
    text = str(text).lower()
    return [s for s in SKILL_LIBRARY if s in text]


# ==================================================
# FAISS SEARCH
# ==================================================
def search_jobs(embeddings, top_k=1):
    embeddings = np.array(embeddings).astype("float32")
    distances, indices = faiss_index.search(embeddings, top_k)
    return distances, indices


# ==================================================
# GET JOB
# ==================================================
def get_job_by_index(idx):
    return job_df.iloc[idx]


# ==================================================
# MAIN PIPELINE
# ==================================================
def run_alignment_analysis(df):
    load_engine()

    results = []

    df["combined_text"] = (
        df["course_title"].astype(str) + " " +
        df["course_description"].astype(str)
    )

    # ==================================================
    # EMBEDDINGS (NO TRANSFORMER - LIGHTWEIGHT TF-IDF)
    # ==================================================
    curriculum_embeddings = vectorizer.transform(
        df["combined_text"].tolist()
    ).toarray().astype("float32")

    # ==================================================
    # FAISS SEARCH
    # ==================================================
    distances, indices = search_jobs(curriculum_embeddings, top_k=1)

    # ==================================================
    # PROCESS RESULTS
    # ==================================================
    for i, row in df.iterrows():

        job_idx = int(indices[i][0])
        score = float(1 / (1 + distances[i][0]))

        job = get_job_by_index(job_idx)

        curriculum_skills = list(set(extract_skills(row["combined_text"])))

        # Safe job title handling
        job_title = job.get("title") or job.get("job_title")

        job_skills = job["skills"]

        # Normalize skills
        if isinstance(job_skills, str):
            job_skills = (
                job_skills.replace("[", "")
                .replace("]", "")
                .replace("'", "")
            )
            job_skills = [s.strip() for s in job_skills.split(",") if s.strip()]

        missing_skills = list(set(job_skills) - set(curriculum_skills))
        recommendations = [f"Learn {s}" for s in missing_skills]

        results.append({
            "course_name": row["course_title"],
            "matched_job": job_title,
            "similarity_score": round(score, 4),
            "extracted_skills": curriculum_skills,
            "missing_skills": missing_skills,
            "recommendations": recommendations
        })

    return results
