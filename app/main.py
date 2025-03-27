
import streamlit as st
from app.summarizer import summarize_text
from app.sentiment import classify_sentiment
from app.parser import extract_text_from_pdf
from app.sheets_export import export_to_sheets

st.title("📉 GenAI Market Summarizer")

user_input = ""

option = st.radio("Choose input type:", ("Paste Text", "Upload PDF"))

if option == "Paste Text":
    user_input = st.text_area("Paste financial text:")
elif option == "Upload PDF":
    uploaded_file = st.file_uploader("Upload PDF file", type="pdf")
    if uploaded_file:
        user_input = extract_text_from_pdf(uploaded_file)
        st.success("PDF processed!")

if st.button("Summarize") and user_input:
    with st.spinner("Generating summary..."):
        summary = summarize_text(user_input)
        sentiment = classify_sentiment(summary)

        st.subheader("📝 Summary")
        st.write(summary)
        st.subheader("📊 Sentiment")
        st.write(f"**{sentiment}**")

        if st.button("📤 Export to Google Sheets"):
            export_to_sheets(summary, sentiment)
            st.success("Exported successfully!")
