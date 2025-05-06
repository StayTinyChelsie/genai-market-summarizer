import gspread
from oauth2client.service_account import ServiceAccountCredentials
import datetime
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set up Google Sheets access
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
credentials_file = os.getenv("GSPREAD_CREDENTIALS", "gspread_credentials.json")
creds = ServiceAccountCredentials.from_json_keyfile_name(credentials_file, scope)
client = gspread.authorize(creds)

# Create or open spreadsheet and select sheet
spreadsheet_name = "GenAI Summaries"
sheet_name = os.getenv("GSPREAD_SHEET_NAME", "Sheet1")

try:
    sheet = client.open(spreadsheet_name).worksheet(sheet_name)
except gspread.exceptions.SpreadsheetNotFound:
    spreadsheet = client.create(spreadsheet_name)  # Create the spreadsheet
    sheet = spreadsheet.add_worksheet(title=sheet_name, rows="100", cols="20")
except gspread.exceptions.WorksheetNotFound:
    spreadsheet = client.open(spreadsheet_name)  # Open the existing spreadsheet
    sheet = spreadsheet.add_worksheet(title=sheet_name, rows="100", cols="20")

# Max length setting (optional)
max_text_length = int(os.getenv("MAX_EXPORT_TEXT_LENGTH", "1000"))

def export_to_sheets(original_text, summary_result):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    original_text_truncated = original_text[:max_text_length]
    summary_result_truncated = summary_result[:max_text_length]
    row = [now, original_text_truncated, summary_result_truncated]
    sheet.append_row(row)

if __name__ == "__main__":
    original_text = "The market is showing strong growth with positive trends."
    summary_result = "Strong market growth observed."
    export_to_sheets(original_text, summary_result)
    print("Exported to Google Sheets successfully.")
    