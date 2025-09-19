# def chunk_text(text):
#     import re
#     paragraphs = re.split(r'\n\s*\n', text.strip())
#     chunks = [p.strip().replace('\n', ' ') for p in paragraphs if p.strip()]
#     return chunks

def chunk_text(text: str, chunk_size=1000, overlap=100):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=overlap,
        separators=["\n\n", "\n", ".", " ", ""]
    )
    return splitter.split_text(text)
