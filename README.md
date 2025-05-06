# GenAI Market Summarizer 🧠📊  
*Powered by FinSight*

## 🚀 Overview

**GenAI Market Summarizer** is an AI-powered financial app that streamlines market research, portfolio strategy, and financial reporting. Built using Python, Streamlit, OpenAI, and yFinance, it helps users—students, founders, and investors—analyze financial data, generate visual reports, and make smarter market decisions.

## 🔑 Key Features

- **Live Financial Data Fetching** (yFinance, NYT, FRED, World Bank)
- **Multi-Ticker Comparison** with AI-generated summaries
- **Portfolio Tools:** Monte Carlo Simulation & Efficient Frontier Analysis
- **Smart Chart Generation** (up to 80 chart types!)
- **Export Options:** PowerPoint, Excel, PDF, and Google Sheets
- **Preloaded & Uploadable Datasets** (e.g., SEC filings, cryptocurrency, treasury yields)
- **NYT Financial Article Summarizer**
- **Hedge Fund Strategy Assistant** and AI-driven investment tips

## 🧩 App Structure

- `main.py` — Core Streamlit app interface
- `chart_logic.py` — Handles chart generation and formatting
- `summary.py` — Summarizes text and financial insights using OpenAI
- `fetch_dataset.py` — Pulls live and static datasets (yFinance, FRED, World Bank, etc.)
- `exporter.py` — Exports to Excel, Google Sheets, PowerPoint, PDF
- `presentation.py` — Builds AI-powered investor slides
- `ui_handlers.py` — Manages dynamic input modes and UI flows

## 🖥️ How to Run the App

```bash
# Clone the repository
git clone https://github.com/your-username/GenAI-Market-Summarizer.git
cd GenAI-Market-Summarizer

# Install dependencies
pip install -r requirements.txt

# Run the Streamlit app
streamlit run main.py
