# from io import BytesIO
# from docx import Document
# from PyPDF2 import PdfReader
# import os

# def extract_text_from_file(uploaded_file):
#     if not uploaded_file or not hasattr(uploaded_file, 'read'):
#         raise ValueError("Invalid file uploaded.")

#     file_bytes = uploaded_file.read()
#     buffer = BytesIO(file_bytes)
#     ext = os.path.splitext(uploaded_file.name)[1].lower()

#     if ext == '.txt':
#         return file_bytes.decode('utf-8', errors='ignore')

#     elif ext == '.docx':
#         doc = Document(buffer)
#         return '\n'.join([p.text for p in doc.paragraphs])

#     elif ext == '.pdf':
#         reader = PdfReader(buffer)
#         text = ''
#         for page in reader.pages:
#             content = page.extract_text()
#             if content:
#                 text += content + '\n'
#         return text

#     else:
#         raise ValueError("Unsupported file type. Please upload .txt, .docx, or .pdf")




from io import BytesIO
from docx import Document
from PyPDF2 import PdfReader
import os
import streamlit as st

def extract_text_from_file(uploaded_file):
    if not uploaded_file or not hasattr(uploaded_file, 'read'):
        return None, "Invalid file uploaded."

    file_bytes = uploaded_file.read()
    buffer = BytesIO(file_bytes)
    ext = os.path.splitext(uploaded_file.name)[1].lower()
    text = ""

    if ext == '.txt':
        text = file_bytes.decode('utf-8', errors='ignore')
    elif ext == '.docx':
        doc = Document(buffer)
        text = '\n'.join([p.text for p in doc.paragraphs])
    elif ext == '.pdf':
        reader = PdfReader(buffer)
        for page in reader.pages:
            content = page.extract_text()
            if content:
                text += content + '\n'
    else:
        return None, "Unsupported file type. Please upload .txt, .docx, or .pdf"

    if len(text) < 200:
        return text, "Document is too short. Please upload a file with more content."
    else:
        return text, "Document processed successfully."

# Example of how to use this in a Streamlit app
st.title("Document Text Extractor")

uploaded_file = st.file_uploader("Upload a file", type=['txt', 'docx', 'pdf'])

if uploaded_file:
    extracted_text, message = extract_text_from_file(uploaded_file)
    st.write(f"**Status:** {message}")
    if extracted_text:
        st.subheader("Extracted Text")
        st.text_area("File Content", extracted_text, height=300)
