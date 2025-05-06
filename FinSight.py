# finsight.py

import streamlit as st
from dotenv import load_dotenv
from openai_client import client
import fitz  # For PDFs
import pandas as pd
from pitch_generator import generate_pitch
from brainstorm_idea_generator import brainstorm_ideas
from portfolio_builder_generator import build_portfolio
from ticker_analyzer import generate_ticker_analysis
# --- System Prompts ---
FINSIGHT_SYSTEM_PROMPT = """
You are FinSight, an AI-powered Financial Advisor designed to assist users with market insights, portfolio strategies, financial report summaries, and hedge fund advice.
Speak professionally, but be friendly and supportive.
Prioritize actionable insights, data-driven suggestions, and financial clarity.
"""

STRATEGY_PROMPT_TEMPLATE = """
You are FinSight, an AI-powered portfolio strategist.
Based on the following report summary, generate a portfolio strategy.
Risk profile: {risk_profile}.
Include:
- Suggested asset classes
- Sectors or industries
- Allocation percentages
- Risk level commentary
Keep it professional but easy to understand.
"""

# --- Initialize FinSight ---
def init_finsight_session():
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "system", "content": FINSIGHT_SYSTEM_PROMPT}]

# --- Upload and Summarize Files ---
def upload_and_summarize_file():
    uploaded_file = st.file_uploader("📄 Upload a financial report (PDF or Excel)", type=["pdf", "xlsx", "xls"])
    
    if uploaded_file:
        if uploaded_file.name.endswith(".pdf"):
            doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
            text = "\n".join(page.get_text() for page in doc)
        elif uploaded_file.name.endswith((".xlsx", ".xls")):
            df = pd.read_excel(uploaded_file)
            text = df.to_string()
        
        st.session_state.messages.append({"role": "user", "content": f"Summarize this report:\n{text[:4000]}"})
        
        return uploaded_file
    return None

# --- Risk Level Selector ---
def risk_profile_selector():
    selected_risk_profile = st.radio(
        "Select your desired risk profile:",
        ["Conservative", "Balanced", "Aggressive"],
        index=1
    )
    return selected_risk_profile

# --- Handle Chat Conversation ---
def handle_chat():
    user_input = st.chat_input("Ask FinSight anything about finance, markets, portfolios...")

    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})

        user_lower = user_input.lower()

        # Detect if user needs special help even without typing 'pitch:' etc
        if "pitch" in user_lower and "help" in user_lower:
            bot_reply = "It sounds like you want help with a pitch! Please switch to 'Generate a Pitch' mode on the sidebar to create one easily. 🎤"

        elif "brainstorm" in user_lower and "help" in user_lower:
            bot_reply = "It sounds like you want to brainstorm ideas! Please switch to 'Brainstorm Ideas' mode on the sidebar to get started. 💡"

        elif "portfolio" in user_lower and "help" in user_lower:
            bot_reply = "It sounds like you want to build a portfolio! Please switch to 'Build a Portfolio' mode on the sidebar. 📈"
        elif user_input.lower().startswith("analyze ticker:"):
            ticker = user_input.split(":")[1].strip().upper()
            reply = generate_ticker_analysis(ticker)
        else:
            # Normal chatbot conversation
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=st.session_state.messages,
                temperature=0.6,
                max_tokens=400
            )
            bot_reply = response.choices[0].message.content

        st.session_state.messages.append({"role": "assistant", "content": bot_reply})
        return bot_reply
    else:
        return None


# --- Show Action Buttons ---
def show_action_buttons(uploaded_file, bot_reply):
    if uploaded_file:
        st.markdown("### 🔥 What would you like to do next?")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("📊 Generate Chart", key="generate_chart"):
                st.session_state["next_action"] = "generate_chart"
        with col2:
            if st.button("📋 Create Report", key="create_report"):
                st.session_state["next_action"] = "create_report"
        with col3:
            if st.button("💼 Build Strategy", key="build_strategy"):
                st.session_state["next_action"] = "build_strategy"

# --- Generate Portfolio Strategy Based on Risk ---
def generate_portfolio_strategy(summary_text, risk_profile="Balanced"):
    strategy_prompt = STRATEGY_PROMPT_TEMPLATE.format(risk_profile=risk_profile)
    conversation = [
        {"role": "system", "content": strategy_prompt},
        {"role": "user", "content": summary_text}
    ]

    response = client.chat.completion.create(
        model="gpt-4o",
        messages=conversation
    )

    strategy_text= response.choices[0].message.content

    return strategy_text
