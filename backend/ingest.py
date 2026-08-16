from pathlib import Path
from typing import Iterable

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_community.document_loaders import PyPDFLoader, TextLoader

from backend.llm_setup import get_embeddings

VECTOR_DIR = "storage/chroma"
COLLECTION = "project_docs"


def load_paths(paths: Iterable[str]):
    docs = []
    for p in paths:
        path = Path(p)
        if path.suffix.lower() == ".pdf":
            docs.extend(PyPDFLoader(str(path)).load())
        else:
            docs.extend(TextLoader(str(path), encoding="utf-8").load())
    return docs


def build_or_update_index(paths: list[str]) -> Chroma:
    raw_docs = load_paths(paths)
    splitter = RecursiveCharacterTextSplitter(chunk_size=1200, chunk_overlap=150)
    chunks = splitter.split_documents(raw_docs)

    embeddings = get_embeddings()
    vs = Chroma(collection_name=COLLECTION, embedding_function=embeddings, persist_directory=VECTOR_DIR)
    vs.add_documents(chunks)
    return vs


if __name__ == "__main__":
    sample_docs = [str(p) for p in Path("docs").glob("*.*")]
    if sample_docs:
        build_or_update_index(sample_docs)
