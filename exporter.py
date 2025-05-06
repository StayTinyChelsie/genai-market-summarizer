# exporter.py
import io
import os
import pandas as pd
import streamlit as st
from fpdf import FPDF
import xlsxwriter
from google_sheet import export_to_sheets
from presentation import generate_presentation

def export_excel_summary(df, file_name="portfolio_analysis.xlsx"):
    excel_buffer = io.BytesIO()
    with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=True, sheet_name='Portfolio')
        workbook = writer.book
        worksheet = writer.sheets['Portfolio']
        if isinstance(df.columns, pd.MultiIndex) and 'Close' in df.columns.get_level_values(0):
            try:
                chart = workbook.add_chart({'type': 'line'})
                chart.add_series({
                    'categories': f'=Portfolio!$A$2:$A${len(df)+1}',
                    'values':     f'=Portfolio!$B$2:$B${len(df)+1}',
                    'name':       'Close Prices'
                })
                chart.set_title({'name': 'Line Chart of Close Prices'})
                worksheet.insert_chart('H2', chart)
            except Exception as e:
                st.warning(f"Chart not created: {e}")
    return excel_buffer

from fpdf import FPDF
import io

def export_pdf_summary(tickers, weights, returns, risks, avg_return, avg_risk):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, txt="Portfolio Summary", ln=True, align="C")

    for i in range(len(tickers)):
        pdf.cell(200, 10, txt=f"{tickers[i]} - Weight: {weights[i]:.2f}, Return: {returns[i]:.4f}, Risk: {risks[i]:.4f}", ln=True)

    pdf.cell(200, 10, txt=f"Weighted Avg Return: {avg_return:.4f}, Risk: {avg_risk:.4f}", ln=True)

    # Use BytesIO and return a stream
    pdf_bytes = pdf.output(dest='S').encode('latin1')
    buffer = io.BytesIO(pdf_bytes)
    return buffer


def get_saved_chart_paths(ticker, df, selected_charts, chart_func):
    return chart_func(ticker, df, selected_charts, show_interactive=False, save_files=True)

def download_powerpoint_btn(ppt_path, label="⬇️ Download AI-Powered PowerPoint"):
    st.download_button(
        label=label,
        data=open(ppt_path, "rb"),
        file_name=os.path.basename(ppt_path),
        mime="application/vnd.openxmlformats-officedocument.presentationml.presentation"
    )

def download_excel_btn(excel_buffer, label="📅 Download Excel File", file_name="portfolio_analysis.xlsx"):
    st.download_button(
        label=label,
        data=excel_buffer.getvalue(),
        file_name=file_name,
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

def download_pdf_btn(pdf_buffer, label="⬇️ Download PDF Report", file_name="hedge_fund_summary.pdf"):
    st.download_button(
        label=label,
        data=pdf_buffer.getvalue(),
        file_name=file_name,
        mime="application/pdf"
    )

def export_to_google_sheets(df, sheet_name):
    try:
        sheet_url = export_to_sheets(df, sheet_name=sheet_name)
        st.success(f"✅ Data exported to [Google Sheets]({sheet_url})")
    except Exception as e:
        st.error(f"⚠️ Google Sheets export failed: {e}")
