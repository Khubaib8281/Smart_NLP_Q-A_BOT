from io import BytesIO
from docx import Document
from PyPDF2 import PdfReader
import os

def extract_text_from_file(uploaded_file):
    if not uploaded_file or not hasattr(uploaded_file, 'read'):
        raise ValueError("Invalid file uploaded.")

    file_bytes = uploaded_file.read()
    buffer = BytesIO(file_bytes)
    ext = os.path.splitext(uploaded_file.name)[1].lower()

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
