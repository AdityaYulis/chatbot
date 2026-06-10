import chromadb

client = chromadb.PersistentClient(
    path="./vectordb"
)

collection = client.get_or_create_collection(
    name="dikemas"
)

def save_chunks(chunks, embeddings):
    for i, chunk in enumerate(chunks):
        collection.add(
            ids=[f"chunk_{i}"],
            documents=[chunk['text']],
            metadatas=[chunk['metadata']],
            embeddings=[
                embeddings[i].tolist()
            ]
        )

def search(
        query_embedding,
        n_results=5
):
    
    return collection.query(
        query_embeddings=[
            query_embedding[0].tolist()
        ],
        n_results=n_results
    )
