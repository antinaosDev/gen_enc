import gspread
from oauth2client.service_account import ServiceAccountCredentials
import toml

# --- CONFIG ---
SHEET_URL = "https://docs.google.com/spreadsheets/d/1JjYw2W6c-N2swGPuIHbz0CU7aDhh1pA-6VH1WuXV41w/edit"
secrets = toml.load("d:/PROYECTOS PROGRAMACIÓN/ANTIGRAVITY_PROJECTS/encuesta_riesgo/.streamlit/secrets.toml")
creds_dict = secrets["gcp_service_account"]
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(creds)

def clean_sheet(sheet_name):
    sh = client.open_by_url(SHEET_URL)
    ws = sh.worksheet(sheet_name)
    all_rows = ws.get_all_values()
    
    if not all_rows:
        return
        
    header = all_rows[0]
    # Filtrar filas que tengan al menos algo en las primeras columns (ID o Familia)
    # o que simplemente no sean todo strings vacíos
    clean_rows = []
    clean_rows.append(header)
    
    for row in all_rows[1:]:
        # Criterio: tener un ID de evaluación o al menos el nombre de la familia
        if row[0].strip() or (len(row) > 2 and row[2].strip()):
            clean_rows.append(row)
    
    print(f"Sheet '{sheet_name}': Original rows {len(all_rows)}, Cleaned rows {len(clean_rows)}")
    
    # Limpiar y reescribir
    ws.clear()
    ws.update('A1', clean_rows)

if __name__ == "__main__":
    clean_sheet("Evaluaciones")
    clean_sheet("Planes de Intervención")
    clean_sheet("Ecomapas")
