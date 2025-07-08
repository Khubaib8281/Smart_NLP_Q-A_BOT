from io import BytesIO
from docx import Document
from PyPDF2 import PdfReader
import os

def extract_text_from_file(uploaded_file):
    ext = os.path.splitext(uploaded_file.name)[1].lower()
    file_bytes = uploaded_file.read()  # 🔑 Read once

    if ext == '.txt':
        return file_bytes.decode('utf-8')

    elif ext == '.docx':
        doc = Document(BytesIO(file_bytes))  # Reuse the bytes
        return '\n'.join([p.text for p in doc.paragraphs])

    elif ext == '.pdf':
        reader = PdfReader(BytesIO(file_bytes))  # Reuse the bytes
        text = ''
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + '\n'
        return text

    else:
        raise ValueError("Unsupported file type. Please upload .txt, .docx, or .pdf")
