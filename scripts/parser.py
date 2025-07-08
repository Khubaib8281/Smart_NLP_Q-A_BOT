from io import BytesIO
from docx import Document
from PyPDF2 import PdfReader
import os


def extract_text_from_file(uploaded_dict):
    filename = next(iter(uploaded_dict))  # Get filename string
    content = uploaded_dict[filename]     # Get binary content
    ext = os.path.splitext(filename)[1].lower()

    if ext == '.txt':
        return content.decode('utf-8')

    elif ext == '.docx':
        doc = Document(BytesIO(content))
        return '\n'.join([p.text for p in doc.paragraphs])

    elif ext == '.pdf':
        reader = PdfReader(BytesIO(content))
        text = ''
        for page in reader.pages:
            text += page.extract_text() + '\n'
        return text

    else:
        raise ValueError("Unsupported file type.")
