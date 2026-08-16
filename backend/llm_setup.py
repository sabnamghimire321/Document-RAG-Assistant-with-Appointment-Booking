import os

import google.generativeai as genai
from langchain.embeddings.base import Embeddings

api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY not set. Please run: export GEMINI_API_KEY='your_key_here'")

genai.configure(api_key=api_key)


class GeminiEmbeddings(Embeddings):
    def embed_documents(self, texts):
        embeddings = []
        for text in texts:
            response = genai.embed_content(model="models/embedding-001", content=text)
            embeddings.append(response["embedding"])
        return embeddings

    def embed_query(self, text):
        return self.embed_documents([text])[0]


def get_embeddings():
    return GeminiEmbeddings()
