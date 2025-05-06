from openai_client import client

def generate_swot_analysis(business_name_or_idea):
    """Generate a SWOT analysis for a business or product idea."""
    prompt = (
        f"Create a SWOT analysis for the following business, product, or startup idea:\n\n"
        f"{business_name_or_idea}\n\n"
        "Return your response with the following structure:\n"
        "- Strengths\n- Weaknesses\n- Opportunities\n- Threats"
    )

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a strategic business advisor creating SWOT analyses."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.5,
        max_tokens=600
    )

    return response.choices[0].message.content
