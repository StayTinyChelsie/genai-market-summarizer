from dotenv import load_dotenv
load_dotenv()

from openai_client import client

import os
MAX_CHARS = 4000
def summarize_text(text):
    if len(text) > MAX_CHARS:
        
        text = text[:MAX_CHARS]  # Truncate overly long input

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful financial market summarizer."},
            {"role": "user", "content": text}
        ],
        max_tokens=600,
        temperature=0.7
    )
    return response.choices[0].message.content.strip()





