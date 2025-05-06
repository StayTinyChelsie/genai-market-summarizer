from openai_client import client

def brainstorm_ideas(topic, number_of_ideas=5, creativity_level="normal"):
    """Brainstorm creative ideas based on a topic with customizable settings."""
    
    creativity = 0.7  # default temperature
    if creativity_level == "wild":
        creativity = 1.0
    elif creativity_level == "serious":
        creativity = 0.3

    prompt = f"Brainstorm {number_of_ideas} creative ideas about: {topic}."

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a creative expert helping people brainstorm ideas."},
            {"role": "user", "content": prompt}
        ],
        temperature=creativity,
        max_tokens=400
    )

    return response.choices[0].message.content
