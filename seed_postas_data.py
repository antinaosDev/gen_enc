"""
seed_postas_data.py — Inserta 30 familias de prueba ricas.
RISK_KEYS sincronizados exactamente con app.py (incluye t3_duelo).
"""
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json, random
from datetime import date, timedelta

SHEET_URL = "https://docs.google.com/spreadsheets/d/1JjYw2W6c-N2swGPuIHbz0CU7aDhh1pA-6VH1WuXV41w/edit"
import toml
secrets    = toml.load("d:/PROYECTOS PROGRAMACIÓN/ANTIGRAVITY_PROJECTS/encuesta_riesgo/.streamlit/secrets.toml")
creds_dict = secrets["gcp_service_account"]
scope  = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds  = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(creds)
sh     = client.open_by_url(SHEET_URL)
ws_eval = sh.worksheet("Evaluaciones")

# ── EXACTAMENTE igual a app.py risk_keys ──────────────────────────────────
RISK_KEYS = [
    't1_vif', 't1_drogas', 't1_alcohol', 't1_saludMentalDescomp', 't1_abusoSexual',
    't1_riesgoBiopsicoGrave', 't1_epsaRiesgo', 't1_vulnerabilidadExtrema', 't1_trabajoInfantil',
    't2_enfermedadGrave', 't2_altoRiesgoHosp', 't2_discapacidad', 't2_saludMentalLeve',
    't2_judicial', 't2_rolesParentales', 't2_sobrecargaCuidador', 't2_conflictosSeveros', 't2_adultosRiesgo',
    't3_patologiaCronica', 't3_discapacidadLeve', 't3_rezago', 't3_madreAdolescente', 't3_duelo',
    't3_sinRedApoyo', 't3_cesantia', 't3_vulneNoExtrema', 't3_precariedadLaboral',
    't3_hacinamiento', 't3_entornoInseguro', 't3_adultoSolo', 't3_desercionEscolar',
    't3_analfabetismo', 't3_escolaridadIncompleta', 't3_dificultadAcceso',
    't4_monoparental', 't4_riesgoCardio', 't4_contaminacion', 't4_higiene',
    't4_sinRecreacion', 't4_sinEspaciosSeguros', 't4_endeudamiento', 't4_serviciosIncompletos',
    't5_lactancia', 't5_habitos', 't5_redesSociales', 't5_redFamiliar',
    't5_comunicacion', 't5_recursosSuficientes', 't5_resiliencia', 't5_viviendaAdecuada'
]

# ── Datos ─────────────────────────────────────────────────────────────────
APELLIDOS  = ["Perez","Gonzalez","Muñoz","Rojas","Jimenez","Saavedra",
               "Painemal","Huenchullan","Curivil","Ñancupil",
               "Catrileo","Lefiman","Nahuelpan","Cayupe","Cona",
               "Torres","Vargas","Fuentes","Valenzuela","Castro"]
NOMBRES_M  = ["Juan","José","Carlos","Luis","Miguel","Pedro","Rodrigo","Jorge","Pablo","Diego"]
NOMBRES_F  = ["María","Rosa","Ana","Carmen","Elena","Daniela","Francisca","Valentina","Javiera","Pilar"]
POSTAS     = ["Cesfam Cholchol","Posta Huentelar","Posta Huamaqui","Posta Malalche","EMR Rapahue","EMR Repocura"]
SECTORES   = ["Sol","Luna"]
PROGRAMAS  = ["MAIS","ChCC","Salud Mental","Adulto Mayor","Crónico","SOME"]
GENEROS    = ["Masculino","Femenino","No binario","Transgénero","Prefiero no decir"]
ECIVIL     = ["Soltero/a (S)","Casado/a (C)","Conviviente (Co)","Divorciado/a (D)","Viudo/a (V)","Fallecido/a (F)"]
PARENTESCOS     = ["Jefe/a de Hogar","Cónyuge/Pareja","Hijo/a","Padre/Madre","Abuelo/a","Hermano/a","Tío/a","Nieto/a","Otro familiar"]
OCUPACIONES     = ["Obrero/a","Dueño/a de Casa","Estudiante","Agricultor/a","Temporero/a",
                    "Enfermero/a","Comerciante","Pensionado/a","Sin empleo","Técnico/a","Profesor/a"]
