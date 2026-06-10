from langchain_text_splitters import RecursiveCharacterTextSplitter

def create_chunks(documents):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, 
        chunk_overlap=200
        )
    
    chunks = []

    for doc in documents:
        text_chunks = splitter.split_text(
            doc['content']
        )

        for idx, chunk in enumerate(text_chunks):
            chunks.append({
                "text": chunk,
                "metadata": {
                    "title" : doc['title'],
                    "url" : doc['url'],
                    "category" : doc['category'],
                    "chunk_id": idx
                }
            })
    return chunks