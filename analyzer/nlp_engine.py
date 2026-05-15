import os
import numpy as np
import pandas as pd
import faiss

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD

# ==================================================
# PATHS
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
svd_model = None

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

CORE_SKILLS = {
    "python": 1.0,
    "java": 1.0,
    "sql": 1.0,
    "machine learning": 1.0,
    "javascript": 1.0,
    "api": 0.9,
    "django": 0.9,
    "flask": 0.9,
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
    global faiss_index, job_df, vectorizer, svd_model

    if faiss_index is None:
        faiss_index = faiss.read_index(FAISS_PATH)

    if job_df is None:
        job_df = pd.read_csv(JOB_PATH, encoding="latin1")

    # TF-IDF
    if vectorizer is None:
        vectorizer = TfidfVectorizer(
            max_features=faiss_index.d,
            ngram_range=(1, 2)
        )

        text_data = job_df.fillna("").astype(str).agg(" ".join, axis=1)
        tfidf_matrix = vectorizer.fit_transform(text_data)

        # ==================================================
        # SVD SEMANTIC LAYER (NEW)
        # ==================================================
        svd_model = TruncatedSVD(
            n_components=min(300, tfidf_matrix.shape[1] - 1)
        )

        svd_model.fit(tfidf_matrix)


# ==================================================
# SKILL EXTRACTION
# ==================================================
def extract_skills(text):
    text = str(text).lower()
    return [s for s in SKILL_LIBRARY if s in text]


# ==================================================
# SKILL SCORE (CLEAN FIX)
# ==================================================
def compute_weighted_skill_score(curr_skills, job_skills):

    curr_set = set([s.lower() for s in curr_skills])
    job_set = set([s.lower() for s in job_skills])

    if not job_set:
        return 0.0

    score = 0.0
    total = 0.0

    for s in job_set:
        w = CORE_SKILLS.get(s, SOFT_SKILLS.get(s, 0.7))
        total += w
        if s in curr_set:
            score += w

    return min(score / total, 0.85) if total > 0 else 0.0


# ==================================================
# OVERLAP SCORE (FIXED)
# ==================================================
def compute_skill_overlap(curr_skills, job_skills):

    curr_set = set([s.lower() for s in curr_skills])
    job_set = set([s.lower() for s in job_skills])

    if not job_set:
        return 0.0

    return len(curr_set.intersection(job_set)) / len(job_set)


# ==================================================
# TITLE BOOST + PENALTY SYSTEM
# ==================================================
def compute_title_effect(job_title, curr_skills):

    if not job_title:
        return 0.0

    title = job_title.lower()
    boost = 0.0

    # boost if skill appears in title
    for s in curr_skills:
        if s in title:
            boost += 0.08

    # penalty for UX/UI noise bias
    if any(x in title for x in ["ux", "ui", "designer"]):
        boost -= 0.1

    return max(min(boost, 0.25), -0.25)


# ==================================================
# FAISS SEARCH
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
# MAIN PIPELINE (FINAL UPGRADED)
# ==================================================
def run_alignment_analysis(df):

    load_engine()

    results = []

    df["combined_text"] = (
        df["course_title"].astype(str) + " " +
        df["course_description"].astype(str)
    )

    # ==================================================
    # SEMANTIC EMBEDDING (SVD TRANSFORM)
    # ==================================================
    tfidf_matrix = vectorizer.transform(df["combined_text"])
    semantic_embeddings = svd_model.transform(tfidf_matrix).astype("float32")

    # ==================================================
    # FAISS SEARCH
    # ==================================================
    distances, indices = search_jobs(semantic_embeddings, top_k=5)

    # ==================================================
    # RERANKING
    # ==================================================
    for i, row in df.iterrows():

        best_score = -1
        best_result = None

        curriculum_skills = list(set(extract_skills(row["combined_text"])))

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

            # ==================================================
            # SCORES
            # ==================================================
            weighted = compute_weighted_skill_score(curriculum_skills, job_skills)
            overlap = compute_skill_overlap(curriculum_skills, job_skills)
            title_effect = compute_title_effect(job_title, curriculum_skills)

            final_score = (
                (faiss_score * 0.45) +
                (weighted * 0.35) +
                (overlap * 0.10) +
                (title_effect * 0.10)
            )

            if final_score > best_score:

                best_score = final_score

                missing_skills = list(set(job_skills) - set(curriculum_skills))
                recommendations = [f"Learn {s}" for s in missing_skills]

                best_result = {
                    "course_name": row["course_title"],
                    "matched_job": job_title,

                    "faiss_score": round(faiss_score, 4),
                    "weighted_skill_score": round(weighted, 4),
                    "skill_overlap": round(overlap, 4),
                    "title_effect": round(title_effect, 4),

                    "similarity_score": round(final_score, 4),

                    "extracted_skills": curriculum_skills,
                    "missing_skills": missing_skills,
                    "recommendations": recommendations
                }

        results.append(best_result)

    return results