ETNIAS          = ["Ninguno","Mapuche","Aymara","Rapa Nui","Atacameño (Lickanantay)",
                   "Quechua","Colla","Diaguita","Afrodescendiente","Otro","Ninguno","Mapuche","Ninguno","Ninguno"]
NACIONALIDADES  = ["Chilena","Chilena","Chilena","Chilena","Venezolana","Peruana","Haitiana","Colombiana"]
TIPO_UNION_OPTS = ["Casados","Convivientes","Separados","Sin pareja"]
OBJETIVOS  = ["Reducir factores de riesgo de VIF","Controlar patología crónica",
               "Mejorar acceso a red de apoyo","Acompañamiento en proceso de duelo",
               "Inserción laboral del jefe de hogar","Control psicológico familiar",
               "Derivación a programa social","Educación en hábitos saludables"]
ACTIVIDADES = ["Visita domiciliaria quincenal","Derivación a psicólogo/a",
                "Coordinación con DIDECO","Taller de crianza ChCC",
                "Control médico mensual","Seguimiento telefónico",
                "Inscripción en programa","Apoyo educacional"]
ESTADOS_SEG = ["Pendiente","En progreso","Completado","En progreso","Pendiente","Cancelado"]
EVALUACIONES_PLAN = ["Logrado","Parcial","No logrado","Pendiente",""]
OBS_POOL = [
    "Familia comprometida con el plan establecido.",
    "Se detecta resistencia al proceso. Se acordó nueva fecha.",
    "Buena adherencia. Avance satisfactorio.",
    "Familia en situación de hacinamiento. Se coordinó con municipio.",
    "Cuidador principal presenta sobrecarga. Se derivó a psicología.",
    "Menor con rezago del desarrollo. En control con kinesiología.",
    "Adulto mayor vive solo. Red de apoyo escasa.",
    "Situación de VIF en curso. Se activó protocolo.",
    "Familia requiere apoyo nutricional.",
    "Plan ejecutado satisfactoriamente. Evaluando egreso.",
]

def rut():
    n = random.randint(8_000_000, 25_000_000)
    return f"{n//1_000_000}.{(n//1000)%1000:03d}.{n%1000:03d}-{random.choice('0123456789K')}"

def rand_past(years_min=1, years_max=80):
    return (date.today() - timedelta(days=random.randint(365*years_min, 365*years_max))).strftime("%Y-%m-%d")

def rand_future(days_max=60):
    return (date.today() + timedelta(days=random.randint(7, days_max))).strftime("%Y-%m-%d")

def gen_family(apellido):
    n = random.randint(2, 7)
    members = []
    for i in range(n):
        genero = random.choice(GENEROS)
        nombre = random.choice(NOMBRES_M if genero == "Masculino" else NOMBRES_F)
        parentesco = PARENTESCOS[0] if i == 0 else random.choice(PARENTESCOS[1:])
        members.append({
            "Nombre y Apellidos": f"{nombre} {apellido} {random.choice(APELLIDOS)}",
            "RUT":                rut(),
            "F. Nac":             rand_past(1, 80),
            "Identidad de género": genero,
            "Pueblo Originario":  random.choice(ETNIAS),
            "Nacionalidad":       random.choice(NACIONALIDADES),
            "Parentesco":         parentesco,
            "E. Civil":           random.choice(ECIVIL),
            "Ocupación":          random.choice(OCUPACIONES),
            "Cronico":            random.random() < 0.20,
            "Resp":               (i == 0),
        })
    return members

