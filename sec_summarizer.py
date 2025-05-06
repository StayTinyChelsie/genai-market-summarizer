import fitz  # PyMuPDF for PDF parsing
from openai_client import client

def extract_text_from_pdf(uploaded_file):
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    full_text = ""
    for page in doc:
        full_text += page.get_text()
    return full_text.strip()

def summarize_sec_filing(text, focus="full"):
    focus_map = {
        "full": "Summarize the key risks, financial performance, and business strategy.",
        "risks": "Summarize the Risk Factors section only.",
        "strategy": "Summarize the Business Overview and Strategy.",
        "financials": "Summarize key financial performance details only."
    }

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a financial analyst summarizing SEC filings."},
            {"role": "user", "content": f"{focus_map[focus]}\n\n{text[:4000]}"}  # Limit input size
        ],
        temperature=0.5,
        max_tokens=700
    )
    return response.choices[0].message.content
