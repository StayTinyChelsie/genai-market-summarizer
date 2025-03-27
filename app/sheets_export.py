
import gspread
from oauth2client.service_account import ServiceAccountCredentials

def export_to_sheets(summary, sentiment, sheet_name="Summaries"):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("gcreds.json", scope)
    client = gspread.authorize(creds)

    sheet = client.open(sheet_name).sheet1
    sheet.append_row([summary, sentiment])
