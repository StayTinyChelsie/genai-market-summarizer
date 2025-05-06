from openai_client import client

def generate_case_study(topic_or_company):
    """Generate a simulated business case study."""
    prompt = (
        f"Generate a business case study for: {topic_or_company}\n\n"
        "Structure it as:\n"
        "- Executive Summary\n"
        "- Business Problem\n"
        "- Market/Industry Context\n"
        "- Key Data Points\n"
        "- Strategic Alternatives\n"
        "- Recommendation\n\n"
        "Make it concise but realistic, like a case used in a business school."
    )

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a Harvard-style business case writer."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.6,
        max_tokens=800
    )

    return response.choices[0].message.content
