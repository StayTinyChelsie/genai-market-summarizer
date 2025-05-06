from openai_client import client

def generate_pitch(prompt, style="standard"):
    """Generate a structured business pitch."""
    
    system_prompt = "You are a professional business pitch generator. Create a startup pitch using this format: Problem, Solution, Target Market, Business Model, Competitive Advantage, and Closing Statement."
    
    if style == "elevator":
        system_prompt = "You are creating a very short 30-second elevator pitch."
    elif style == "formal":
        system_prompt = "You are creating a formal venture capital pitch document."
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=600
    )
    
    return response.choices[0].message.content
