from io import BytesIO
from docx import Document
from PyPDF2 import PdfReader
import os

def extract_text_from_file(uploaded_file):
    if not uploaded_file:
        raise ValueError("No file uploaded")

    filename = uploaded_file.name
    ext = os.path.splitext(filename)[1].lower()

    file_content = uploaded_file.read()  # read once
    file_buffer = BytesIO(file_content)  # wrap in BytesIO

    if ext == '.txt':
        return file_content.decode('utf-8')

    elif ext == '.docx':
        doc = Document(file_buffer)
        return '\n'.join([p.text for p in doc.paragraphs])

    elif ext == '.pdf':
        reader = PdfReader(file_buffer)
        text = ''
        for page in reader.pages:
            content = page.extract_text()
            if content:
                text += content + '\n'
        return text

    else:
        raise ValueError("Unsupported file type. Please upload .txt, .docx, or .pdf")
