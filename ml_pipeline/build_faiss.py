import numpy as np
import pandas as pd
import faiss


# ==========================================
# LOAD DATA
# ==========================================
df = pd.read_csv("processed_jobs.csv", encoding="latin1")

embeddings = np.load("job_embeddings.npy").astype("float32")

print("Embeddings shape:", embeddings.shape)


# ==========================================
# GET VECTOR DIMENSION
# ==========================================
dim = embeddings.shape[1]


# ==========================================
# BUILD INDEX
# ==========================================
index = faiss.IndexFlatL2(dim)

index.add(embeddings)


# ==========================================
# SAVE INDEX
# ==========================================
faiss.write_index(index, "faiss_index.index")

print("FAISS index saved successfully.")
