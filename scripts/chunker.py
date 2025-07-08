# def chunk_text(text, chunk_size = 100):
#     import re
#     words = re.findall(r'\b\w+\b', text)  # Find all words in the text ignoring punctuation and special chars.

#     chunks = []
#     for i in range(0, len(text), chunk_size):
#         chunk = ' '.join(words[i:i+chunk_size])
#         chunks.append(chunk)
#     return chunks


def chunk_text(text):
    import re
    paragraphs = re.split(r'\n\s*\n', text.strip())
    chunks = [p.strip().replace('\n', ' ') for p in paragraphs if p.strip()]
    return chunks