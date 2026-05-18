import os
import pandas as pd
import numpy as np
import faiss

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD

# ==================================================
# ROOT DIRECTORY
# ==================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ==================================================
# FILE PATHS
# ==================================================
JOB_PATH = os.path.join(BASE_DIR, "processed_jobs.csv")
FAISS_PATH = os.path.join(BASE_DIR, "faiss_index.index")

# ==================================================
# LOAD DATA
# ==================================================
job_df = pd.read_csv(JOB_PATH)

# ==================================================
# COMBINE TEXT
# ==================================================
job_df["combined_text"] = (
    job_df.fillna("").astype(str).agg(" ".join, axis=1)
)

# ==================================================
# TF-IDF
# ==================================================
vectorizer = TfidfVectorizer(
    max_features=3000,
    ngram_range=(1, 2)
)

tfidf_matrix = vectorizer.fit_transform(
    job_df["combined_text"]
)

# ==================================================
# SVD SEMANTIC LAYER
# ==================================================
svd_model = TruncatedSVD(
    n_components=min(300, tfidf_matrix.shape[1] - 1),
    random_state=42
)

semantic_embeddings = svd_model.fit_transform(
    tfidf_matrix
)

semantic_embeddings = semantic_embeddings.astype("float32")

# ==================================================
# BUILD FAISS
# ==================================================
dimension = semantic_embeddings.shape[1]

index = faiss.IndexFlatL2(dimension)

index.add(semantic_embeddings)

# ==================================================
# SAVE INDEX
# ==================================================
faiss.write_index(index, FAISS_PATH)

# ==================================================
# SUCCESS MESSAGE
# ==================================================
print("FAISS rebuilt successfully.")
print("FAISS saved to:", FAISS_PATH)
print("Embedding shape:", semantic_embeddings.shape)
print("FAISS dimension:", dimension)