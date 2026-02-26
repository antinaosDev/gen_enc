
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json
import toml
from datetime import date

# Cargar secretos directamente del archivo de la app
secrets = toml.load("d:/PROYECTOS PROGRAMACIÓN/ANTIGRAVITY_PROJECTS/encuesta_riesgo/.streamlit/secrets.toml")["gcp_service_account"]

creds_dict = {
    "type": secrets["type"],
    "project_id": secrets["project_id"],
    "private_key_id": secrets["private_key_id"],
    "private_key": secrets["private_key"],
    "client_email": secrets["client_email"],
    "client_id": secrets["client_id"],
    "auth_uri": secrets["auth_uri"],
    "token_uri": secrets["token_uri"],
    "auth_provider_x509_cert_url": secrets["auth_provider_x509_cert_url"],
    "client_x509_cert_url": secrets["client_x509_cert_url"],
    "universe_domain": secrets["universe_domain"]
}

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(creds)
sh = client.open_by_url("https://docs.google.com/spreadsheets/d/1JjYw2W6c-N2swGPuIHbz0CU7aDhh1pA-6VH1WuXV41w/edit")
ws = sh.worksheet("Evaluaciones")

# Definir risk_keys exactas de app.py
risk_keys = [
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

final_headers = [
    "ID Evaluación", "Fecha", "Familia", "Dirección", "Establecimiento", "Sector",
    "Parentesco", "Programa/Unidad", "Puntaje", "Nivel", "Evaluador", "Tipo Unión"
] + risk_keys + ["Grupo Familiar JSON", "Plan Intervención JSON", "Equipo Salud JSON", "Relaciones JSON"] + [
    "Rep Sector", "Familia Comp", "Dir Comp", "Rep Familia", "RUT Rep", "Fecha Comp",
    "Firma Funcionario", "Firma Beneficiario", "Firma Equipo", "Firma Jefe", "Firma Evaluador",
    "egreso_alta", "egreso_traslado", "egreso_derivacion", "egreso_abandono",
    "Fecha Egreso", "Observaciones"
]

# Sincronizar encabezados de la hoja
ws.update(range_name="A1", values=[final_headers])

# Re-insertar familia de máxima complejidad
id_eval = "EVA-999-FAM-MAX"
family_name = "Familia Compleja MAIS"

members = [
    {"Nombre y Apellidos": "Abuelo Roberto", "RUT": "5111222-3", "F. Nac": "1940-03-03", "Sexo": "M", "Parentesco": "Abuelo/a", "Resp": False, "E. Civil": "Fallecido/a", "Cronico": True},
    {"Nombre y Apellidos": "Juan Jefe Demo", "RUT": "15111222-3", "F. Nac": "1980-06-15", "Sexo": "M", "Parentesco": "Jefe/a de Hogar", "Resp": True, "E. Civil": "Divorciado/a", "Cronico": False},
    {"Nombre y Apellidos": "Elena Pareja Actual", "RUT": "16222333-4", "F. Nac": "1985-09-20", "Sexo": "F", "Parentesco": "Cónyuge/Pareja", "Resp": False, "E. Civil": "Conviviente", "Cronico": True},
    {"Nombre y Apellidos": "Gemelo 1", "RUT": "22111444-1", "F. Nac": "2010-05-10", "Sexo": "M", "Parentesco": "Hijo/a (Gemelo Fraterno)", "Resp": False, "E. Civil": "Soltero/a"},
    {"Nombre y Apellidos": "Gemelo 2", "RUT": "22111444-2", "F. Nac": "2010-05-10", "Sexo": "F", "Parentesco": "Hijo/a (Gemelo Fraterno)", "Resp": False, "E. Civil": "Soltero/a"},
    {"Nombre y Apellidos": "Idéntico A", "RUT": "22111555-1", "F. Nac": "2015-08-12", "Sexo": "F", "Parentesco": "Hijo/a (Gemelo Idéntico)", "Resp": False, "E. Civil": "Soltero/a"},
    {"Nombre y Apellidos": "Idéntico B", "RUT": "22111555-2", "F. Nac": "2015-08-12", "Sexo": "F", "Parentesco": "Hijo/a (Gemelo Idéntico)", "Resp": False, "E. Civil": "Soltero/a"},
    {"Nombre y Apellidos": "Embarazo Actual", "RUT": "GEST-001", "F. Nac": "2024-10-01", "Sexo": "G", "Parentesco": "Hijo/a", "Resp": False, "E. Civil": "Soltero/a"},
    {"Nombre y Apellidos": "Aborto Previo", "RUT": "GEST-002", "F. Nac": "2022-05-01", "Sexo": "G", "Parentesco": "Hijo/a", "Resp": False, "E. Civil": "Provocado"}
]

# Definir relaciones (usando IDs m0, m1...)
relaciones = [
    {"from": "m1", "to": "m2", "type": "estrecha conflictiva"}, # Fusionada-Conflictiva
    {"from": "m1", "to": "m3", "type": "estrecha"},
    {"from": "m2", "to": "m0", "type": "distante"},
    {"from": "m1", "to": "m0", "type": "quiebre"}
]

row = [
    id_eval, str(date.today()), family_name, "Cholchol Rural Km 7", "CESFAM Cholchol", "Luna",
    "Jefe/a de Hogar", "Salud Mental", 50, "RIESGO ALTO", "Sistema MAIS", "Divorciados"
]
risks = [False] * 47
risks[0] = True # VIF
risks[13] = True # Judicial
row.extend(risks)

row.extend([
    json.dumps(members, ensure_ascii=False), # Grupo Familiar JSON
    "[]",                                    # Plan Intervención JSON
    "[]",                                    # Equipo Salud JSON
    json.dumps(relaciones),                  # Relaciones JSON
    "Luna", family_name, "Camino Cholchol", members[1]["Nombre y Apellidos"], members[1]["RUT"], str(date.today()),
    "Firma F", "Firma B", "", "Firma J", "Firma E",
    False, False, False, False, "", "Escenario extremo con todas las simbologías."
])

# Actualizar o insertar
all_values = ws.get_all_values()
row_to_update = -1
for i, r in enumerate(all_values):
    if r and r[0] == id_eval:
        row_to_update = i + 1
        break

if row_to_update != -1:
    ws.update(range_name=f"A{row_to_update}", values=[row])
    print(f"✅ Actualizado registro {id_eval} en fila {row_to_update}")
else:
    ws.append_row(row, value_input_option='USER_ENTERED')
    print(f"✅ Insertado nuevo registro {id_eval}")
# --- ESCENARIO 2: MÁXIMA SIMBOLOGÍA (SYM-TEST) ---
id_eval_sym = "EVA-888-SYM-TEST"
family_name_sym = "FAMILIA PRUEBA SIMBOLOGÍA"

members_sym = [
    {"Nombre y Apellidos": "Pedro Abuelo", "RUT": "5111222-K", "F. Nac": "1940-01-01", "Sexo": "M", "Parentesco": "Abuelo/a", "Resp": False, "E. Civil": "Fallecido/a", "Cronico": True}, # Fallecido + Crónico
    {"Nombre y Apellidos": "Juan Jefe (IP)", "RUT": "15111222-1", "F. Nac": "1980-01-01", "Sexo": "M", "Parentesco": "Jefe/a de Hogar", "Resp": True, "E. Civil": "Casado/a", "Cronico": True}, # IP + Crónico
    {"Nombre y Apellidos": "Maria Pareja", "RUT": "16111222-2", "F. Nac": "1982-01-01", "Sexo": "F", "Parentesco": "Cónyuge/Pareja", "Resp": False, "E. Civil": "Casado/a", "Cronico": True}, # Crónico
    {"Nombre y Apellidos": "Carla Gemela F", "RUT": "22111333-1", "F. Nac": "2010-01-01", "Sexo": "F", "Parentesco": "Hijo/a (Gemelo Fraterno)", "Resp": False, "E. Civil": "Soltero/a"},
    {"Nombre y Apellidos": "Carlos Gemelo F", "RUT": "22111333-2", "F. Nac": "2010-01-01", "Sexo": "M", "Parentesco": "Hijo/a (Gemelo Fraterno)", "Resp": False, "E. Civil": "Soltero/a"},
    {"Nombre y Apellidos": "Ana Gemela I", "RUT": "22111444-1", "F. Nac": "2015-01-01", "Sexo": "F", "Parentesco": "Hijo/a (Gemelo Idéntico)", "Resp": False, "E. Civil": "Soltero/a"},
    {"Nombre y Apellidos": "Bela Gemela I", "RUT": "22111444-2", "F. Nac": "2015-01-01", "Sexo": "F", "Parentesco": "Hijo/a (Gemelo Idéntico)", "Resp": False, "E. Civil": "Soltero/a"},
    {"Nombre y Apellidos": "Embarazo", "RUT": "G-001", "F. Nac": "2025-01-01", "Sexo": "G", "Parentesco": "Hijo/a", "Resp": False, "E. Civil": "Soltero/a"}, # Gestación normal
    {"Nombre y Apellidos": "Aborto Esp", "RUT": "G-002", "F. Nac": "2024-01-01", "Sexo": "G", "Parentesco": "Hijo/a", "Resp": False, "E. Civil": "Espontáneo"}, # Gestación aborto X
    {"Nombre y Apellidos": "Aborto Pro", "RUT": "G-003", "F. Nac": "2023-01-01", "Sexo": "G", "Parentesco": "Hijo/a", "Resp": False, "E. Civil": "Provocado"} # Gestación aborto ●
]

relaciones_sym = [
    {"from": "m1", "to": "m2", "type": "estrecha conflictiva"}, # Juan-Maria: Fusionada-Conflictiva (≡⚡)
    {"from": "m1", "to": "m0", "type": "quiebre"},              # Juan-Pedro: Quiebre (||)
    {"from": "m2", "to": "m3", "type": "distante"},             # Maria-Carla: Distante (···)
    {"from": "m3", "to": "m4", "type": "fusionada"},            # Carla-Carlos: Fusionada (≡)
    {"from": "m1", "to": "m4", "type": "conflictiva"}           # Juan-Carlos: Conflictiva (⚡)
]

row_sym = [
    id_eval_sym, str(date.today()), family_name_sym, "Calle de las Rosas 123", "CESFAM Demo", "Sector Sur",
    "Jefe/a de Hogar", "APS General", 25, "RIESGO MEDIO", "Sistema Antigravity", "Casados"
]
risks_sym = [False] * 47
risks_sym[16] = True # Patología Crónica (T3)
row_sym.extend(risks_sym)

row_sym.extend([
    json.dumps(members_sym, ensure_ascii=False), # Grupo Familiar JSON
    "[]",                                         # Plan Intervención JSON
    "[]",                                         # Equipo Salud JSON
    json.dumps(relaciones_sym),                   # Relaciones JSON
    "Sector Sur", family_name_sym, "Calle Rosas", "Juan Jefe", "15111222-1", str(date.today()),
    "", "", "", "", "",
    False, False, False, False, "", "Escenario de prueba integral con toda la simbología clínica."
])

# Guardar ambos
ws.append_rows([row, row_sym])
print(f"✅ Escenarios EVA-999 y {id_eval_sym} creados exitosamente.")
