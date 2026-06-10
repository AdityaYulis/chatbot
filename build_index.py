from rag.loader import load_documents
from rag.chucker import create_chunks
from rag.embedder import embed_texts
from rag.vector_store import save_chunks

documents = load_documents()

chunks = create_chunks(documents)

texts = [
    chunk['text'] 
    for chunk in chunks
]

embeddings = embed_texts(texts)

save_chunks(
    chunks,
    embeddings
)

print("Index berhasil dibuat dan disimpan ke dalam vector store.")