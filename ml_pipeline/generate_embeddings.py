import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer


# ==========================================
# LOAD CLEANED JOB DATA
# ==========================================
df = pd.read_csv("processed_jobs.csv", encoding="latin1")

print("Loaded:", df.shape)


# ==========================================
# LOAD MODEL (ONCE)
# ==========================================
model = SentenceTransformer("all-MiniLM-L6-v2")


# ==========================================
# GENERATE EMBEDDINGS
# ==========================================
texts = df["combined_text"].tolist()

print("Generating embeddings...")

embeddings = model.encode(
    texts,
    show_progress_bar=True,
    batch_size=32
)

embeddings = np.array(embeddings).astype("float32")


# ==========================================
# SAVE EMBEDDINGS
# ==========================================
np.save("job_embeddings.npy", embeddings)

print("Embeddings saved:", embeddings.shape)