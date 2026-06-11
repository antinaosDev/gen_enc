import gspread
from oauth2client.service_account import ServiceAccountCredentials
import toml
import os

# --- CONFIG ---
# Leer credenciales
secrets = toml.load("d:/PROYECTOS PROGRAMACIÓN/ANTIGRAVITY_PROJECTS/encuesta_riesgo/.streamlit/secrets.toml")
SHEET_URL = secrets["SHEET_URL"]
creds_dict = secrets["gcp_service_account"]

scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(creds)

try:
    sh = client.open_by_url(SHEET_URL)
    print(f"Spreadsheet Title: {sh.title}")
    print(f"Spreadsheet URL: {SHEET_URL}")
    print(f"Spreadsheet ID: {sh.id}")
    
    worksheets = sh.worksheets()
    print("\nWorksheets found:")
    for ws in worksheets:
        rows = ws.get_all_values()
        print(f"- {ws.title}: {len(rows)} rows (including headers)")
        if ws.title == "Evaluaciones":
             print(f"  First 10 IDs found in Evaluaciones: {[r[0] for r in rows[1:11]] if len(rows) > 1 else 'NO DATA'}")
             if len(rows) > 1:
                 print(f"  Last 5 IDs found in Evaluaciones: {[r[0] for r in rows[-5:]]}")

except Exception as e:
    print(f"Error accessing sheet: {e}")
