import streamlit as st
import os
import sys

# Append project path for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from scripts.parser import extract_text_from_file
from scripts.chunker import chunk_text
from scripts.embedder import embed_text
from scripts.vector_store import build_faiss_index
from scripts.question_answer import get_best_chunk
from scripts.gemini_api import generate_answer_from_chunks

# Page configuration
st.set_page_config(page_title="Smart Document Q&A Assistant", page_icon="📄", layout="centered")

# ────────────────────────
# ✨ Custom CSS Styling
# ────────────────────────
# Style fixes
st.markdown("""
    <style>
        html, body {
            font-family: 'Segoe UI', sans-serif;
            background-color: #f5f7fa;
        }
        .stButton > button {
            background-color: #0066cc;
            color: white;
            padding: 0.6rem 1.2rem;
            font-weight: 600;
            border-radius: 8px;
            border: none;
            transition: background-color 0.3s ease;
        }
        .stButton > button:hover {
            background-color: #004d99;
            cursor: pointer;
        }
        .footer {
            text-align: center;
            color: #999;
            font-size: 0.85rem;
            margin-top: 3rem;
            padding-top: 2rem;
            border-top: 1px solid #e6e6e6;
        }
        .how-it-works {
            background-color: #e9eff6;
            padding: 1.5rem;
            border-radius: 10px;
            border: 1px solid #d0d9e0;
            color: #333;
            font-size: 0.95rem;
            line-height: 1.6;
            box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        }
    </style>
""", unsafe_allow_html=True)

# Updated "How it Works"
with st.expander("ℹ️ How It Works"):
    st.markdown("""
    <div class='how-it-works'>
        1. Upload your document (TXT, PDF, DOCX).<br>
        2. It is split into chunks and converted into smart vectors.<br>
        3. Ask any question — we fetch the most relevant content chunks.<br>
    </div>
    """, unsafe_allow_html=True)


# ────────────────────────
# 📤 File Upload
# ────────────────────────
uploaded_file = st.file_uploader("📁 Upload your file", type=["txt", "pdf", "docx"])

# Initialize document processing
if uploaded_file:
    with st.spinner("🔍 Processing document..."):
        text = extract_text_from_file(uploaded_file)
        chunks = chunk_text(text)

        if len(chunks) < 2:
            st.error("⚠️ The document is too short for answering questions.")
            st.stop()

        embeddings = embed_text(chunks)
        index = build_faiss_index(embeddings)

    st.success("✅ Document processed successfully!")

    # ────────────────────────
    # ❓ Q&A Section
    # ────────────────────────
    st.subheader("💬 Ask a Question")
    user_question = st.text_input("Enter your question here")

    if st.button("🧠 Get Answer"):
        if user_question.strip() == "":
            st.warning("⚠️ Please enter a question.")
        else:
            with st.spinner("⏳ Analyzing document and generating answer..."):
                top_chunks = get_best_chunk(user_question, chunks, index)
                answer = generate_answer_from_chunks(top_chunks, user_question)
            st.markdown("### 📚 Answer")
            st.success(answer)

# ────────────────────────
# 📌 Footer
# ────────────────────────
st.markdown("""
    <div class='footer'>
        &copy; 2025 • Built with ❤️ by <strong>Khubaib</strong> | Smart NLP Q&A Bot
    </div>
""", unsafe_allow_html=True)
