import os
import time
import hashlib
import logging
import re
from unittest import result
from unittest import result

import google.generativeai as genai

from rag.embedder import embed_query
from rag.vector_store import search
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO)

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError(
        "GEMINI_API_KEY tidak ditemukan di file .env"
    )

genai.configure(
    api_key=api_key
)

model = genai.GenerativeModel(
    "gemini-2.5-flash"
)

CACHE = {}

LAST_REQUEST_TIME = 0

def wait_for_rate_limit():
    global LAST_REQUEST_TIME

    current_time = time.time()
    elapsed_time = current_time - LAST_REQUEST_TIME

    # 5 RPM = 1 request per 12 seconds
    if elapsed_time < 12:
        time.sleep(12 - elapsed_time)
    LAST_REQUEST_TIME = time.time()

def ask (question: str):
    # caching mechanism
    cache_key = hashlib.md5(
        question.lower().strip().encode()
    ).hexdigest()

    if cache_key in CACHE:
        return CACHE[cache_key]
    
    # retrieval
    
    query_embedding = embed_query(question)

    results = search(
        query_embedding=query_embedding,
        n_results=3
        )
    
    if (
        not results.get('documents')
        or len(results['documents'][0]) == 0
        or len(results['metadatas'][0]) == 0
    ):
        return {
            "answer": "Tidak ditemukan informasi yang relevan",
            "sources": []
        }

    documents = results['documents'][0]
    metadatas = results['metadatas'][0]

    # limit context to 3 documents
    context = "\n\n".join(documents)

    MAX_CONTEXT_LENGTH = 4000

    if len(context) > MAX_CONTEXT_LENGTH:
        context = context[:MAX_CONTEXT_LENGTH]

    # prompt construction
    prompt = f"""
        Anda adalah chatbot customer service website diKemas.

            Tugas Anda:
            - Jawab hanya berdasarkan konteks.
            - Jangan mengarang informasi.
            - Jika informasi tidak ditemukan, katakan:
            "Informasi tidak tersedia pada data yang saya miliki."

            Format jawaban:
            - Jika jawaban berisi daftar produk, layanan, mesin, artikel, atau lebih dari 2 item, gunakan format daftar bernomor.
            - Jangan gunakan bullet (*, -, •).
            - Gunakan format:

            1. Item pertama
            2. Item kedua
            3. Item ketiga

            Pastikan setiap item berada pada baris baru.

            - Jangan menampilkan URL.
            - Jangan menampilkan judul halaman website.
            - Berikan jawaban yang rapi dan mudah dibaca.

KONTEKS:
{context}

PERTANYAAN:
{question}
"""
    # rate limit handling
    wait_for_rate_limit()

    # generate response
    try :

        response = model.generate_content(
            prompt,
            generation_config={
                "temperature": 0.5,
                "max_output_tokens": 500
            }
        )

        answer = getattr(
            response,
            "text",
            "Maaf, saya tidak dapat memproses permintaan Anda."
        )

        answer = re.sub(
            r'(\d+\.)',
            r'\n\1',
            answer
        )

        answer = answer.strip()

    except Exception as e:
        logging.error(f"Gemini Error: {e}")

        return {
            "answer": (
                "Maaf, terjadi kesalahan saat memproses permintaan Anda."
                "Silakan coba beberapa saat lagi."
            ),
            "sources": []
        }

    result = {
        "answer": answer,
        "sources": [
            {
                "title": m.get('title'),
                "url": m.get('url'),
            }
            for m in metadatas
        ]
    }
    
    # cache the result
    CACHE[cache_key] = result

    return result