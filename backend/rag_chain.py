from langchain_community.vectorstores import Chroma
import google.generativeai as genai

from backend.llm_setup import get_embeddings

VECTOR_DIR = "storage/chroma"
COLLECTION = "project_docs"

vs = Chroma(
    collection_name=COLLECTION,
    embedding_function=get_embeddings(),
    persist_directory=VECTOR_DIR,
)

retriever = vs.as_retriever()


def answer_from_docs(query: str) -> str:
    docs = retriever.get_relevant_documents(query)
    context_text = "\n\n".join([d.page_content for d in docs])

    prompt = f"Answer the question based on the following documents:\n{context_text}\nQuestion: {query}\nAnswer:"

    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)

    return response.text
