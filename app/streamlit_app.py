import streamlit as st
import sys, os
from PIL import Image
import json
import requests
from streamlit_lottie import st_lottie

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from scripts.parser import extract_text_from_file
from scripts.chunker import chunk_text
from scripts.embedder import embed_text
from scripts.vector_store import build_faiss_index
from scripts.question_answer import get_best_chunk
from scripts.gemini_api import generate_answer_from_chunks

# ----------------------
# 🌈 Load Lottie Animation
# ----------------------
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

qa_animation = load_lottieurl("https://lottie.host/7dbf5172-6f7a-4e6f-805f-bd3c29eeb598/X1Pt1WrG0P.json")

# ----------------------
# 🔧 Page Config
# ----------------------
st.set_page_config(
    page_title="Smart NLP QA Bot",
    page_icon="🧠",
    layout="wide"
)

# ----------------------
# 🎨 Custom Styling
# ----------------------
st.markdown("""
    <style>
    html, body {
        background-color: #f7f9fc;
        font-family: 'Segoe UI', sans-serif;
    }
    .main {
        background-color: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    }
    .stButton>button {
        background: linear-gradient(135deg, #2f80ed, #56ccf2);
        color: white;
        border: none;
        padding: 10px 16px;
        border-radius: 8px;
        font-weight: bold;
        transition: 0.3s ease;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #1c60d6, #3694f2);
        transform: scale(1.02);
    }
    </style>
""", unsafe_allow_html=True)

# ----------------------
# 🚀 Sidebar
# ----------------------
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/e/ed/SmartNLP.png/1200px-SmartNLP.png", width=150)
    st.markdown("## 🤖 Smart NLP QA Bot")
    st.write("This app lets you upload `.pdf`, `.docx`, or `.txt` files and ask questions directly from the document using Gemini + FAISS + Sentence Transformers.")
    st.markdown("---")
    st.markdown("🧑‍💻 Made by [Khubaib](https://github.com/Khubaib8281)")
    st.markdown("📬 Contact: `khubaib@example.com`")
    st.markdown("🌐 Powered by Gemini & Streamlit")

# ----------------------
# 💡 Header Section
# ----------------------
st.markdown("<h1 style='text-align: center;'>🧠 Smart NLP Document Q&A</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 18px;'>Ask intelligent questions from your document using cutting-edge AI!</p>", unsafe_allow_html=True)

st_lottie(qa_animation, height=250, key="docqa")

# ----------------------
# 📁 File Upload
# ----------------------
uploaded_file = st.file_uploader("📤 Upload a file (.txt, .pdf, .docx)", type=['txt', 'pdf', 'docx'])

if uploaded_file:
    with st.spinner("🧠 Reading and processing the document..."):
        text = extract_text_from_file(uploaded_file)
        chunks = chunk_text(text)

        if len(chunks) < 2:
            st.error("⚠️ Document is too short. Please upload a longer file.")
            st.stop()

        embeddings = embed_text(chunks)
        index = build_faiss_index(embeddings)

    st.success("✅ File processed successfully!")

    # ----------------------
    # ❓ Question Answering
    # ----------------------
    with st.container():
        st.markdown("### ❓ Ask a question")
        user_question = st.text_input("What would you like to know?")

        if user_question:
            with st.spinner("💬 Thinking..."):
                top_chunks = get_best_chunk(user_question, chunks, index)
                answer = generate_answer_from_chunks(top_chunks, user_question)

            st.markdown("### 📚 Answer")
            st.info(answer, icon="💡")

# ----------------------
# 🔚 Footer
# ----------------------
st.markdown("---")
st.markdown("<p style='text-align: center; font-size: 0.9rem;'>⚡ Built with 💙 by Khubaib | Powered by Gemini, FAISS, Sentence Transformers</p>", unsafe_allow_html=True)
