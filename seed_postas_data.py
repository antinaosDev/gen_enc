import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json
import random
from datetime import date, timedelta

# --- CONFIG ---
SHEET_URL = "https://docs.google.com/spreadsheets/d/1JjYw2W6c-N2swGPuIHbz0CU7aDhh1pA-6VH1WuXV41w/edit"

# Credenciales (se asume que el script corre en el mismo entorno)
# Para este script rápido, leeré el secrets.toml local
import toml
secrets = toml.load("d:/PROYECTOS PROGRAMACIÓN/ANTIGRAVITY_PROJECTS/encuesta_riesgo/.streamlit/secrets.toml")
creds_dict = secrets["gcp_service_account"]

scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(creds)
sh = client.open_by_url(SHEET_URL)
ws_eval = sh.worksheet("Evaluaciones")

# --- LISTAS DE DATOS ---
POSTAS = ["Posta Malalche", "Posta Huentelar", "Posta Huamaqui", "EMR Repocura", "EMR Rapahue"]
APELLIDOS = ["Perez", "Gonzalez", "Muñoz", "Rojas", "Jimenez", "Saavedra", "Painemal", "Huenchullan", "Curivil", "Ñancupil"]
NOMBRES = ["Juan", "Maria", "Jose", "Rosa", "Luis", "Ana", "Carlos", "Carmen", "Patricio", "Elena"]

RISK_KEYS = [
    't1_vif', 't1_drogas', 't1_alcohol', 't1_saludMentalDescomp', 't1_abusoSexual', 
    't1_riesgoBiopsicoGrave', 't1_epsaRiesgo', 't1_vulnerabilidadExtrema', 't1_trabajoInfantil',
    't2_enfermedadGrave', 't2_altoRiesgoHosp', 't2_discapacidad', 't2_saludMentalLeve', 
    't2_judicial', 't2_rolesParentales', 't2_adultosRiesgo',
    't3_patologiaCronica', 't3_discapacidadLeve', 't3_rezago', 't3_madreAdolescente', 
    't3_sinRedApoyo', 't3_cesantia', 't3_vulneNoExtrema', 't3_precariedadLaboral', 
    't3_hacinamiento', 't3_entornoInseguro', 't3_adultoSolo', 't3_desercionEscolar', 
    't3_analfabetismo', 't3_escolaridadIncompleta', 't3_dificultadAcceso',
    't4_monoparental', 't4_riesgoCardio', 't4_contaminacion', 't4_higiene', 
    't4_sinRecreacion', 't4_sinEspaciosSeguros', 't4_endeudamiento', 't4_serviciosIncompletos',
    't5_lactancia', 't5_habitos', 't5_redesSociales', 't5_redFamiliar', 
    't5_comunicacion', 't5_recursosSuficientes', 't5_resiliencia', 't5_viviendaAdecuada'
]

def generate_rut():
    num = random.randint(10000000, 25000000)
    # simplificado sin DV real para datos de prueba rápidos
    return f"{num//1000000}.{(num//1000)%1000:03d}.{num%1000:03d}-K"

def seed_data():
    rows_to_add = []
    
    # Obtener el último ID para seguir la secuencia
    all_vals = ws_eval.get_all_values()
    last_idx = 1
    if len(all_vals) > 1:
        try:
            # EVA-001-FAM-XXX
            last_id = all_vals[-1][0]
            last_number = int(last_id.split('-')[1])
            last_idx = last_number + 1
        except:
            last_idx = len(all_vals)

    for i in range(20):
        apellido = random.choice(APELLIDOS)
        familia_name = f"Familia {apellido}"
        posta = random.choice(POSTAS)
        eval_id = f"EVA-{last_idx + i:03d}-FAM-{apellido[:3].upper()}"
        fecha = (date.today() - timedelta(days=random.randint(0, 30))).strftime("%Y-%m-%d")
        
        # Miembros
        members = []
        n_members = random.randint(2, 5)
        for m in range(n_members):
            members.append({
                "Nombre y Apellidos": f"{random.choice(NOMBRES)} {apellido}",
                "RUT": generate_rut(),
                "F. Nac": (date.today() - timedelta(days=random.randint(365*1, 365*80))).strftime("%Y-%m-%d"),
                "Sexo": random.choice(["M", "F"]),
                "Resp": (m == 0)
            })
        
        ruts_list = ", ".join([m["RUT"] for m in members])
        
        # Riesgos
        risks_vals = []
        active_risks_dict = {}
        for k in RISK_KEYS:
            val = random.random() < 0.15 # 15% de probabilidad de riesgo
            risks_vals.append(val)
            active_risks_dict[k] = val
        
        # Puntajes y Niveles
        puntos = sum([5 if v and k.startswith('t1') else 3 if v and k.startswith('t2') else 1 if v else 0 for k,v in active_risks_dict.items()])
        nivel = "RIESGO ALTO" if puntos > 15 else "RIESGO MEDIO" if puntos > 5 else "RIESGO BAJO"
        
        # Data row matching final_headers
        row = [
            eval_id, fecha, familia_name, f"Calle Falsa {random.randint(100, 999)}", 
            posta, "Luna", "Jefe/a de Hogar", "Salud Rural",
            puntos, nivel, "Simulador de Datos",
            ruts_list
        ]
        row.extend(risks_vals)
        
        # JSONs
        row.append(json.dumps(members, ensure_ascii=False))
        row.append(json.dumps([{"Objetivo": "Prueba", "Actividad": "Seguimiento", "Fecha Prog": fecha}], ensure_ascii=False))
        row.append(json.dumps([{"Nombre y Profesión": "Médico Simulador", "Firma": True}], ensure_ascii=False))
        
        # Extra Fields (Compromisos, Firmas, Egreso, Observaciones) - 17 campos vacíos aprox
        row.extend([""] * 17)
        
        rows_to_add.append(row)
    
    ws_eval.append_rows(rows_to_add)
    print(f"Se han insertado 20 registros para {POSTAS}")

if __name__ == "__main__":
    seed_data()
