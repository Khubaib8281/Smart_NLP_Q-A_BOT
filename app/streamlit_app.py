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
# ✨ Light Theme CSS Styling
# ────────────────────────
st.markdown("""
<style>
/* Global Styles */
html, body, [class*="css"] {
    background-color: #ffffff;
    font-family: 'Segoe UI', sans-serif;
    color: #333333;
}

/* Streamlit title override */
.title-style {
    font-size: 2.8rem;
    font-weight: 700;
    color: #2c3e50;
    text-align: center;
    margin-bottom: 1rem;
}

/* File uploader styling */
section[data-testid="stFileUploader"] > div {
    border: 2px dashed #c0c0c0;
    background-color: #fafafa;
    border-radius: 10px;
    padding: 1.5rem;
    transition: 0.3s ease-in-out;
}

section[data-testid="stFileUploader"] > div:hover {
    background-color: #f0f0f0;
}

/* Input box */
input[type="text"] {
    border: 1px solid #cccccc;
    border-radius: 5px;
    padding: 0.5rem;
}

/* Answer box */
.stSuccess {
    background-color: #f6fff9;
    color: #1d5e3b;
    font-weight: 500;
    border-left: 5px solid #27ae60;
    padding: 1rem;
    margin-top: 1rem;
    border-radius: 10px;
}

/* Expander content */
[data-testid="stExpander"] div[role="button"] {
    background-color: #f2f2f2;
    color: #333333;
    border-radius: 8px;
    font-weight: bold;
}

[data-testid="stExpander"] .streamlit-expanderContent {
    background-color: #ffffff;
    color: #333333;
    border-left: 4px solid #cccccc;
    padding: 1rem;
}

/* Footer */
.footer {
    margin-top: 4rem;
    text-align: center;
    font-size: 14px;
    color: #888888;
}
</style>
""", unsafe_allow_html=True)

# ────────────────────────
# 📌 TITLE & HEADER
# ────────────────────────
st.markdown("<div class='title-style'>📝 AskMyDoc</div>", unsafe_allow_html=True)
st.write("Upload your document and ask questions about its content.")

# ℹ️ How it Works
with st.expander("ℹ️ How It Works"):
    st.markdown("""
    1. **Upload your document** (`.txt`, `.pdf`, `.docx`)  
    2. It gets converted into text, split into smart chunks  
    3. **Ask your question** → AI finds the best answers from context  
    """)

# 📤 File Upload
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

    # ❓ Q&A Section
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

# 📌 Footer
st.markdown("""
<div class='footer'>
    &copy; 2025 • Built with ❤️ by <strong>Khubaib</strong> | Smart NLP Q&A Bot
</div>
""", unsafe_allow_html=True)
