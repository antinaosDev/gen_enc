import pandas as pd
import gspread
import io
import datetime
import streamlit as st
import json

PERCAPITA_SHEET_URL = st.secrets["PERCAPITA_SHEET_URL"]
WORKSHEET_NAME = "percapita"

def map_month_to_num(month_str):
    """Convierte el nombre del mes en español a número (1-12)"""
    if not isinstance(month_str, str):
        return 0
    m = month_str.strip().lower()
    months = {
        'enero': 1, 'febrero': 2, 'marzo': 3, 'abril': 4,
        'mayo': 5, 'junio': 6, 'julio': 7, 'agosto': 8,
        'septiembre': 9, 'octubre': 10, 'noviembre': 11, 'diciembre': 12
    }
    return months.get(m, 0)

@st.cache_data(ttl=600, show_spinner=False)
def fetch_percapita_data():
    """Descarga los datos percapita usando las credenciales del app.py"""
    try:
        from app import get_google_sheet_client
        client = get_google_sheet_client()
        if not client:
            return None, "Error de conexión con Google Sheets."
        
        spreadsheet = client.open_by_url(PERCAPITA_SHEET_URL)
        worksheet = spreadsheet.worksheet(WORKSHEET_NAME)
        
        all_data = worksheet.get_all_values()
        if len(all_data) < 2:
            return pd.DataFrame(), "Hoja percapita vacía."
        
        df = pd.DataFrame(all_data[1:], columns=all_data[0])
        return df, None
    except gspread.exceptions.APIError as e:
        if e.response.status_code in [403, 404]:
            return None, f"Acceso denegado a la planilla Percapita. Verifique que se ha compartido el libro '{PERCAPITA_SHEET_URL}' con el correo de la Service Account."
        return None, f"Error API de Google: {e}"
    except gspread.exceptions.WorksheetNotFound:
        return None, f"No se encontró la hoja llamada '{WORKSHEET_NAME}'."
    except Exception as e:
        return None, str(e)

def process_percapita_data(df):
    """Agrupa por el máximo mes y año."""
    if df.empty:
        return df, "Periodo no encontrado"
        
    required_cols = ['RUT', 'ANIO_CORTE', 'MES_CORTE']
    for col in required_cols:
        if col not in df.columns:
            return pd.DataFrame(), f"Falta la columna requerida: {col}"

    df_clean = df.copy()
    
    # Limpieza de valores vacíos y conversión a numérico
    df_clean = df_clean[df_clean['ANIO_CORTE'].str.strip() != ""]
    df_clean['ANIO_CORTE_NUM'] = pd.to_numeric(df_clean['ANIO_CORTE'], errors='coerce').fillna(0).astype(int)
    df_clean['MES_CORTE_NUM'] = df_clean['MES_CORTE'].apply(map_month_to_num)
    
    if df_clean.empty:
        return df_clean, "No hay datos válidos para procesar."
        
    # Identificar el mayor año y mes
    max_year = df_clean['ANIO_CORTE_NUM'].max()
    max_month = df_clean[df_clean['ANIO_CORTE_NUM'] == max_year]['MES_CORTE_NUM'].max()
    
    df_filtered = df_clean[(df_clean['ANIO_CORTE_NUM'] == max_year) & (df_clean['MES_CORTE_NUM'] == max_month)]
    
    period_str = f"Mes: {max_month} | Año: {max_year}"
    if not df_filtered.empty:
        # Intentar obtener el nombre del mes para el mensaje
        max_month_name = df_filtered.iloc[0].get('MES_CORTE', '')
        period_str = f"{str(max_month_name).capitalize()} {max_year}"
    
    return df_filtered, period_str

def cross_reference_families(df_percapita_filtered):
    """
    Lee todas las evaluaciones locales, extrae los integrantes del 'Grupo Familiar JSON'
    y los cruza con el DataFrame de percapitados.
    """
    from app import get_google_sheet_client, SHEET_URL
    import json
    
    client = get_google_sheet_client()
    if not client:
        return pd.DataFrame()
        
    try:
        sh = client.open_by_url(SHEET_URL)
        ws = sh.worksheet("Evaluaciones")
        all_vals = ws.get_all_values()
        if len(all_vals) < 2:
            return pd.DataFrame()
            
        df_evals = pd.DataFrame(all_vals[1:], columns=all_vals[0])
    except Exception:
        return pd.DataFrame()
        
    # Extraer todos los miembros
    members_data = []
    
    for _, row in df_evals.iterrows():
        fam_json = row.get("Grupo Familiar JSON", "[]")
        eval_id = row.get("ID Evaluación", "Desconocido")
        familia = row.get("Familia", "Desconocida")
        sector = row.get("Sector", "No Identificado")
        
        try:
            gf = json.loads(fam_json)
            for m in gf:
                rut_miembro = str(m.get("RUT", "")).strip().upper()
                if not rut_miembro or rut_miembro == "S/R":
                    continue
                
                members_data.append({
                    "ID Evaluación": eval_id,
                    "Familia": familia,
                    "Sector": sector,
                    "Nombre Miembro": str(m.get("Nombre y Apellidos", "")).strip(),
                    "RUT Miembro": rut_miembro,
                    "Parentesco": str(m.get("Parentesco", "")),
                })
        except:
            continue
            
    df_members = pd.DataFrame(members_data)
    if df_members.empty:
        return df_members

    # Limpiar RUTs en Percapita para un cruce exacto
    def clean_rut(rut_str):
        if not isinstance(rut_str, str):
            return str(rut_str).upper()
        # Remueve puntos, permite guion, todo mayúscula
        import re
        r = rut_str.replace(".", "").strip().upper()
        # Asegurarse de que si el RUT tiene formato sin guion, intentar estandarizar
        # (Dependerá de cómo viene en la base percapita, asumimos que viene con guion o sin él pero sin puntos)
        return r

    df_percapita_filtered['RUT_CLEAN'] = df_percapita_filtered['RUT'].apply(clean_rut)
    df_members['RUT_CLEAN'] = df_members['RUT Miembro'].apply(clean_rut)
    
    # Cruce: Left join de Members con Percapita
    df_merged = pd.merge(
        df_members, 
        df_percapita_filtered[['RUT_CLEAN', 'NOMBRE_CENTRO']], 
        on='RUT_CLEAN', 
        how='left'
    )
    
    # Marcar percapitado si tiene cruce exitoso
    df_merged['Estado Percapita'] = df_merged['NOMBRE_CENTRO'].apply(lambda x: 'Percapitado' if pd.notnull(x) and x != "" else 'No Percapitado')
    df_merged['Centro Percapita'] = df_merged['NOMBRE_CENTRO'].fillna('No Registrado')
    
    # Reordenar columnas
    cols_to_show = ["ID Evaluación", "Familia", "Sector", "Nombre Miembro", "RUT Miembro", "Estado Percapita", "Centro Percapita"]
    return df_merged[cols_to_show]

