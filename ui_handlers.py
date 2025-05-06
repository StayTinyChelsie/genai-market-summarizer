# ui_handlers.py
import os
import fitz  # PyMuPDF
import streamlit as st
import pandas as pd
from Nyt_fetcher import fetch_nyt_articles
from fetch_dataset import fetch_yfinance_multiindex_data
from summarizer import summarize_text
from summary import generate_market_overview_and_insights, generate_comparison_summary
from fetch_dataset import fetch_valuation_metrics, fetch_sector_info, compare_vs_benchmark
from chart_logic import generate_all_charts_for_multiple_tickers
from presentation import generate_presentation
from exporter import export_excel_summary, export_to_google_sheets
from summary import generate_ai_insight

def extract_text_from_pdf(uploaded_file):
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    return "\n".join([page.get_text() for page in doc])

def handle_input_modes(input_mode):
    text, df, tickers, presentation_title = "", pd.DataFrame(), [], "Financial Analysis Report"

    if input_mode == "Upload PDF":
        uploaded_file = st.file_uploader("Upload a PDF Report", type=["pdf"])
        if uploaded_file:
            text = extract_text_from_pdf(uploaded_file)
            presentation_title = uploaded_file.name.replace("_", " ").title()

    elif input_mode == "Paste Text":
        text = st.text_area("Paste financial text below")
        presentation_title = "Pasted Financial Insight"

    elif input_mode == "Use Preinstalled Dataset":
        dataset_paths = {
            "World Bank GDP": "data/worldbank_gdp.csv",
            "Quandl AAPL": "data/quandl_aapl.csv",
            "VIX Index": "data/vix_index.csv"
        }
        option = st.selectbox("Choose dataset", list(dataset_paths.keys()))
        if option in dataset_paths and os.path.exists(dataset_paths[option]):
            df = pd.read_csv(dataset_paths[option])
            text = df.to_string(index=False)
            tickers = [option.split()[-1]]
            presentation_title = f"{option} Summary"
            st.code(text[:1000], language='text')

    elif input_mode == "Live Ticker Lookup":
        custom_ticker = st.text_input("Enter stock ticker(s) (e.g., TSLA or TSLA, AAPL):")
        if custom_ticker:
            df = fetch_yfinance_multiindex_data(custom_ticker)
            if df is not None and not df.empty:
                tickers = df.columns.get_level_values(1).unique().tolist()
                text = df.to_csv(index=True)
                presentation_title = f"Live Market Summary: {', '.join(tickers)}"
            else:
                st.error("No data returned. Please check your ticker symbols.")

    elif input_mode == "New York Times":
        nyt_ticker = st.text_input("Enter topic or ticker for NYT search:")
        if nyt_ticker:
            with st.spinner("Searching New York Times..."):
                try:
                    nyt_articles = fetch_nyt_articles(nyt_ticker)
                except Exception as e:
                    st.error(f"Error fetching NYT articles: {e}")
                    return text, df, tickers, presentation_title
            if nyt_articles:
                for article in nyt_articles:
                    st.markdown(f"[{article['title']}]({article['url']}) — *{article['date']}*")
            else:
                st.info("No articles found.")
            st.stop()

    return text, df, tickers, presentation_title
