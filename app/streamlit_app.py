import streamlit as st
import os
import sys

# Local script imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from scripts.parser import extract_text_from_file
from scripts.chunker import chunk_text
from scripts.embedder import embed_text
from scripts.vector_store import build_faiss_index
from scripts.question_answer import get_best_chunk
from scripts.gemini_api import generate_answer_from_chunks

# ---------- PAGE SETUP ----------
st.set_page_config(
    page_title="Smart NLP Q&A Bot",
    page_icon="🤖",
    layout="wide"
)

# ---------- CUSTOM CSS ----------
st.markdown("""
    <style>
        .main {
            background-color: #f7f7f7;
        }
        .stTextInput>div>div>input {
            background-color: #fff !important;
        }
        .stFileUploader>div>div {
            background-color: #fff !important;
        }
        .stButton>button {
            border-radius: 8px;
            padding: 0.5rem 1rem;
            background-color: #4CAF50;
            color: white;
            font-weight: 600;
        }
        .stButton>button:hover {
            background-color: #45a049;
        }
        .css-18e3th9 {
            padding-top: 2rem;
        }
    </style>
""", unsafe_allow_html=True)

# ---------- HEADER ----------
st.title("🤖 Smart NLP Document Q&A Bot")
st.markdown("Upload a `.pdf`, `.docx`, or `.txt` file and ask questions about its contents using natural language. Powered by Google Gemini API.")

# ---------- FILE UPLOAD ----------
uploaded_file = st.file_uploader("📄 Upload your document", type=["txt", "pdf", "docx"])

if uploaded_file:
    st.info("📤 File uploaded successfully! Processing...")

    # Read and process the file
    text = extract_text_from_file(uploaded_file)
    chunks = chunk_text(text)

    if len(chunks) < 2:
        st.warning("⚠️ The document is too short for meaningful Q&A.")
        st.stop()

    with st.spinner("🔍 Creating embeddings and building index..."):
        embeddings = embed_text(chunks)
        index = build_faiss_index(embeddings)

    st.success("✅ Document processed. Ready for questions!")

    # ---------- USER QUESTION ----------
    st.markdown("### ❓ Ask a Question")
    user_question = st.text_input("Type your question below:")

    if user_question:
        with st.spinner("💬 Generating answer..."):
            top_chunks = get_best_chunk(user_question, chunks, index)
            answer = generate_answer_from_chunks(top_chunks, user_question)

        st.markdown("### 📚 Answer")
        st.success(answer)
