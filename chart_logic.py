# chart_logic.py
import os
import uuid
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
import streamlit as st
from summary import generate_ai_insight

def save_plotly_figure(fig, path):
    fig.write_image(path, format="png")

def generate_all_charts(ticker, data, chart_types=None, output_dir="data", show_interactive=True, save_files=False):
    charts = []
    figures = []
    os.makedirs(output_dir, exist_ok=True)
    chart_types = [c.strip().lower() for c in (chart_types or [])]

    if not pd.api.types.is_datetime64_any_dtype(data.index):
        data.index = pd.to_datetime(data.index)

    chart_funcs = {
        "line": lambda: px.line(data, x=data.index, y="Close", title=f"{ticker} Line Chart") if "Close" in data.columns else None,
        "candlestick": lambda: go.Figure(data=[go.Candlestick(x=data.index, open=data["Open"], high=data["High"], low=data["Low"], close=data["Close"])]) if set(["Open", "High", "Low", "Close"]).issubset(data.columns) else None,
        "scatter": lambda: px.scatter(data, x=data.index, y="Close", title=f"{ticker} Scatter Chart") if "Close" in data.columns else None,
        "histogram": lambda: px.histogram(data, x="Close", title=f"{ticker} Histogram") if "Close" in data.columns else None,
        "box": lambda: px.box(data, y="Close", title=f"{ticker} Box Plot") if "Close" in data.columns else None,
        "heatmap": lambda: px.imshow(data.corr(), title=f"{ticker} Heatmap") if not data.empty else None,
        "area": lambda: px.area(data, x=data.index, y="Close", title=f"{ticker} Area Chart") if "Close" in data.columns else None,
        "bar": lambda: px.bar(data, x=data.index, y="Volume", title=f"{ticker} Bar Chart") if "Volume" in data.columns else None,
        "violin": lambda: px.violin(data, y="Close", title=f"{ticker} Violin Plot") if "Close" in data.columns else None,
        "pie": lambda: px.pie(data.head(10), values="Volume", names=data.head(10).index.astype(str), title=f"{ticker} Pie Chart") if "Volume" in data.columns else None,
        "funnel": lambda: px.funnel(data, x=data.index, y="Close", title=f"{ticker} Funnel Chart") if "Close" in data.columns else None,
        "sunburst": lambda: None,
    }

    for chart_type, chart_func in chart_funcs.items():
        if chart_type in chart_types:
            st.write(f"🔍 [Chart Generation] Trying to generate {chart_type} chart for {ticker}")
            try:
                fig = chart_func()
                if fig is not None:
                    figures.append((fig, ticker, chart_type))

                    if save_files:
                        path = f"{output_dir}/{ticker}_{chart_type}_chart.png"
                        save_plotly_figure(fig, path)
                        charts.append(path)
                else:
                    st.warning(f"⚠️ [Chart Generation] {chart_type} chart returned None for {ticker}")
            except Exception as e:
                st.warning(f"⚠️ [Chart Generation] Failed to generate {chart_type} chart for {ticker}: {e}")

    return charts, figures



def generate_all_charts_for_multiple_tickers(ticker_str, df, selected_charts, show_interactive=True, save_files=False):
    st.write("🔍 [Charts] Starting chart generation for multiple tickers...")
    tickers = [t.strip().upper() for t in ticker_str.split(",")]
    all_chart_paths = []
    all_figures = []

    for t in tickers:
        st.write(f"📊 [Charts] Processing: {t}")
        try:
            if t not in df.columns.get_level_values(1).unique():
                st.warning(f"⚠️ No data found for ticker: {t}")
                continue

            st.write(f"📈 [Charts] Preparing data slice for: {t}")
            sliced_data = df.xs(t, axis=1, level=1)  # ✅ Proper slicing per ticker

            chart_paths, figures = generate_all_charts(
                t,
                sliced_data,
                chart_types=selected_charts,
                show_interactive=show_interactive,
                save_files=save_files
            )

            st.write(f"✅ [Charts] Finished charts for {t} — {len(chart_paths)} saved, {len(figures)} figures.")
            all_chart_paths.extend(chart_paths)
            all_figures.extend(figures)

        except Exception as e:
            st.error(f"❌ Chart generation failed for {t}: {e}")

    st.write("✅ [Charts] All tickers processed.")

    # ✅ Now plot the collected figures
    for fig, ticker, chart_type in all_figures:
        unique_key = f"{ticker}_{chart_type}_{uuid.uuid4().hex}"
        try:
            if fig is not None:
                st.plotly_chart(fig, use_container_width=True, key=unique_key)
            else:
                st.warning(f"⚠️ Skipped empty figure for {ticker} ({chart_type})")
        except Exception as e:
            st.error(f"❌ Failed to plot {chart_type} chart for {ticker}: {e}")     

    return all_chart_paths
