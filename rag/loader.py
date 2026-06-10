import os
import json

def load_documents(data_dir="dokumen"):
    documents = []
    
    for root, dirs, files in os.walk(data_dir):
        for file in files:
            if file.endswith('.json'):
                file_path = os.path.join(root, file)
                with open(file_path, 
                          'r', 
                          encoding='utf-8'
                ) as f:
                    data = json.load(f)
                    documents.append(data)
    return documents

if __name__ == "__main__":
    docs = load_documents()
    print(f"Loaded {len(docs)} documents.")