import streamlit as st
import sys
import docx
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from scripts.parser import extract_text_from_file
from scripts.chunker import chunk_text
from scripts.embedder import embed_text
from scripts.vector_store import build_faiss_index
from scripts.main import get_best_chunk
from scripts.gemini_api import generate_answer_from_chunks
import tempfile

st.set_page_config(page_title="Smart NLP QA Bot", layout="wide")

st.title("🤖 Smart Document Q&A Bot")
st.write("Upload a document (.pdf, .docx, .txt) and ask questions about its content.")

# Upload file
uploaded_file = st.file_uploader("Upload your file", type=['txt', 'pdf', 'docx'])

if uploaded_file:
    with st.spinner("🔍 Processing file..."):
        temp_file = tempfile.NamedTemporaryFile(delete=False)
        temp_file.write(uploaded_file.read())
        temp_file_path = temp_file.name

        text = extract_text_from_file(temp_file_path)
        chunks = chunk_text(text)
        if len(chunks) < 2:
            st.warning("⚠️ The document is too short for QA.")
            st.stop()

        embeddings = embed_text(chunks)
        index = build_faiss_index(embeddings)

    st.success("✅ File processed successfully!")

    # Question Answering
    st.markdown("### ❓ Ask a Question")
    user_question = st.text_input("Enter your question:")

    if user_question:
        with st.spinner("💬 Generating answer..."):
            top_chunks = get_best_chunk(user_question, chunks, index, k=3)
            answer = generate_answer_from_chunks(top_chunks, user_question)
        st.markdown("### 📚 Answer")
        st.success(answer)


# streamlit run app/streamlit_app.py
