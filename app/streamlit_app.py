import streamlit as st
import sys
import os
from PIL import Image

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from scripts.parser import extract_text_from_file
from scripts.chunker import chunk_text
from scripts.embedder import embed_text
from scripts.vector_store import build_faiss_index
from scripts.question_answer import get_best_chunk
from scripts.gemini_api import generate_answer_from_chunks

# ---------- 🔧 Streamlit Config ----------
st.set_page_config(page_title="Smart NLP QA Bot", page_icon="🤖", layout="wide")

# ---------- 🎨 Custom CSS for styling ----------
st.markdown("""
    <style>
    html, body, [class*="css"] {
        font-family: 'Segoe UI', sans-serif;
        background-color: #f0f2f6;
        color: #1c1e21;
    }

    .main {
        background-color: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    }

    h1 {
        color: #2f80ed;
    }

    .stTextInput>div>div>input {
        border: 2px solid #2f80ed;
        border-radius: 8px;
        padding: 10px;
    }

    .stTextInput>div>div>input:focus {
        border-color: #56ccf2;
        box-shadow: 0 0 5px rgba(86, 204, 242, 0.5);
    }

    .stButton>button {
        background-color: #2f80ed;
        color: white;
        border-radius: 8px;
        padding: 0.6rem 1.2rem;
        border: none;
        font-weight: 600;
        transition: background-color 0.3s ease;
    }

    .stButton>button:hover {
        background-color: #1c60d6;
    }

    .css-1aumxhk {
        padding: 1rem !important;
    }

    </style>
""", unsafe_allow_html=True)

# ---------- 🚀 App Title ----------
st.markdown("<h1 style='text-align: center;'>🤖 Smart Document Q&A Bot</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Upload a document (.pdf, .docx, .txt) and ask questions about its content.</p>", unsafe_allow_html=True)

# ---------- 📁 File Upload ----------
uploaded_file = st.file_uploader("📤 Upload your document file", type=['txt', 'pdf', 'docx'])

# ---------- 🧠 NLP Pipeline ----------
if uploaded_file:
    with st.spinner("🔍 Processing file..."):
        text = extract_text_from_file(uploaded_file)
        chunks = chunk_text(text)

        if len(chunks) < 2:
            st.warning("⚠️ The document is too short for QA.")
            st.stop()

        embeddings = embed_text(chunks)
        index = build_faiss_index(embeddings)

    st.success("✅ Document processed! Now ask your question below.")

    # ---------- ❓ Question Form ----------
    with st.form(key="qa_form"):
        user_question = st.text_input("💬 Ask a question based on the uploaded document:")
        submit_btn = st.form_submit_button("Get Answer")

    if submit_btn and user_question:
        with st.spinner("💬 Generating answer..."):
            top_chunks = get_best_chunk(user_question, chunks, index, k=3)
            answer = generate_answer_from_chunks(top_chunks, user_question)

        st.markdown("### 📚 Answer")
        st.success(answer)

# ---------- 🔚 Footer ----------
st.markdown("""
    <hr>
    <p style='text-align: center; font-size: 0.8rem; color: #888;'>Made with ❤️ by Khubaib</p>
""", unsafe_allow_html=True)