def gen_plan():
    plan = []
    for _ in range(random.randint(2, 5)):
        fp = (date.today() - timedelta(days=random.randint(10, 90))).strftime("%Y-%m-%d")
        fr = (date.today() - timedelta(days=random.randint(0, 9))).strftime("%Y-%m-%d") if random.random() < 0.55 else ""
        plan.append({
            "Objetivo":          random.choice(OBJETIVOS),
            "Actividad":         random.choice(ACTIVIDADES),
            "Fecha Prog":        fp,
            "Responsable":       f"{'Dra.' if random.random()<.5 else 'Dr.'} {random.choice(NOMBRES_F+NOMBRES_M)} {random.choice(APELLIDOS)}",
            "Fecha Real":        fr,
            "Evaluación":        random.choice(EVALUACIONES_PLAN),
            "Estado":            random.choice(ESTADOS_SEG),
            "F. Seguimiento":    rand_future(45),
            "Obs. Seguimiento":  random.choice(["","Requiere atención adicional","Avance positivo","Sin novedades"]),
        })
    return plan

def gen_seguimiento(plan):
    return [{
        "Objetivo":         row["Objetivo"],
        "Actividad":        row["Actividad"],
        "Estado":           row["Estado"],
        "F. Seguimiento":   row["F. Seguimiento"],
        "Obs. Seguimiento": row["Obs. Seguimiento"],
    } for row in plan]

def gen_apgar():
    vals = [random.randint(0, 2) for _ in range(5)]
    return sum(vals), vals

def compute_risk(active):
    c_t3 = sum(1 for k,v in active.items() if k.startswith('t3') and v)
    c_t4 = sum(1 for k,v in active.items() if k.startswith('t4') and v)
    s_t3 = c_t3 * 4
    s_t4 = c_t4 * 3
    total = s_t3 + s_t4
    if any(v for k,v in active.items() if k.startswith('t1') and v):
        nivel = "RIESGO ALTO"
    elif total >= 14:
        nivel = "RIESGO ALTO"
    elif total >= 7:
        nivel = "RIESGO MEDIO"
    elif total > 0:
        nivel = "RIESGO BAJO"
    else:
        nivel = "SIN RIESGO"
    return total, nivel


def delete_last_n_rows(ws, n):
    """Elimina las últimas n filas de datos (no header)."""
    all_vals = ws.get_all_values()
    total = len(all_vals)
    if total <= 1:
        print("No hay filas para eliminar.")
        return
    start_row = max(2, total - n + 1)
    rows_to_delete = list(range(total, start_row - 1, -1))
    print(f"Eliminando {len(rows_to_delete)} fila(s) incorrecta(s)...")
    for r in rows_to_delete:
        ws.delete_rows(r)
    print("Filas eliminadas.")


