from openai_client import client

def generate_business_plan(idea, target_market, revenue_model, funding_goal=None):
    """Generates a full business plan from core inputs."""
    funding_text = f"Funding goal: {funding_goal}." if funding_goal else ""
    
    prompt = (
        f"Create a detailed business plan for the following idea:\n\n"
        f"Idea: {idea}\n"
        f"Target Market: {target_market}\n"
        f"Revenue Model: {revenue_model}\n"
        f"{funding_text}\n\n"
        f"Structure it into:\n"
        f"- Executive Summary\n"
        f"- Market Analysis\n"
        f"- Product/Service Offering\n"
        f"- Business Model\n"
        f"- Go-to-Market Strategy\n"
        f"- Financial Overview\n"
        f"- Conclusion"
    )

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a professional business plan writer."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.6,
        max_tokens=1000
    )
    return response.choices[0].message.content
