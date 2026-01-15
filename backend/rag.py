from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate

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
    embeddings = OpenAIEmbeddings()
    db = FAISS.load_local(VECTOR_DIR, embeddings,
                          allow_dangerous_deserialization=True)

    docs = db.similarity_search(question, k=10)
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
