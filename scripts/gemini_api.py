def generate_answer_from_chunks(chunks, question):
    import os
    import google.generativeai as genai

    genai.configure(api_key = os.getenv"GEMINI_API_KEY")
    gemini_model = genai.GenerativeModel("gemini-2.0-flash")
    context = "\n\n".join(chunks)
    prompt = f"""Use the context below to answer the question.

Context:
{context}

Question:
{question}

Answer:"""

    response = gemini_model.generate_content(prompt)
    return response.text.strip()