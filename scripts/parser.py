from io import BytesIO
from docx import Document
from PyPDF2 import PdfReader
import os

def extract_text_from_file(uploaded_file):
    if uploaded_file is None:
        raise ValueError("No file uploaded.")

    filename = uploaded_file.name
    ext = os.path.splitext(filename)[1].lower()

    file_bytes = uploaded_file.read()  # ✅ Read file content once
    buffer = BytesIO(file_bytes)       # ✅ Wrap it in buffer

    if ext == '.txt':
        return file_bytes.decode('utf-8', errors='ignore')

    elif ext == '.docx':
        doc = Document(buffer)
        return '\n'.join([p.text for p in doc.paragraphs])

    elif ext == '.pdf':
        reader = PdfReader(buffer)
        text = ''
        for page in reader.pages:
            content = page.extract_text()
            if content:
                text += content + '\n'
        return text

    else:
        raise ValueError("Unsupported file type. Please upload .txt, .docx, or .pdf")