def export_percapita_dashboard_excel(df_cruzado, periodo_str, user_info):
    """
    Genera el Excel del reporte de Percapita de Familias Registradas
    """
    from openpyxl import Workbook
    from openpyxl.styles import PatternFill, Font, Alignment, Border, Side
    from openpyxl.drawing.image import Image as OpenpyxlImage
    import os
    import io
    from datetime import datetime
    
    wb = Workbook()
    ws = wb.active
    ws.title = "Reporte Percapita"
    
    # Estilos
    DARK_BLUE   = PatternFill("solid", fgColor="1F3864")
    CELESTE     = PatternFill("solid", fgColor="BDD7EE")
    BOLD_WHITE  = Font(bold=True, color="FFFFFF", size=12)
    BOLD_DARK   = Font(bold=True, color="1F3864", size=10)
    NORMAL      = Font(size=10)
    THIN = Side(style="thin", color="B8CCE4")
    THIN_BORDER = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)
    CENTER = Alignment(horizontal="center", vertical="center", wrap_text=True)
    LEFT = Alignment(horizontal="left", vertical="center", wrap_text=True)

    def set_cell(row, col, value, fill=None, font=None, align=None, border=True):
        cell = ws.cell(row=row, column=col, value=value)
        if fill: cell.fill = fill
        if font: cell.font = font
        if align: cell.alignment = align
        if border: cell.border = THIN_BORDER
        return cell

    # Cabecera Institucional
    r = 1
    ws.row_dimensions[r].height = 50
    ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=7)
    set_cell(r, 1, f"REPORTE PERCAPITA - USUARIOS DE FAMILIAS REGISTRADAS", DARK_BLUE, BOLD_WHITE, CENTER, border=False)
    
    # Insertar Logo
    logo_path = "NUEVO LOGO.png"
    if not os.path.exists(logo_path):
        logo_path = "Logo_enc_fam.png"
    
    if os.path.exists(logo_path):
        try:
            img = OpenpyxlImage(logo_path)
            # Redimensionar la imagen para que encaje bien (aprox 100x50 px)
            img.width = 100
            img.height = 50
            ws.add_image(img, "A1")
        except Exception:
            pass
            
    r += 1
    ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=7)
    set_cell(r, 1, f"Periodo de Análisis Percapita: {periodo_str}", CELESTE, BOLD_DARK, CENTER, border=False)
    
    r += 1
    ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=7)
    set_cell(r, 1, f"Generado por: {user_info.get('usuario', 'Usuario')} - {user_info.get('cargo', '')} | Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M')}", None, NORMAL, LEFT, border=False)
    
    r += 2
    # Encabezados de tabla
    headers = list(df_cruzado.columns)
    for i, h in enumerate(headers, 1):
        set_cell(r, i, h, DARK_BLUE, BOLD_WHITE, CENTER)
        
    r += 1
    for _, row_data in df_cruzado.iterrows():
        for i, h in enumerate(headers, 1):
            val = str(row_data[h])
            # Color semántico estado
            if h == 'Estado Percapita':
                if val == 'Percapitado':
                    set_cell(r, i, val, PatternFill("solid", fgColor="dcfce7"), Font(color="166534"), CENTER)
                else:
                    set_cell(r, i, val, PatternFill("solid", fgColor="fee2e2"), Font(color="991b1b"), CENTER)
            else:
                set_cell(r, i, val, None, NORMAL, LEFT if i in [2,4] else CENTER)
        r += 1

    # Ajustar anchos
    widths = [15, 25, 12, 35, 15, 15, 20]
    from openpyxl.utils import get_column_letter
    for i, w in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(i)].width = w
        
    buf = io.BytesIO()
    wb.save(buf)
    buf.seek(0)
    return buf
