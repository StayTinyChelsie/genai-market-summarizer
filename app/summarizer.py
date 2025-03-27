
import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def summarize_text(text, model="gpt-4"):
    prompt = f"Summarize this financial report with key points and market relevance:\n\n{text}"
    
    response = openai.ChatCompletion.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5,
        max_tokens=600
    )
    
    return response['choices'][0]['message']['content'].strip()
