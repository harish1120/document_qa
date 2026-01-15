import streamlit as st
import requests

BACKEND_URL = "http://localhost:8000"
TIMEOUT = 60

st.title("📄 PDF Question Answering (RAG)")

uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])

if uploaded_file:
    files = {"file": uploaded_file}
    res = requests.post(f"{BACKEND_URL}/upload_pdf", files=files, timeout=TIMEOUT)
    st.success("PDF uploaded")

    pdf_path = res.json()["path"]

    if st.button("Index Document"):
        requests.post(
            f"{BACKEND_URL}/index",
            params={"path": pdf_path},
            timeout=TIMEOUT
        )
        st.success("Document indexed")

st.divider()

question = st.text_input("Ask a question")

if question:
    res = requests.post(
        f"{BACKEND_URL}/ask",
        json={"question": question},
        timeout=TIMEOUT
    )

    if res.status_code == 200:
        data = res.json()
        st.markdown("### Answer")
        st.write(data["answer"])

        st.markdown("### Sources")
        for s in data["sources"]:
            st.write("-", s)
    else:
        st.error(res.json()["detail"])
