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




import os
from io import BytesIO
from docx import Document
from PyPDF2 import PdfReader
from zipfile import BadZipFile # We need to import the specific error to catch it

def extract_text_from_file(uploaded_dict):
    """
    Extracts text from a single uploaded file dictionary.

    Args:
        uploaded_dict (dict): A dictionary from a Streamlit file_uploader
                              containing filename and content.

    Returns:
        str: The extracted text or an error message if processing fails.
    """
    filename = next(iter(uploaded_dict))
    content = uploaded_dict[filename]
    ext = os.path.splitext(filename)[1].lower()

    if ext == '.txt':
        try:
            return content.decode('utf-8')
        except UnicodeDecodeError:
            return "Error: Could not decode text file with UTF-8. It may be corrupted or use a different encoding."

    elif ext == '.docx':
        try:
            # Use BytesIO to handle the file in memory without saving to disk
            doc = Document(BytesIO(content))
            return '\n'.join([p.text for p in doc.paragraphs])
        except BadZipFile as e:
            # This handles the specific case of a corrupted DOCX file
            print(f"Error: BadZipFile when processing .docx file - {e}")
            return "Error: The uploaded Word document appears to be corrupted and cannot be read."
        except Exception as e:
            # Catch any other potential errors during docx parsing
            print(f"Error processing .docx file: {e}")
            return "Error: Could not process the uploaded Word document due to an unexpected issue."

    elif ext == '.pdf':
        try:
            reader = PdfReader(BytesIO(content))
            text = ''
            for page in reader.pages:
                text += page.extract_text() + '\n'
            return text
        except Exception as e:
            # Catch errors in PDF parsing
            print(f"Error processing .pdf file: {e}")
            return "Error: Could not process the uploaded PDF document."

    else:
        # Handle unsupported file types gracefully
        return "Error: Unsupported file type. Please upload a .txt, .docx, or .pdf file."
