from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from pathlib import Path
import pickle
from dotenv import load_dotenv
load_dotenv()

VECTOR_DIR = "vectorstore"


def ingest_pdf(pdf_path: str):
    loader = PyPDFLoader(pdf_path)
    documents = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )
    chunks = splitter.split_documents(documents)

    embeddings = OpenAIEmbeddings()
    db = FAISS.from_documents(chunks, embeddings)

    Path(VECTOR_DIR).mkdir(exist_ok=True)
    db.save_local(VECTOR_DIR)

    with open(f"{VECTOR_DIR}/docs.pkl", "wb") as f:
        pickle.dump(chunks, f)

if __name__ == "__main__":
    ingest_pdf("/Users/harishsundaralingam/myworkspace/document_qa/data/uploads/AI Engineering.pdf")