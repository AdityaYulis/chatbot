from sentence_transformers import SentenceTransformer

MODEL_NAME = "all-MiniLM-L6-v2"

model = SentenceTransformer(MODEL_NAME)

def embed_texts(texts):
    return model.encode(texts, show_progress_bar=True)

def embed_query(query):
    return model.encode([query])