def seed_data(n=30):
    # 1. Eliminar los 30 registros malos anteriores
    delete_last_n_rows(ws_eval, 30)

    # 2. Determinar último ID
    all_vals = ws_eval.get_all_values()
    last_idx = 1
    if len(all_vals) > 1:
        try:
            last_idx = int(all_vals[-1][0].split('-')[1]) + 1
        except:
            last_idx = len(all_vals)

    rows = []
    for i in range(n):
        apellido  = random.choice(APELLIDOS)
        apellido2 = random.choice(APELLIDOS)
        familia   = f"Familia {apellido} {apellido2}"
        posta     = random.choice(POSTAS)
        sector    = random.choice(SECTORES)
        programa  = random.choice(PROGRAMAS)
        eval_id   = f"EVA-{last_idx+i:03d}-FAM-{apellido[:3].upper()}"
        fecha     = (date.today() - timedelta(days=random.randint(0, 120))).strftime("%Y-%m-%d")
        direccion = f"{random.choice(['Calle','Pasaje','Camino a','Las','Los'])} {random.choice(APELLIDOS)} #{random.randint(100,9999)}, Cholchol"

        members  = gen_family(apellido)
        ruts_str = ", ".join(m["RUT"] for m in members)

        # Risk
        perfiles = ["alto","medio","bajo","sin"]
        pesos    = [0.20, 0.40, 0.30, 0.10]
        perfil   = random.choices(perfiles, pesos)[0]
        active = {}
        for k in RISK_KEYS:
            if perfil == "alto":
                p = 0.45 if k.startswith('t1') else 0.30 if k.startswith('t2') else 0.35
            elif perfil == "medio":
                p = 0.05 if k.startswith('t1') else 0.20 if k.startswith('t2') else 0.45
            elif perfil == "bajo":
                p = 0.02 if k.startswith('t1') else 0.08 if k.startswith('t2') else 0.18
            else:
                p = 0.01
            active[k] = random.random() < p
        total_pts, nivel = compute_risk(active)

        plan = gen_plan()
        seg  = gen_seguimiento(plan)
        apgar_total, apgar_vals = gen_apgar()

        evaluador  = f"{random.choice(['Enf.','Dr.','Dra.','Mat.','AS.'])} {random.choice(NOMBRES_F+NOMBRES_M)} {random.choice(APELLIDOS)}"
        rep_sector = f"{random.choice(NOMBRES_F+NOMBRES_M)} {random.choice(APELLIDOS)} ({random.choice(['Enf.','Dr./Dra.','AS.'])})"
        comp_fecha = (date.today() - timedelta(days=random.randint(0, 30))).strftime("%Y-%m-%d")

        # Egresos (20%)
        egreso_alta = egreso_tras = egreso_der = egreso_aban = False
        fecha_egreso = ""
        if random.random() < 0.20:
            e = random.choice(["alta","traslado","derivacion","abandono"])
            egreso_alta = e == "alta"; egreso_tras = e == "traslado"
            egreso_der  = e == "derivacion"; egreso_aban = e == "abandono"
            fecha_egreso = (date.today() - timedelta(days=random.randint(0,15))).strftime("%Y-%m-%d")

        link_drive = f"https://drive.google.com/drive/folders/DEMO_{eval_id}"

        # ── Fila (debe coincidir EXACTAMENTE con final_headers de app.py) ──
        row = [
            eval_id, fecha, familia, direccion, posta, sector,
            random.choice(PARENTESCOS[:4]), programa,
            total_pts, nivel, evaluador,
            random.choice(TIPO_UNION_OPTS), ruts_str,
        ]                                                       # 13 cols
        row.extend([active[k] for k in RISK_KEYS])             # 50 cols
        # JSONs (5)
        row.append(json.dumps(members, ensure_ascii=False, default=str))
        row.append(json.dumps(plan,    ensure_ascii=False, default=str))
        row.append(json.dumps([
            {"Nombre y Profesión": f"Enf. {random.choice(NOMBRES_F)} {random.choice(APELLIDOS)}", "Firma": ""},
            {"Nombre y Profesión": f"AS. {random.choice(NOMBRES_F)} {random.choice(APELLIDOS)}",  "Firma": ""},
        ], ensure_ascii=False))
        row.append(json.dumps([], ensure_ascii=False))                               # Relaciones JSON
        row.append(json.dumps(seg, ensure_ascii=False, default=str))                 # Seguimiento Plan JSON
        # APGAR (6)
        row.extend([apgar_total] + apgar_vals)
        # Extra (17)
        row.extend([
            sector,                           # Rep Sector
            familia,                          # Familia Comp
            direccion,                        # Dir Comp
            members[0]["Nombre y Apellidos"], # Rep Familia
            members[0]["RUT"],                # RUT Rep
            comp_fecha,                       # Fecha Comp
            rep_sector,                       # Firma Funcionario
            members[0]["Nombre y Apellidos"], # Firma Beneficiario
            "",                               # Firma Equipo
            "",                               # Firma Jefe
            evaluador,                        # Firma Evaluador
            egreso_alta,                      # egreso_alta
            egreso_tras,                      # egreso_traslado
            egreso_der,                       # egreso_derivacion
            egreso_aban,                      # egreso_abandono
            fecha_egreso,                     # Fecha Egreso
            random.choice(OBS_POOL),          # Observaciones
            link_drive,                       # Carpeta Digital (Drive)
        ])

        rows.append(row)
        print(f"  [{i+1:02d}/30] {eval_id} — {familia} ({len(members)} integrantes) — {nivel} ({total_pts}pts) [{perfil}]")

    ws_eval.append_rows(rows, value_input_option="USER_ENTERED")
    print(f"\n✅ {len(rows)} familias con grupo familiar completo insertadas.")
    print(f"   Columnas por fila: {len(rows[0])} | RISK_KEYS: {len(RISK_KEYS)}")

if __name__ == "__main__":
    seed_data(30)
