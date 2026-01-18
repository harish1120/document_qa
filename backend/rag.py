from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate
from rank_bm25 import BM25Okapi
import pickle
import numpy as np

VECTOR_DIR = "vectorstore"

PROMPT = """
You are a helpful assistant.
Answer the question using ONLY the context below.
If the answer is not in the context, say "I don't know".

Context:
{context}

Question:
{question}

Answer:
"""


def answer_question(question: str):
    # embeddings = OpenAIEmbeddings()
    # db = FAISS.load_local(VECTOR_DIR, embeddings,
    #                       allow_dangerous_deserialization=True)

    docs = hybrid_search(question, k=10)
    context = "\n\n".join([d.page_content for d in docs])

    llm = ChatOpenAI(model="gpt-5-nano", temperature=0.5)

    prompt = PromptTemplate(
        template=PROMPT,
        input_variables=["context", "question"]
    )

    response = llm.invoke(prompt.format(
        context=context,
        question=question
    ))

    sources = []
    for d in docs:
        sources.append({
            "content": d.page_content,
            "page": d.metadata.get("page"),
            "source": d.metadata.get("source"),
        })

    return response.content, sources


def hybrid_search(query: str, k: int = 5, alpha: float = 0.5):
    embeddings = OpenAIEmbeddings()
    db = FAISS.load_local(VECTOR_DIR, embeddings,
                          allow_dangerous_deserialization=True)

    with open(f"{VECTOR_DIR}/docs.pkl", "rb") as f:
        documents = pickle.load(f)

    bm25 = BM25Okapi([doc.page_content.split() for doc in documents])

    # dense
    dense_docs = db.similarity_search_with_score(query, k=10)

    # sparse
    tokenized_query = query.split()
    bm25_scores = bm25.get_scores(tokenized_query)

    bm25_scores = (bm25_scores - np.min(bm25_scores)) / (
        np.max(bm25_scores) - np.min(bm25_scores) + 1e-9
    )

    scored = []
    for idx, (doc, dense_score) in enumerate(dense_docs):
        sparse_score = bm25_scores[idx]
        final_score = alpha * (1 - dense_score) + (1 - alpha) * sparse_score
        scored.append((doc, final_score))

    scored.sort(key=lambda x: x[1], reverse=True)
    return [doc for doc, _ in scored[:k]]
