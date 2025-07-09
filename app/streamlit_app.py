import streamlit as st
import os
import sys

# Adjust path for module imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from scripts.parser import extract_text_from_file
from scripts.chunker import chunk_text
from scripts.embedder import embed_text
from scripts.vector_store import build_faiss_index
from scripts.question_answer import get_best_chunk
from scripts.gemini_api import generate_answer_from_chunks

# ──────────────────────────────────────────────────────────────
# 🎨 Page Config
# ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Smart Document Q&A Assistant",
    page_icon="📄",
    layout="wide"
)

# 🔧 Custom Styling
st.markdown("""
    <style>
        html, body, [class*="css"]  {
            font-family: 'Segoe UI', sans-serif;
            background-color: #f8f9fa;
        }
        h1 {
            color: #333;
        }
        .stTextInput>div>div>input {
            padding: 10px;
            border-radius: 6px;
            border: 1px solid #ccc;
        }
        .stFileUploader>div>div {
            border-radius: 6px;
            background-color: #fff;
        }
        .stButton>button {
            border-radius: 6px;
            background-color: #0066cc;
            color: white;
            padding: 0.6rem 1.2rem;
            font-weight: 600;
            transition: background-color 0.2s ease;
        }
        .stButton>button:hover {
            background-color: #004999;
        }
    </style>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────
# 🚀 Header
# ──────────────────────────────────────────────────────────────
st.title("📄 Smart Document Q&A Assistant")
st.caption("Upload a `.txt`, `.pdf`, or `.docx` document, then ask anything based on its contents. Powered by Google Gemini AI.")

# ──────────────────────────────────────────────────────────────
# 📤 File Upload
# ──────────────────────────────────────────────────────────────
uploaded_file = st.file_uploader("Select a document", type=["txt", "pdf", "docx"])

if uploaded_file:
    with st.spinner("🔍 Extracting and processing document..."):
        text = extract_text_from_file(uploaded_file)
        chunks = chunk_text(text)

        if len(chunks) < 2:
            st.error("❗ The document is too short for Q&A. Please upload a more detailed file.")
            st.stop()

        embeddings = embed_text(chunks)
        index = build_faiss_index(embeddings)

    st.success("✅ Document processed successfully.")

    # ──────────────────────────────────────────────────────────────
    # 🧠 Q&A Interaction
    # ──────────────────────────────────────────────────────────────
    st.subheader("💬 Ask a Question")
    user_question = st.text_input("Type your question here...")

    if user_question:
        with st.spinner("🧠 Thinking..."):
            top_chunks = get_best_chunk(user_question, chunks, index)
            answer = generate_answer_from_chunks(top_chunks, user_question)

        st.markdown("### 📝 Answer")
        st.info(answer)
