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
/* Global Styles */
body {
    background-color: #f2f6fc;
    font-family: 'Segoe UI', sans-serif;
}

/* Center the app title */
h1 {
    color: #1f4e79;
    text-align: center;
    padding-top: 1rem;
}

/* File uploader styling */
.css-1cpxqw2 {
    border: 2px dashed #4682b4;
    background-color: #eaf4ff;
    border-radius: 10px;
    padding: 1.5rem;
    transition: 0.3s ease-in-out;
}

.css-1cpxqw2:hover {
    background-color: #d4eaff;
}

/* Text input styling */
input[type="text"] {
    border: 1px solid #4682b4;
    border-radius: 5px;
    padding: 0.5rem;
}

/* Answer box */
.stSuccess {
    background-color: #e0f3ec;
    color: #1e4633;
    font-weight: 500;
    border-left: 5px solid #2e8b57;
    padding: 1rem;
    margin-top: 1rem;
    border-radius: 10px;
}

/* Spinner loading color */
.css-1y4p8pa {
    color: #4682b4 !important;
}

/* "How it Works" Section */
.how-it-works-section {
    background-color: #ffffff;
    padding: 2rem;
    border-radius: 10px;
    margin-top: 2rem;
    border-left: 5px solid #1f4e79;
    box-shadow: 0 4px 12px rgba(0,0,0,0.05);
}

.how-it-works-section h3 {
    color: #1f4e79;
    font-size: 22px;
    margin-bottom: 1rem;
}

.how-it-works-section p {
    color: #333333;
    line-height: 1.6;
    font-size: 16px;
    margin-bottom: 0.5rem;
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
