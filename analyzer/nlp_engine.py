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

# ==================================================
# GLOBALS
# ==================================================
faiss_index = None
job_df = None
vectorizer = None

# ==================================================
# SKILL LIBRARY (for extraction)
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
# SKILL WEIGHTS (NEW)
# ==================================================
CORE_SKILLS = {
    "python": 1.0,
    "java": 1.0,
    "sql": 1.0,
    "machine learning": 1.0,
    "javascript": 1.0,
    "php": 0.9,
    "django": 0.9,
    "flask": 0.9,
    "api": 0.9,
}

SOFT_SKILLS = {
    "communication": 0.5,
    "teamwork": 0.5,
    "problem solving": 0.6
}

# ==================================================
# LOAD ENGINE
# ==================================================
def load_engine():
    global faiss_index, job_df, vectorizer

    if faiss_index is None:
        faiss_index = faiss.read_index(FAISS_PATH)

    if job_df is None:
        job_df = pd.read_csv(JOB_PATH, encoding="latin1")

    if vectorizer is None:
        vectorizer = TfidfVectorizer(max_features=faiss_index.d)

        text_data = job_df.fillna("").astype(str).agg(" ".join, axis=1)
        vectorizer.fit(text_data)

# ==================================================
# SKILL EXTRACTION
# ==================================================
def extract_skills(text):
    text = str(text).lower()
    return [s for s in SKILL_LIBRARY if s in text]

# ==================================================
# WEIGHTED SKILL SCORE (NEW)
# ==================================================
def compute_weighted_skill_score(curr_skills, job_skills):

    curr_set = set([s.lower() for s in curr_skills])
    job_set = set([s.lower() for s in job_skills])

    if not job_set:
        return 0.0

    score = 0.0
    total_weight = 0.0

    for skill in job_set:
        weight = CORE_SKILLS.get(skill, SOFT_SKILLS.get(skill, 0.7))
        total_weight += weight

        if skill in curr_set:
            score += weight

    if total_weight == 0:
        return 0.0

    return score / total_weight

# ==================================================
# SKILL OVERLAP (backup signal)
# ==================================================
def compute_skill_overlap(curr_skills, job_skills):

    curr_set = set([s.lower() for s in curr_skills])
    job_set = set([s.lower() for s in job_skills])

    if len(job_set) == 0:
        return 0.0

    return len(curr_set.intersection(job_set)) / len(job_set)

# ==================================================
# TITLE BOOST (NEW)
# ==================================================
def compute_title_boost(job_title, curr_skills):

    if not job_title:
        return 0.0

    title = job_title.lower()
    boost = 0.0

    for skill in curr_skills:
        if skill in title:
            boost += 0.1

    return min(boost, 0.3)

# ==================================================
# FAISS SEARCH (TOP-5)
# ==================================================
def search_jobs(embeddings, top_k=5):

    embeddings = np.array(embeddings).astype("float32")
    distances, indices = faiss_index.search(embeddings, top_k)

    return distances, indices

# ==================================================
# GET JOB
# ==================================================
def get_job_by_index(idx):
    return job_df.iloc[idx]

# ==================================================
# MAIN PIPELINE (UPGRADED)
# ==================================================
def run_alignment_analysis(df):

    load_engine()

    results = []

    df["combined_text"] = (
        df["course_title"].astype(str) + " " +
        df["course_description"].astype(str)
    )

    # ==================================================
    # EMBEDDINGS
    # ==================================================
    curriculum_embeddings = vectorizer.transform(
        df["combined_text"].tolist()
    ).toarray().astype("float32")

    # ==================================================
    # TOP-5 SEARCH
    # ==================================================
    distances, indices = search_jobs(curriculum_embeddings, top_k=5)

    # ==================================================
    # PROCESS EACH ROW WITH RERANKING
    # ==================================================
    for i, row in df.iterrows():

        best_score = -1
        best_result = None

        curriculum_skills = list(set(extract_skills(row["combined_text"])))

        # --------------------------------------------------
        # RERANK TOP 5
        # --------------------------------------------------
        for rank in range(5):

            job_idx = int(indices[i][rank])
            faiss_score = float(1 / (1 + distances[i][rank]))

            job = get_job_by_index(job_idx)

            job_title = job.get("title") or job.get("job_title")

            job_skills = job["skills"]

            if isinstance(job_skills, str):
                job_skills = (
                    job_skills.replace("[", "")
                    .replace("]", "")
                    .replace("'", "")
                )
                job_skills = [s.strip().lower() for s in job_skills.split(",") if s.strip()]

            # -------------------------------
            # SCORES
            # -------------------------------
            weighted_skill = compute_weighted_skill_score(curriculum_skills, job_skills)
            overlap_skill = compute_skill_overlap(curriculum_skills, job_skills)
            title_boost = compute_title_boost(job_title, curriculum_skills)

            # -------------------------------
            # FINAL HYBRID SCORE
            # -------------------------------
            final_score = (
                (faiss_score * 0.5) +
                (weighted_skill * 0.3) +
                (overlap_skill * 0.1) +
                (title_boost * 0.1)
            )

            # -------------------------------
            # TRACK BEST MATCH
            # -------------------------------
            if final_score > best_score:
                best_score = final_score

                missing_skills = list(set(job_skills) - set(curriculum_skills))
                recommendations = [f"Learn {s}" for s in missing_skills]

                best_result = {
                    "course_name": row["course_title"],
                    "matched_job": job_title,

                    "faiss_score": round(faiss_score, 4),
                    "weighted_skill_score": round(weighted_skill, 4),
                    "skill_overlap": round(overlap_skill, 4),
                    "title_boost": round(title_boost, 4),

                    "similarity_score": round(final_score, 4),

                    "extracted_skills": curriculum_skills,
                    "missing_skills": missing_skills,
                    "recommendations": recommendations
                }

        results.append(best_result)

    return results
