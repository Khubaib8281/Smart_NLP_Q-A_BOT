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
from zipfile import BadZipFile

def extract_text_from_file(uploaded_dict):
    """
    Extracts text from a single uploaded file dictionary and cleans it.

    Args:
        uploaded_dict (dict): A dictionary from a Streamlit file_uploader
                              containing filename and content.

    Returns:
        str: The extracted and cleaned text or an error message if processing fails.
    """
    filename = next(iter(uploaded_dict))
    content = uploaded_dict[filename]
    ext = os.path.splitext(filename)[1].lower()

    text = ""
    if ext == '.txt':
        try:
            text = content.decode('utf-8')
        except UnicodeDecodeError:
            return "Error: Could not decode text file with UTF-8. It may be corrupted or use a different encoding."

    elif ext == '.docx':
        try:
            # Use BytesIO to handle the file in memory without saving to disk
            doc = Document(BytesIO(content))
            # The paragraphs include empty lines, which we will handle below
            text = '\n'.join([p.text for p in doc.paragraphs])
        except BadZipFile as e:
            print(f"Error: BadZipFile when processing .docx file - {e}")
            return "Error: The uploaded Word document appears to be corrupted and cannot be read."
        except Exception as e:
            print(f"Error processing .docx file: {e}")
            return "Error: Could not process the uploaded Word document due to an unexpected issue."

    elif ext == '.pdf':
        try:
            reader = PdfReader(BytesIO(content))
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + '\n'
        except Exception as e:
            print(f"Error processing .pdf file: {e}")
            return "Error: Could not process the uploaded PDF document."

    else:
        return "Error: Unsupported file type. Please upload a .txt, .docx, or .pdf file."

    # --- New Text Cleaning Logic ---
    # This addresses the "not reading all text" issue caused by empty lines
    cleaned_lines = []
    for line in text.split('\n'):
        # Strip leading/trailing whitespace and check if the line is not empty
        stripped_line = line.strip()
        if stripped_line:
            cleaned_lines.append(stripped_line)
            
    # Join the cleaned lines back into a single string
    cleaned_text = '\n'.join(cleaned_lines)

    return cleaned_text
   
