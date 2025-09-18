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


# import os
# from io import BytesIO
# from docx import Document
# from PyPDF2 import PdfReader
# from zipfile import BadZipFile

# def extract_text_from_file(uploaded_dict):
#     """
#     Extracts text from a single uploaded file dictionary and performs robust cleaning.

#     This version is designed to handle common formatting issues like extra
#     line breaks and empty paragraphs, ensuring a clean output for the
#     chunking process.

#     Args:
#         uploaded_dict (dict): A dictionary from a Streamlit file_uploader
#                               containing filename and content.

#     Returns:
#         tuple: A tuple containing the extracted text and an error message (if any).
#                Text will be an empty string if there's an error.
#                Error message will be an empty string if there's no error.
#     """
#     filename = next(iter(uploaded_dict))
#     content = uploaded_dict[filename]
#     ext = os.path.splitext(filename)[1].lower()

#     text = ""
#     error_message = ""

#     if ext == '.txt':
#         try:
#             text = content.decode('utf-8')
#         except UnicodeDecodeError:
#             error_message = "Error: Could not decode text file. It may be corrupted or use a different encoding."

#     elif ext == '.docx':
#         try:
#             # Use BytesIO to handle the file in memory without saving to disk
#             doc = Document(BytesIO(content))
            
#             # --- Aggressive Text Cleaning Logic ---
#             # We now build a list of non-empty, stripped paragraphs directly
#             cleaned_paragraphs = []
#             for p in doc.paragraphs:
#                 stripped_text = p.text.strip()
#                 if stripped_text:
#                     cleaned_paragraphs.append(stripped_text)
            
#             # Join the cleaned paragraphs with a single newline
#             text = '\n'.join(cleaned_paragraphs)

#         except BadZipFile as e:
#             # This handles the specific case of a corrupted DOCX file
#             error_message = f"Error: The uploaded Word document appears to be corrupted and cannot be read. Details: {e}"
#         except Exception as e:
#             # Catch any other potential errors during docx parsing
#             error_message = f"Error processing .docx file due to an unexpected issue. Details: {e}"

#     elif ext == '.pdf':
#         try:
#             reader = PdfReader(BytesIO(content))
#             for page in reader.pages:
#                 page_text = page.extract_text()
#                 if page_text:
#                     text += page_text + '\n'
#         except Exception as e:
#             error_message = f"Error: Could not process the uploaded PDF document. Details: {e}"

#     else:
#         error_message = "Error: Unsupported file type. Please upload a .txt, .docx, or .pdf file."

#     # Return the cleaned text or the error message
#     if error_message:
#         return ("", error_message)
#     else:
#         return (text, "")
   
