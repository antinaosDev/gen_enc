"""
migrate_ids.py
Migración directa de IDs de Evaluación al formato EVA-NNN-FAM-XXX en Google Sheets.
Ejecutar desde la raíz del proyecto: python migrate_ids.py
"""
import unicodedata
import re
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import toml

# ----------- Cargar credenciales desde secrets.toml -----------
secrets = toml.load(r".streamlit/secrets.toml")
creds_dict = dict(secrets["gcp_service_account"])

SCOPE = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

# Leer URL desde el mismo archivo o configurarlo aquí
# Si la URL está en secrets.toml, leerla desde ahí; sino, escribirla directamente
SHEET_URL = secrets.get("SHEET_URL", "")
if not SHEET_URL:
    # Leer desde config si existe
    try:
        cfg = toml.load(r".streamlit/config.toml")
        SHEET_URL = cfg.get("SHEET_URL", "")
    except Exception:
        pass

# Si aún no se encontró, buscarla en app.py
if not SHEET_URL:
    with open("app.py", "r", encoding="utf-8") as f:
        for line in f:
            if "SHEET_URL" in line and "=" in line and "http" in line:
                SHEET_URL = line.split("=", 1)[1].strip().strip('"').strip("'")
                break

print(f"✅ Conectando a: {SHEET_URL[:60]}...")

credentials = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, SCOPE)
client = gspread.authorize(credentials)
spreadsheet = client.open_by_url(SHEET_URL)


def clean_prefix(apellido):
    """Extrae 3 letras del apellido, sin tildes."""
    if not apellido or not str(apellido).strip():
        return "XXX"
    s = unicodedata.normalize('NFD', str(apellido).strip())
    s = ''.join(c for c in s if unicodedata.category(c) != 'Mn')
    s = ''.join(c for c in s if c.isalpha())
    return s[:3].upper() if len(s) >= 3 else s.upper().ljust(3, 'X')


# ----------- Leer hoja Evaluaciones -----------
print("📋 Leyendo hoja Evaluaciones...")
ws_eval = spreadsheet.worksheet("Evaluaciones")
all_vals = ws_eval.get_all_values()

if len(all_vals) < 2:
    print("⚠️ No hay registros en Evaluaciones. Nada que migrar.")
    exit(0)

headers = all_vals[0]
data_rows = all_vals[1:]

id_col  = headers.index("ID Evaluación") if "ID Evaluación" in headers else 0
fam_col = headers.index("Familia") if "Familia" in headers else 2

print(f"   → {len(data_rows)} registros encontrados.")
print(f"   → Columna ID: [{id_col}] | Columna Familia: [{fam_col}]")
print()

# ----------- Construir mapa ID_viejo → ID_nuevo -----------
id_map = {}
updates_eval = []
counter = 1

for row in data_rows:
    old_id   = str(row[id_col]).strip()  if len(row) > id_col  else ""
    apellido = str(row[fam_col]).strip().split()[0] if len(row) > fam_col and str(row[fam_col]).strip() else ""
    prefix   = clean_prefix(apellido)
    new_id   = f"EVA-{counter:03d}-FAM-{prefix}"
    id_map[old_id] = new_id

    updated_row = list(row)
    updated_row[id_col] = new_id
    updates_eval.append((counter + 1, updated_row))  # +1 por encabezado
    print(f"   [{counter:03d}] {old_id or '(vacío)':40s} → {new_id}  (Familia: {apellido or 'N/A'})")
    counter += 1

print()
print("💾 Actualizando hoja Evaluaciones...")
for sheet_row_num, updated_row in updates_eval:
    ws_eval.update(range_name=f"A{sheet_row_num}", values=[updated_row])
    print(f"   ✅ Fila {sheet_row_num} actualizada.")

# ----------- Actualizar Planes de Intervención -----------
try:
    ws_plan = spreadsheet.worksheet("Planes de Intervención")
    plan_all = ws_plan.get_all_values()
    if len(plan_all) > 1:
        plan_headers = plan_all[0]
        plan_id_col = plan_headers.index("ID Evaluación") if "ID Evaluación" in plan_headers else 0
        print(f"\n📋 Actualizando Planes de Intervención ({len(plan_all)-1} filas)...")
        for i, row in enumerate(plan_all[1:], 2):
            if len(row) > plan_id_col:
                old_id = str(row[plan_id_col]).strip()
                if old_id in id_map:
                    updated_row = list(row)
                    updated_row[plan_id_col] = id_map[old_id]
                    ws_plan.update(range_name=f"A{i}", values=[updated_row])
                    print(f"   ✅ Plan fila {i}: {old_id} → {id_map[old_id]}")
except Exception as e:
    print(f"   ⚠️ Planes de Intervención: {e}")

# ----------- Actualizar Ecomapas -----------
try:
    ws_eco = spreadsheet.worksheet("Ecomapas")
    eco_all = ws_eco.get_all_values()
    if len(eco_all) > 1:
        eco_headers = eco_all[0]
        eco_id_col = eco_headers.index("ID Evaluación") if "ID Evaluación" in eco_headers else 0
        print(f"\n🗺️  Actualizando Ecomapas ({len(eco_all)-1} filas)...")
        for i, row in enumerate(eco_all[1:], 2):
            if len(row) > eco_id_col:
                old_id = str(row[eco_id_col]).strip()
                if old_id in id_map:
                    updated_row = list(row)
                    updated_row[eco_id_col] = id_map[old_id]
                    ws_eco.update(range_name=f"A{i}", values=[updated_row])
                    print(f"   ✅ Ecomapa fila {i}: {old_id} → {id_map[old_id]}")
except Exception as e:
    print(f"   ⚠️ Ecomapas: {e}")

print()
print(f"✅ MIGRACIÓN COMPLETA: {len(updates_eval)} evaluaciones actualizadas.")
print("   Los nuevos IDs en Google Sheets ya tienen el formato EVA-NNN-FAM-XXX")
