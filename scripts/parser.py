from io import BytesIO
from docx import Document
from PyPDF2 import PdfReader
import os

def extract_text_from_file(uploaded_file):
    file_bytes = uploaded_file.read()  # Read file once
    ext = os.path.splitext(uploaded_file.name)[1].lower()

    if ext == '.txt':
        return file_bytes.decode('utf-8')

    elif ext == '.docx':
        byte_stream = BytesIO(file_bytes)
        doc = Document(byte_stream)
        return '\n'.join([p.text for p in doc.paragraphs])

    elif ext == '.pdf':
        reader = PdfReader(BytesIO(file_bytes))
        text = ''
        for page in reader.pages:
            content = page.extract_text()
            if content:
                text += content + '\n'
        return text

    else:
        raise ValueError("Unsupported file type. Please upload .txt, .docx, or .pdf")
