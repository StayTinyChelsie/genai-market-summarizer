# main.py

import streamlit as st
import pandas as pd
from dotenv import load_dotenv

from FinSight import (
    init_finsight_session,
    upload_and_summarize_file,
    handle_chat,
    show_action_buttons,
    generate_portfolio_strategy,
    risk_profile_selector
)
from brainstorm_idea_generator import brainstorm_ideas
from pitch_generator import generate_pitch
from portfolio_builder_generator import build_portfolio
from openai_client import client
from presentation import generate_presentation
from ui_handlers import handle_input_modes
from summarizer import summarize_text
from fetch_dataset import fetch_yfinance_multiindex_data
from chart_logic import generate_all_charts_for_multiple_tickers
from exporter import (
    export_excel_summary,
    download_powerpoint_btn,
    download_excel_btn,
)
from summary import (
    generate_market_overview_and_insights,
    generate_comparison_summary,
    generate_ai_insight,
)
from fetch_dataset import fetch_valuation_metrics, fetch_sector_info, compare_vs_benchmark
from Nyt_fetcher import fetch_nyt_articles
load_dotenv()
st.set_page_config(page_title="GenAI Market Summarizer", page_icon="📊", layout="wide")

def main():
    selected_category = st.sidebar.selectbox("Choose Tool Category", [
            "🏠 Home",
            "Market Tools",
            "Startup & Strategy",
            "Portfolio Analysis",
            "Document Summarizers",
            "GPT Chat & Assist"
        ])

    if selected_category == "🏠 Home":
        input_mode = "Home"
    elif selected_category == "Market Tools":
        input_mode = st.sidebar.radio("Choose Tool", [
            "Live Ticker Lookup",
            "Compare Tickers",
            "Sector Performance Tracker",
            "Smart Screener",
            "Earnings Summary"
        ])
    elif selected_category == "Startup & Strategy":
        input_mode = st.sidebar.radio("Choose Tool", [
            "Generate Pitch Deck",
            "Business Plan Generator",
            "SWOT Analysis Generator",
            "Case Study Simulator",
            "Brainstorm Ideas"
        ])
    elif selected_category == "Portfolio Analysis":
        input_mode = st.sidebar.radio("Choose Tool", [
            "Build Portfolio Strategy",
            "Auto-Rebalance Engine",
            "Monte Carlo Simulation",
            "Risk Analyzer"
        ])
    elif selected_category == "Document Summarizers":
        input_mode = st.sidebar.radio("Choose Tool", [
            "Upload PDF",
            "Paste Text",
            "Use Preinstalled Dataset",
            "New York Times",
            "SEC Filing Summarizer"
        ])
    elif selected_category == "GPT Chat & Assist":
        input_mode = st.sidebar.radio("Choose Tool", [
            "Chat with FinSight",
            "Hedge Fund Assistant"
        ])
        
    if input_mode == "Home":
        st.title("📊 Welcome to GenAI Market Summarizer")
        st.markdown("### 🤖 Powered by FinSight – Your AI Copilot for Finance and Startups")

        st.markdown("""
        GenAI Market Summarizer is your all-in-one platform for:
        - 📈 Market and ticker analysis
        - 🧮 Portfolio simulation, rebalancing, and risk tools
        - 💼 Startup pitch support and financial modeling
        - 🧠 SWOT, case studies, and business strategy generation
        - 📄 Smart document summarization (PDFs, filings, earnings)
        - 💬 FinSight: Your AI assistant for anything financial
        """)

        st.markdown("---")
        st.subheader("⚡ Quick Start")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("📝 Write a Business Plan"):
                st.session_state["selected_category"] = "Startup & Strategy"
                st.session_state["input_mode"] = "Business Plan Generator"
            if st.button("📊 Compare Tickers"):
                st.session_state["selected_category"] = "Market Tools"
                st.session_state["input_mode"] = "Compare Tickers"
        with col2:
            if st.button("🧠 Generate SWOT"):
                st.session_state["selected_category"] = "Startup & Strategy"
                st.session_state["input_mode"] = "SWOT Analysis Generator"
            if st.button("💬 Chat with FinSight"):
                st.session_state["selected_category"] = "GPT Chat & Assist"
                st.session_state["input_mode"] = "Chat with FinSight"

        st.markdown("---")
        st.subheader("🆕 What’s New This Week")

        st.info("""
        - ✅ Auto-Rebalance Engine added
        - ✅ Case Study Simulator live
        - ✅ Smart Screener + SWOT Assistant launched
        - ✅ New Home Screen + Tool Categories
        """)

        st.markdown("---")
        st.subheader("🧭 Tool Categories Overview")

        st.markdown("""
        - **📈 Market Tools**: Ticker lookup, earnings summaries, smart screening
        - **💼 Startup & Strategy**: Pitch decks, business plans, SWOTs
        - **📊 Portfolio Tools**: Rebalancing, simulation, performance
        - **📄 Document Summarizers**: SEC filings, PDFs, market news
        - **💬 GPT Chat Assistants**: FinSight, hedge fund ideas, brainstorming
        """)

    #return  # Exit main here to skip rendering other tools






    if input_mode == "Compare Tickers":
        compare_input = st.text_input("Enter tickers to compare (comma-separated):")

        if compare_input:
            tickers_list = [t.strip().upper() for t in compare_input.split(",")]
            ticker = ",".join(tickers_list)
            df = fetch_yfinance_multiindex_data(ticker)

            if df is not None and not df.empty:
                text = df.to_csv(index=True)[:1000]

                benchmark_option = st.selectbox("Choose benchmark", [
                    "^GSPC (S&P 500)", "^IXIC (NASDAQ)", "^DJI (Dow Jones)", "SPY (ETF)", "QQQ (ETF)"
                ])
                benchmark_symbol = benchmark_option.split(" ")[0]

                selected_charts = []
                with st.expander("Choose Chart Types"):
                    chart_categories = {
                        "Trend": ["Line", "Area", "Candlestick"],
                        "Volatility": ["Box", "Violin"],
                        "Distribution": ["Histogram", "Pie"],
                        "Relationship": ["Scatter"],
                        "Correlation": ["Heatmap"]
                    }
                    for category, options in chart_categories.items():
                        chosen = st.multiselect(
                            f"{category} Charts",
                            options,
                            default=["Line"] if category == "Trend" else [],
                            key=f"compare_{category}_charts_multiselect"
                        )
                        selected_charts.extend([c.lower() for c in chosen])

                if st.button("📊 Generate Comparison Report"):
                    st.session_state["compare_tickers_report_ready"] = True
                    st.session_state["compare_tickers_data"] = {
                        "tickers_list": tickers_list,
                        "ticker": ticker,
                        "df": df,
                        "text": text,
                        "benchmark_symbol": benchmark_symbol,
                        "selected_charts": selected_charts,
                        "presentation_title": "Comparison Report"
                    }

        if st.session_state.get("compare_tickers_report_ready"):
            data = st.session_state.get("compare_tickers_data", {})

            with st.spinner("Generating Comparison Report..."):
                tickers_list = data.get("tickers_list", [])
                ticker = data.get("ticker", "")
                df = data.get("df", pd.DataFrame())
                text = data.get("text", "")
                benchmark_symbol = data.get("benchmark_symbol", "^GSPC")
                selected_charts = data.get("selected_charts", [])
                presentation_title = data.get("presentation_title", "Comparison Report")

                if not tickers_list or df.empty:
                    st.error("Missing data. Please input tickers and generate again.")
                else:
                    ai_summary = summarize_text(text)
                    market_overview_text, insights_list = generate_market_overview_and_insights(df, tickers_list)
                    comparison_insight = generate_comparison_summary(tickers_list, df)
                    valuation_insights = fetch_valuation_metrics(tickers_list)
                    sector_insights = fetch_sector_info(tickers_list)
                    benchmark_insights = compare_vs_benchmark(tickers_list, df, benchmark=benchmark_symbol)

            chart_paths= generate_all_charts_for_multiple_tickers(
                ",".join(tickers_list), df, selected_charts, show_interactive=True
            )

            ppt_path = generate_presentation(
                title=presentation_title,
                summary_text=ai_summary,
                charts=chart_paths,
                market_overview=market_overview_text,
                key_insights=(insights_list +
                              ["", "📊 Sector Overview"] + sector_insights +
                              ["", "⚔️ Comparison Summary"] + [comparison_insight] +
                              ["", "📉 Benchmark Comparison vs " + benchmark_symbol] + benchmark_insights +
                              ["", "💰 Valuation Metrics"] + valuation_insights)
            )

            st.success("✅ Comparison Report Generated!")
            st.markdown("### 📊 Generated Charts")

            st.download_button(
                        "⬇️ Download PowerPoint",
                        data=open(ppt_path, "rb"),
                        file_name="comparison_report.pptx",
                        mime="application/vnd.openxmlformats-officedocument.presentationml.presentation"
                    )

            st.download_button(
                        "📈 Download Excel Report",
                        data=export_excel_summary(df).getvalue(),
                        file_name="comparison_data.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )

            if st.button("🔄 Reset Comparison Report"):
                        st.session_state["compare_tickers_report_ready"] = False
                        st.session_state["compare_tickers_data"] = {}

    elif input_mode == "Hedge Fund Assistant":
        st.header("🏦 Hedge Fund Strategy Assistant")
        st.markdown("### 🤖 Portfolio Guidance Generator")

        risk_preference = st.radio("Risk Tolerance", ["Low", "Medium", "High"], index=1)
        sector_focus = st.multiselect("Preferred Sectors", ["Tech", "Healthcare", "Finance", "Energy", "Consumer", "Crypto"])
        num_recommendations = st.slider("Number of Ticker Recommendations", 3, 10, 5)

        if st.button("Generate Portfolio Recommendations"):
            st.session_state["hedge_recommendations_ready"] = True

        if st.session_state.get("hedge_recommendations_ready"):
            prompt = f"Generate {num_recommendations} stock or crypto tickers that a hedge fund could include based on a {risk_preference.lower()} risk tolerance and focus on these sectors: {', '.join(sector_focus)}. Provide a reason for each."
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.6,
                max_tokens=400
            )
            st.markdown("### 📈 Suggested Portfolio")
            st.markdown(response.choices[0].message.content.strip())

            if st.button("🔄 Reset Portfolio Recommendations"):
                st.session_state["hedge_recommendations_ready"] = False

    elif input_mode == "Chat with FinSight":
        st.title("💬 Chat with FinSight")

        init_finsight_session()
        uploaded_file = upload_and_summarize_file()
        selected_risk_profile = risk_profile_selector()

        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        bot_reply = handle_chat()
        show_action_buttons(uploaded_file, bot_reply)

        if st.session_state.get("next_action") == "build_strategy":
            strategy = generate_portfolio_strategy(summary_text=bot_reply, risk_profile=selected_risk_profile)
            st.markdown("### 🧠 Portfolio Strategy Recommendation:")
            st.markdown(strategy)
            st.session_state["strategy_text"] = strategy

    # ✅ NEW OUTER ELIFs BELOW

    elif input_mode == "Generate Pitch Deck":
        st.header("🎤 Generate a Startup Pitch")
        prompt = st.text_input("Describe your idea or business concept:")
        style = st.selectbox("Select pitch style", ["standard", "elevator", "formal"])

        if st.button("Generate Pitch"):
            pitch = generate_pitch(prompt, style)
            st.markdown("### Generated Pitch")
            st.write(pitch)

    elif input_mode == "Brainstorm Ideas":
        st.header("💡 Brainstorm Ideas")
        topic = st.text_input("Enter a topic to brainstorm:")
        number_of_ideas = st.selectbox("Number of ideas", [5, 10, 15, 20])
        creativity = st.selectbox("Creativity Level", ["serious", "normal", "wild"])

        if st.button("Brainstorm"):
            ideas = brainstorm_ideas(topic, number_of_ideas, creativity)
            st.markdown("### Brainstormed Ideas")
            st.write(ideas)

    elif input_mode == "Build Portfolio Strategy":
        st.header("📈 Build a Portfolio")
        goal = st.selectbox("Investment Goal", ["growth", "income", "balanced"])
        risk = st.selectbox("Risk Level", ["low", "medium", "high"])

        if st.button("Build Portfolio"):
            portfolio = build_portfolio(goal, risk)
            st.markdown("### Suggested Portfolio")
            for stock, details in portfolio.items():
                st.write(f"• **{stock}** → {details}")


                        
    elif input_mode == "Fetch New York Times Articles":
                    topic = st.text_input("Enter a topic to fetch NYT articles about:")
                    if st.button("Fetch Articles"):
                        articles = fetch_nyt_articles(topic)
                        st.write(articles)
    elif input_mode == "Risk Analyzer":
            from risk_analyzer import run_risk_analysis
            st.header("📉 Sharpe & Beta Analyzer")

            ticker = st.text_input("Enter a stock ticker (e.g. AAPL):")
            if st.button("Analyze Risk") and ticker:
                sharpe, beta = run_risk_analysis(ticker)
                st.write(f"**Sharpe Ratio**: {sharpe}")
                st.write(f"**Beta (vs S&P 500)**: {beta}")

    elif input_mode == "Sector Performance Tracker":
        from sector_tracker import fetch_sector_performance
        st.header("📊 Sector Performance Tracker")
        period = st.selectbox("Select time period", ["1mo", "3mo", "6mo", "1y"], index=1)
        data = fetch_sector_performance(period)
        st.bar_chart(data)
        best = data.idxmax()
        st.success(f"Best sector over {period}: **{best}** ({data[best]}%)")
    elif input_mode == "Earnings Summary":
        from earnings_summary import generate_ai_earnings_summary
        st.header("🧠 Earnings Summary Generator")
        ticker = st.text_input("Enter a stock ticker (e.g. MSFT):")
        if st.button("Summarize Earnings") and ticker:
            summary = generate_ai_earnings_summary(ticker)
            st.markdown("### AI-Generated Summary")
            st.write(summary)
    elif input_mode == "Monte Carlo Simulation":
        from monte_carlo_simulator import simulate_monte_carlo, plot_simulation
        st.header("🧮 Monte Carlo Portfolio Simulator")

        st.markdown("Enter simulation parameters below:")

        with st.form("monte_carlo_form"):
            tickers_input = st.text_input("Enter tickers (comma-separated)", key="mc_ticker_input")
            years = st.slider("Years to Simulate", 1, 30, 10, key="mc_years")
            expected_return = st.slider("Expected Annual Return (%)", 0, 20, 7, key="mc_return") / 100
            volatility = st.slider("Annual Volatility (%)", 5, 50, 15, key="mc_volatility") / 100
            simulations = st.slider("Number of Simulations", 100, 2000, 1000, key="mc_simulations")
            submitted = st.form_submit_button("Run Simulation")

        if submitted and tickers_input:
            tickers = [t.strip().upper() for t in tickers_input.split(",")]
            weights = [1 / len(tickers)] * len(tickers)

            df = simulate_monte_carlo(
                tickers, weights, years=years,
                simulations=simulations,
                expected_return=expected_return,
                volatility=volatility
            )
            fig = plot_simulation(df)
            st.pyplot(fig)

            final_values = df.iloc[-1]
            st.success(f"Projected mean portfolio value after {years} years: ${round(final_values.mean(), 2):,}")
            st.write(f"90% Confidence Interval: ${round(final_values.quantile(0.05), 2):,} - ${round(final_values.quantile(0.95), 2):,}")

    elif input_mode == "SEC Filing Summarizer":
            from sec_summarizer import extract_text_from_pdf, summarize_sec_filing
            st.header("📑 SEC Filing Summarizer")

            uploaded_file = st.file_uploader("Upload a 10-K, 8-K, or other SEC filing (PDF only)", type=["pdf"])
            focus_area = st.selectbox(
                "Choose a focus for summarization:",
                ["full", "risks", "strategy", "financials"],
                format_func=lambda x: {
                    "full": "Full Summary",
                    "risks": "Risk Factors",
                    "strategy": "Business Strategy",
                    "financials": "Financial Performance"
                }[x]
            )

            if uploaded_file and st.button("Summarize Filing"):
                with st.spinner("Extracting and analyzing filing..."):
                    text = extract_text_from_pdf(uploaded_file)
                    summary = summarize_sec_filing(text, focus=focus_area)
                    st.subheader("🧠 AI-Generated Summary")
                    st.write(summary)
    elif input_mode == "Business Plan Generator":
        from business_plan_generator import generate_business_plan
        st.header("📝 AI Business Plan Writer")

        idea = st.text_input("Describe your business idea:")
        target_market = st.text_input("Who is your target market?")
        revenue_model = st.text_input("What is your revenue model?")
        funding_goal = st.text_input("Optional: Funding goal ($) (leave blank if none)")

        if st.button("Generate Business Plan"):
            if idea and target_market and revenue_model:
                plan = generate_business_plan(idea, target_market, revenue_model, funding_goal)
                st.subheader("Generated Business Plan")
                st.write(plan)
        else:
            st.error("Please fill out at least idea, target market, and revenue model.")
    elif input_mode == "Smart Screener":
        from smart_screener import fetch_candidate_stocks, screen_stocks_with_gpt
        st.header("🔍 AI Smart Stock Screener")

        user_prompt = st.text_input("Describe what you're looking for in stocks (e.g., 'cheap tech stocks under $100')")

        if st.button("Screen Stocks") and user_prompt:
            with st.spinner("Fetching and screening..."):
                df = fetch_candidate_stocks()
                result = screen_stocks_with_gpt(user_prompt, df)
                st.subheader("🧠 GPT-Filtered Stocks")
                st.write(result)

    elif input_mode == "SWOT Analysis Generator":
        from swot_analysis import generate_swot_analysis
        st.header("🧠 SWOT Analysis Generator")

        idea = st.text_input("Enter your business, product, or startup idea:")

        if st.button("Generate SWOT"):
            if idea:
                result = generate_swot_analysis(idea)
                st.subheader("SWOT Analysis")
                st.write(result)
        else:
            st.warning("Please describe your business or product idea.")
    elif input_mode == "Case Study Simulator":
        from case_study_simulator import generate_case_study
        st.header("📚 Business Case Study Simulator")

        topic = st.text_input("Enter a company, product, or business scenario:")

        if st.button("Generate Case Study"):
            if topic:
                result = generate_case_study(topic)
                st.subheader("📖 Case Study")
                st.write(result)
        else:
            st.warning("Please enter a topic or company to simulate a case.")
    elif input_mode == "Auto-Rebalance Engine":
        from auto_rebalance_engine import fetch_portfolio_prices, calculate_current_allocation, generate_rebalance_plan
        st.header("🧮 Auto-Rebalance Engine")

        tickers_input = st.text_input("Enter tickers (comma-separated, e.g., AAPL, MSFT, AMZN):")
        weights_input = st.text_input("Enter target weights (comma-separated %, e.g., 40,30,30):")

        if st.button("Rebalance"):
            if tickers_input and weights_input:
                tickers = [t.strip().upper() for t in tickers_input.split(",")]
                raw_weights = [float(w.strip()) for w in weights_input.split(",")]
                total_weight = sum(raw_weights)
                if len(tickers) != len(raw_weights) or total_weight == 0:
                    st.error("Mismatch in number of tickers and weights or invalid input.")
            else:
                weights = [w / total_weight for w in raw_weights]  # Normalize to sum = 1
                prices = fetch_portfolio_prices(tickers)
                current_values, current_alloc = calculate_current_allocation(tickers, weights, prices)
                portfolio_value = sum(current_values)
                df = generate_rebalance_plan(tickers, weights, current_alloc, portfolio_value)

                st.subheader("📊 Rebalance Recommendations")
                st.dataframe(df.set_index("Ticker"))
                st.success(f"Total Portfolio Value: ${portfolio_value:,.2f}")
        else:
            st.warning("Please enter both tickers and weights.")


    else:
        # Handle all other modes (Upload PDF, Live Ticker Lookup, Paste Text, New York Times, Use Preinstalled)
        text, df, tickers, presentation_title = handle_input_modes(input_mode)

        if st.button("Summarize"):
            if not text.strip():
                st.error("Please provide valid input.")
            else:
                st.session_state["summarize_triggered"] = True

        if st.session_state.get("summarize_triggered"):
            with st.spinner("Summarizing and analyzing..."):
                ai_summary = summarize_text(text)
                st.subheader("Summary & Sentiment")
                st.markdown(ai_summary)

                if df is not None and not df.empty:
                    insight = generate_ai_insight(tickers[0], df)
                    if insight:
                        st.markdown(f"**AI Insight:** {insight}")
                        st.write("DataFrame shape:", df.shape)

                    selected_charts = []
                    chart_categories = {
                        "Trend": ["Line", "Area", "Candlestick"],
                        "Volatility": ["Box", "Violin"],
                        "Distribution": ["Histogram", "Pie"],
                        "Relationship": ["Scatter"],
                        "Correlation": ["Heatmap"]
                    }
                    with st.expander("Choose Chart Types by Category"):
                        for category, options in chart_categories.items():
                            chosen = st.multiselect(
                                f"{category} Charts", options,
                                default=["Line"] if category == "Trend" else [],
                                key=f"general_{category}_charts_multiselect"
                            )
                            selected_charts.extend([c.lower() for c in chosen])

                    if selected_charts:
                        chart_paths = generate_all_charts_for_multiple_tickers(
                            ",".join(tickers), df, selected_charts, show_interactive=True
                        )
                        st.success("Charts generated and displayed.")

                        ppt_path = generate_presentation(
                            title=presentation_title,
                            summary_text=ai_summary,
                            charts=chart_paths,
                            market_overview=generate_market_overview_and_insights(df, tickers)[0],
                            key_insights=generate_ai_insight(tickers[0], df)
                        )

                        download_powerpoint_btn(ppt_path)
                        excel_buffer = export_excel_summary(df)
                        download_excel_btn(excel_buffer)
                        
               
if __name__ == "__main__":
    main()
