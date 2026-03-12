from fpdf import FPDF
from datetime import date
import pandas as pd
import os

class PDF(FPDF):
    def footer(self):
        self.set_y(-15)
        self.set_font('helvetica', 'I', 8)
        self.cell(0, 10, f'Página {self.page_no()}/{{nb}}', align='C')

def draw_header(pdf, data, title_text="FICHA DE INGRESO", is_blank=False):
    # Logo
    base_dir = os.path.dirname(os.path.abspath(__file__))
    logo_path = os.path.join(base_dir, "NUEVO LOGO.png")
    if os.path.exists(logo_path):
        pdf.image(logo_path, 10, 8, 25)
    else:
        pdf.set_xy(10, 10)
        pdf.set_font('helvetica', 'B', 10)
        pdf.cell(25, 10, "LOGO", border=1, align='C')

    # Title
    pdf.set_font('helvetica', 'B', 12)
    pdf.set_xy(40, 10)
    pdf.cell(0, 5, "ILUSTRE MUNICIPALIDAD DE CHOLCHOL", ln=True, align='C')
    pdf.set_font('helvetica', '', 10)
    pdf.set_x(40)
    pdf.cell(0, 5, "Departamento de Salud | CESFAM Cholchol", ln=True, align='C')
    
    # ID Box
    # User requested compact ID Eval and Fecha
    pdf.set_xy(140, 20)
    pdf.set_font('helvetica', 'B', 9)
    pdf.cell(60, 6, title_text, border=0, align='C', ln=True)
    
    pdf.set_x(140)
    pdf.set_font('helvetica', '', 9)
    # If blank, remove internal borders for a "cleaner" look if that's what "doble linea" meant
    border_val = 1 if not is_blank else 0
    pdf.cell(20, 6, "ID Eval:", border=border_val)
    pdf.cell(40, 6, str(data.get('idEvaluacion', '')), border=border_val, ln=True)
    pdf.set_x(140)
    pdf.cell(20, 6, "Fecha:", border=border_val)
    pdf.cell(40, 6, str(data.get('fechaEvaluacion', '')), border=border_val, ln=True)
    pdf.ln(5)

def generate_pdf_report(data, family_df, plan_df, team_df=None, is_blank=False):
    pdf = PDF()
    pdf.alias_nb_pages()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    draw_header(pdf, data, is_blank=is_blank)
    pdf.ln(15)
    
    # --- 1. IDENTIFICACIÓN ---
    pdf.set_font('helvetica', 'B', 10)
    pdf.cell(0, 6, "1. DATOS DE IDENTIFICACIÓN", ln=True, fill=False)
    pdf.ln(2)
    
    pdf.set_font('helvetica', '', 9)
    # Row 1
    pdf.cell(25, 6, "FAMILIA:", border=0)
    pdf.cell(70, 6, str(data.get('familia', '')), border="B" if not is_blank else 0)
    pdf.cell(5, 6, "")
    pdf.cell(35, 6, "ESTABLECIMIENTO:", border=0)
    pdf.cell(55, 6, str(data.get('establecimiento', '')), border="B" if not is_blank else 0, ln=True)
    pdf.ln(2)
    # Row 2
    pdf.cell(25, 6, "DIRECCIÓN:", border=0)
    pdf.cell(70, 6, str(data.get('direccion', '')), border="B" if not is_blank else 0)
    pdf.cell(5, 6, "")
    pdf.cell(35, 6, "SECTOR:", border=0)
    pdf.cell(55, 6, str(data.get('sector', '')), border="B" if not is_blank else 0, ln=True)
    pdf.ln(2)
    # Row 3 (New)
    pdf.cell(25, 6, "TIPO UNIÓN:", border=0)
    tu = data.get('tipo_union', '')
    if not tu: tu = '________________' if is_blank else 'Casados'
    pdf.cell(70, 6, str(tu), border="B" if not is_blank else 0, ln=True)
    pdf.ln(5)

    # --- 2. GRUPO FAMILIAR ---
    pdf.set_font('helvetica', 'B', 10)
    pdf.set_fill_color(240, 240, 240)
    pdf.set_text_color(0, 0, 0) # Force Black
    pdf.cell(0, 6, "2. GRUPO FAMILIAR", ln=True, fill=True)
    pdf.set_fill_color(255, 255, 255) # Reset
    pdf.ln(2)
    
    # Check if empty (Robust)
    if family_df is not None and len(family_df) > 0:
        # Table Header
        pdf.set_font('helvetica', 'B', 7)
        pdf.set_text_color(0, 0, 0)
        pdf.set_draw_color(0, 0, 0)
        cols = ["Nombre y Apellidos", "RUT", "Género", "Parentesco", "E. Civil", "Nacionalidad", "Etnia", "Ocupacion"]
        w    = [50,                   23,    12,       22,           12,          20,              18,      33]  # 190 total
        
        for i, c in enumerate(cols):
            pdf.cell(w[i], 6, c, border=1, align='C')
        pdf.ln()
        
        # Table Rows
        pdf.set_font('helvetica', '', 7)
        for index, row in family_df.iterrows():
            pdf.cell(w[0], 6, str(row.get("Nombre y Apellidos", ""))[:28], border=1)
            pdf.cell(w[1], 6, str(row.get("RUT", "")), border=1)
            gender_val = str(row.get("Identidad de género", row.get("Sexo", "")))
            # Abbreviate for small column
            gen_abbr = {"Masculino": "M", "Femenino": "F", "No binario": "NB", "Transgénero": "Trans",
                        "Prefiero no decir": "N/D", "Gestación/Aborto": "G"}.get(gender_val, gender_val[:5])
            pdf.cell(w[2], 6, gen_abbr, border=1, align='C')
            pdf.cell(w[3], 6, str(row.get("Parentesco", ""))[:12], border=1)
            pdf.cell(w[4], 6, str(row.get("E. Civil", ""))[:5], border=1, align='C')
            pdf.cell(w[5], 6, str(row.get("Nacionalidad", ""))[:10], border=1)
            etnia_val = str(row.get("Pueblo Originario", row.get("Etnia", "")))
            etnia_val = etnia_val if etnia_val not in ["Ninguno", "nan", ""] else "-"
            pdf.cell(w[6], 6, etnia_val[:10], border=1)
            pdf.cell(w[7], 6, str(row.get("Ocupación", row.get("Ocupacion", "")))[:16], border=1)
            pdf.ln()
    else:
        pdf.set_font('helvetica', 'I', 8)
        pdf.set_text_color(0, 0, 0)
        pdf.cell(0, 6, "Sin integrantes registrados.", ln=True)

    # --- LEYENDA DISCRETA (solo en modo blanco) ---
    if is_blank:
        pdf.ln(4)
        pdf.set_draw_color(180, 180, 180)
        pdf.line(10, pdf.get_y(), 200, pdf.get_y())
        pdf.set_draw_color(0, 0, 0)
        pdf.ln(2)

        # Helper local para imprimir una etiqueta bold + valor normal en la misma linea
        # IMPORTANTE: usar ancho explicito (168) en multi_cell, NO 0
        # porque despues de cell(ln=False) el cursor X esta desplazado
        _LBL_W = 22   # ancho de la etiqueta
        _TXT_W = 168  # 190 (ancho util) - 22 (etiqueta)

        def leyenda_fila(label, texto):
            pdf.set_font('helvetica', 'B', 7)
            pdf.set_text_color(130, 130, 130)
            pdf.cell(_LBL_W, 4, label, ln=False)
            pdf.set_font('helvetica', '', 7)
            pdf.multi_cell(_TXT_W, 4, texto)

        leyenda_fila("GÉNERO:",
            "Masculino, Femenino, No binario, Transgénero, Prefiero no decir, Gestación/Aborto. (G = Gestación)")

        pdf.ln(1)
        leyenda_fila("PARENTESCO:",
            "Jefe/a de Hogar  /  Conyuge/Pareja  /  Hijo/a  /  Hijo/a Gemelo Fraterno  /  "
            "Hijo/a Gemelo Identico  /  Padre/Madre  /  Hermano/a  /  Abuelo/a  /  Nieto/a  /  "
            "Tio/a  /  Sobrino/a  /  Hijo/a Adoptivo/a  /  Otro familiar  /  No familiar")

        pdf.ln(1)
        leyenda_fila("E. CIVIL:",
            "S=Soltero/a   C=Casado/a   Co=Conviviente   D=Divorciado/a   "
            "Sep=Separado/a   V=Viudo/a   F=Fallecido/a")
        pdf.set_font('helvetica', '', 7)
        pdf.set_text_color(130, 130, 130)
        pdf.cell(_LBL_W, 4, "", ln=False)
        pdf.multi_cell(_TXT_W, 4,
            "Espontaneo = Aborto espontaneo (solo cuando Identidad=Gestación)     "
            "Provocado = Aborto provocado (solo cuando Identidad=Gestación)")

        pdf.ln(1)
        leyenda_fila("GESTACION:",
            "Embarazo en curso: E.Civil vacio     "
            "Aborto Espontaneo: E.Civil='Espontaneo'     "
            "Aborto Provocado: E.Civil='Provocado'")

        pdf.ln(1)
        leyenda_fila("ETNIA:",
            "Ninguno  /  Mapuche  /  Aymara  /  Rapa Nui  /  Atacameno (Lickanantay)  /  Quechua  /  "
            "Colla  /  Diaguita  /  Kawesqar  /  Yagan  /  Changos  /  Afrodescendiente  /  Otro")

        pdf.set_text_color(0, 0, 0)
        pdf.set_font('helvetica', '', 9)


    pdf.ln(5)

    # --- 3. FACTORES DE RIESGO (FULL FORM) ---
    pdf.set_font('helvetica', 'B', 10)
    pdf.set_fill_color(240, 240, 240)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 6, "3. PAUTA DE EVALUACIÓN DE RIESGO FAMILIAR", ln=True, fill=True)
    pdf.set_fill_color(255, 255, 255)
    pdf.ln(2)

    def print_risk_table(title, items, color_rgb=None, is_blank=False):
        if color_rgb:
             pdf.set_fill_color(*color_rgb)
        else:
             pdf.set_fill_color(255, 255, 255) # White default
        
        pdf.set_font('helvetica', 'B', 8)
        pdf.cell(0, 5, title, ln=True, border=1, fill=True if color_rgb else False)
        pdf.set_fill_color(255, 255, 255) # Reset
        
        pdf.set_font('helvetica', '', 8)
        # Multi-column layout for items? 
        # Standard form usually lists them. Let's do 2 columns to save space.
        col_width = 95
        
        for i in range(0, len(items), 2):
            # Left Item
            key1, label1 = items[i]
            checked1 = "X" if (not is_blank and data.get(key1) is True) else " "
            pdf.cell(5, 5, f"[{checked1}]", border=0)
            pdf.cell(col_width - 5, 5, label1, border=0)
            
            # Right Item
            if i + 1 < len(items):
                key2, label2 = items[i+1]
                checked2 = "X" if (not is_blank and data.get(key2) is True) else " "
                pdf.cell(5, 5, f"[{checked2}]", border=0)
                pdf.cell(col_width - 5, 5, label2, border=0, ln=True)
            else:
                pdf.ln()

    # TABLA 1
    t1_items = [
        ('t1_vif', "Familia con VIF (física, psicológica, sexual, económica)"),
        ('t1_drogas', "Consumo problema de drogas o dependencia"),
        ('t1_alcohol', "Consumo problema de alcohol (AUDIT > 13)"),
        ('t1_saludMentalDescomp', "Patología salud mental descompensada o sin TTO"),
        ('t1_abusoSexual', "Abuso sexual (sufrido por algún integrante)"),
        ('t1_riesgoBiopsicoGrave', "Adulto mayor y/o niño/a en riesgo biopsicosocial grave"),
        ('t1_epsaRiesgo', "Pauta EPSA (ChCC) con riesgo"),
        ('t1_vulnerabilidadExtrema', "Vulnerabilidad socioeconómica extrema (indigencia)"),
        ('t1_trabajoInfantil', "Trabajo infantil en niños < 14 años")
    ]
    print_risk_table("TABLA 1: FACTORES DE RIESGO MÁXIMO (NO OTORGAN PTS.)", t1_items, (254, 226, 226), is_blank)
    pdf.ln(2)

    # TABLA 2
    t2_items = [
        ('t2_enfermedadGrave', "Enfermedad grave o terminal integrante"),
        ('t2_altoRiesgoHosp', "Paciente con alto riesgo de hospitalizar"),
        ('t2_discapacidad', "Discapacidad física y/o mental (Bartel 35 o menos)"),
        ('t2_saludMentalLeve', "Patología de salud mental leve o moderada"),
        ('t2_judicial', "Conflictos o problemas con la justicia"),
        ('t2_rolesParentales', "Incumplimiento de roles parentales"),
        ('t2_sobrecargaCuidador', "Sobrecarga del cuidador principal"),
        ('t2_conflictosSeveros', "Conflictos familiares severos o crisis de comunicación"),
        ('t2_adultosRiesgo', "Adultos en riesgo biopsicosocial a cargo de niños")
    ]
    print_risk_table("TABLA 2: FACTORES DE RIESGO ALTO (NO OTORGAN PTS.)", t2_items, (255, 237, 213), is_blank)
    pdf.ln(2)

    # TABLA 3
    t3_items = [
        ('t3_patologiaCronica', "Patología crónica descompensada sintomática"),
        ('t3_discapacidadLeve', "Miembro con discapacidad leve/moderada (40-55pts)"),
        ('t3_rezago', "Rezago desarrollo psicomotor"),
        ('t3_madreAdolescente', "Madre adolescente"),
        ('t3_duelo', "Duelo reciente (pérdida de integrante significativo)"),
        ('t3_sinRedApoyo', "Ausencia o escasa red de apoyo social/familiar"),
        ('t3_cesantia', "Cesantía de más de 1 mes del proveedor"),
        ('t3_vulneNoExtrema', "Vulnerabilidad socioeconómica no extrema"),
        ('t3_precariedadLaboral', "Precariedad laboral (temporal/honorarios)"),
        ('t3_hacinamiento', "Hacinamiento (2.5+ personas por dormitorio)"),
        ('t3_entornoInseguro', "Entorno inseguro (delincuencia)"),
        ('t3_adultoSolo', "Adulto mayor que vive solo"),
        ('t3_desercionEscolar', "Deserción o fracaso escolar"),
        ('t3_analfabetismo', "Analfabetismo padre/madre/cuidador"),
        ('t3_escolaridadIncompleta', "Escolaridad básica incompleta padres"),
        ('t3_dificultadAcceso', "Dificultad de acceso a servicios")
    ]
    print_risk_table("TABLA 3: FACTORES DE RIESGO MEDIO (4 PTS. C/U)", t3_items, (254, 249, 195), is_blank)
    pdf.ln(2)

    # TABLA 4
    t4_items = [
        ('t4_monoparental', "Hogar monoparental"),
        ('t4_riesgoCardio', "Riesgo cardiovascular (tabaco, obesidad)"),
        ('t4_contaminacion', "Foco contaminación ambiental cercano"),
        ('t4_higiene', "Deficiencia hábitos higiene"),
        ('t4_sinRecreacion', "Ausencia prácticas recreación"),
        ('t4_sinEspaciosSeguros', "Ausencia espacios seguros recreación"),
        ('t4_endeudamiento', "Endeudamiento familiar elevado (>40%)"),
        ('t4_serviciosIncompletos', "Servicios básicos incompletos/inadecuados")
    ]
    print_risk_table("TABLA 4: FACTORES DE RIESGO BAJO (3 PTS. C/U)", t4_items, (220, 252, 231), is_blank)
    pdf.ln(2)

    # TABLA 5
    t5_items = [
        ('t5_lactancia', "Lactancia materna exclusiva/complementaria"),
        ('t5_habitos', "Hábitos saludables (actividad física, alim.)"),
        ('t5_redesSociales', "Presencia redes sociales/comunitarias"),
        ('t5_redFamiliar', "Presencia red apoyo familiar"),
        ('t5_comunicacion', "Habilidades comunicacionales (afecto)"),
        ('t5_recursosSuficientes', "Recursos socioeconómicos suficientes"),
        ('t5_resiliencia', "Resiliencia (sobreponerse a crisis)"),
        ('t5_viviendaAdecuada', "Vivienda adecuada")
    ]
    print_risk_table("TABLA 5: FACTORES PROTECTORES (NO OTORGAN PTS.)", t5_items, (219, 234, 254), is_blank)
    
    # Score Box
    pdf.ln(3)
    pdf.set_font('helvetica', 'B', 10)
    pdf.set_text_color(0, 0, 0)
    
    # Detailed Breakdown
    pdf.cell(0, 6, "DETALLE PUNTAJE:", ln=True)
    pdf.set_font('helvetica', '', 9)
    
    c_t3 = data.get('count_t3', 0)
    s_t3 = data.get('score_medium', 0)
    c_t4 = data.get('count_t4', 0)
    s_t4 = data.get('score_low', 0)
    total = data.get('total_points', 0)
    level = data.get('level', 'SIN RIESGO')

    if is_blank:
        pdf.set_font('helvetica', '', 8)
        pdf.set_text_color(80, 80, 80)
        pdf.cell(0, 5, "T3 (Riesgo Medio, 4 pts c/u): ____ factores x 4 = ____ pts.", ln=True)
        pdf.cell(0, 5, "T4 (Riesgo Bajo,  3 pts c/u): ____ factores x 3 = ____ pts.", ln=True)
        pdf.set_text_color(0, 0, 0)
    else:
        pdf.set_font('helvetica', '', 8)
        pdf.set_text_color(80, 80, 80)
        pdf.cell(0, 5,
            f"Tabla 3 (Riesgo Medio, 4 pts c/u): {c_t3} factores marcados x 4 = {s_t3} pts.", ln=True)
        pdf.cell(0, 5,
            f"Tabla 4 (Riesgo Bajo,  3 pts c/u): {c_t4} factores marcados x 3 = {s_t4} pts.", ln=True)
        pdf.cell(0, 5,
            f"PUNTAJE TOTAL = {s_t3} + {s_t4} = {total} pts.  ->  Clasificación: {level}", ln=True)
        pdf.set_text_color(0, 0, 0)
    pdf.ln(1)

    pdf.set_font('helvetica', 'B', 10)
    pdf.cell(40, 8, "PUNTAJE TOTAL:", border=1 if not is_blank else 0, align='R')
    pdf.cell(20, 8, str(data.get('total_points', 0)), border=1 if not is_blank else 0, align='C')
    pdf.cell(40, 8, "NIVEL DE RIESGO:", border=1 if not is_blank else 0, align='R')
    level_text = str(data.get('level', 'SIN RIESGO')) if not is_blank else '____________________'
    pdf.cell(50, 8, level_text, border=1 if not is_blank else 0, align='C')
    pdf.ln(8)

    # Evaluator Sig Area — immediately after PUNTAJE TOTAL
    pdf.ln(10)
    pdf.set_font('helvetica', '', 9)
    if not is_blank:
        pdf.cell(100, 5, "", border=0)
        pdf.cell(80, 5, "____________________________________", border=0, align='C', ln=True)
    
    pdf.cell(100, 5, "", border=0)
    sig_eval = data.get('sig_evaluador_input', '') or data.get('evaluador_nombre', '')
    if is_blank: sig_eval = '____________________________________'
    pdf.cell(80, 5, f"Evaluador: {sig_eval}", border=0, align='C', ln=True)
    pdf.ln(5)

    # =====================================================================
    # PÁGINA 2: INSTRUMENTOS COMPLEMENTARIOS — APGAR FAMILIAR
    # =====================================================================
    pdf.add_page()
    draw_header(pdf, data, "INSTRUMENTOS COMPLEMENTARIOS", is_blank=is_blank)
    pdf.ln(8)

    # --- APGAR FAMILIAR ---
    pdf.set_font('helvetica', 'B', 11)
    pdf.set_fill_color(220, 230, 255)
    pdf.cell(0, 8, "INSTRUMENTO 1: APGAR FAMILIAR", ln=True, fill=True, border=1, align='C')
    pdf.ln(3)

    pdf.set_font('helvetica', 'I', 9)
    pdf.set_text_color(80, 80, 80)
    pdf.multi_cell(0, 4,
        "El APGAR Familiar (Smilkstein, 1978) evalua la percepcion subjetiva del funcionamiento familiar "
        "desde la perspectiva de un integrante. Mide cinco dimensiones: "
        "Adaptacion (A), Participacion (P), Crecimiento (G), Afecto (A) y Resolucion (R)."
    )
    pdf.set_text_color(0, 0, 0)
    pdf.ln(4)

    # Cabecera en dos filas para evitar desborde
    pdf.set_font('helvetica', 'B', 8)
    pdf.set_fill_color(245, 245, 245)
    pdf.cell(140, 6, "Pregunta / Componente", border=1, fill=True)
    pdf.cell(50, 6, "Puntaje", border=1, fill=True, align='C', ln=True)
    pdf.cell(140, 5, "", border=0)
    pdf.cell(50, 5, "0=Casi nunca  1=A veces  2=Casi siempre", border=0, align='C', ln=True)

    apgar_questions = [
        ("A - Adaptación: ¿Está satisfecho con la ayuda que recibe de su familia cuando tiene problemas?", 'apgar_a1'),
        ("P - Participación: ¿Está satisfecho con la forma en que su familia discute problemas y comparte soluciones?", 'apgar_a2'),
        ("G - Crecimiento: ¿Siente que su familia acepta y apoya sus nuevos intereses o cambios?", 'apgar_a3'),
        ("A - Afecto: ¿Está satisfecho con la forma en que su familia expresa afecto y responde a sus emociones?", 'apgar_a4'),
        ("R - Resolución: ¿Está satisfecho con la cantidad de tiempo que comparte con su familia?", 'apgar_a5'),
    ]

    pdf.set_font('helvetica', '', 8)
    for q_text, q_key in apgar_questions:
        val = data.get(q_key, 0)
        checked_apgar = str(val) if not is_blank else "  "
        pdf.cell(140, 7, q_text, border=1)
        pdf.cell(50, 7, checked_apgar, border=1, align='C', ln=True)

    apgar_total = data.get('apgar_total', 0)

    if is_blank:
        apgar_label = "_______________________"
        apgar_color = (0, 0, 0)
    else:
        try:
            val_num = int(apgar_total)
        except (ValueError, TypeError):
            val_num = 0
        if val_num >= 7:
            apgar_label = "FAMILIA FUNCIONAL (7-10 pts)"
            apgar_color = (22, 101, 52)
        elif 4 <= val_num <= 6:
            apgar_label = "DISFUNCIÓN LEVE (4-6 pts)"
            apgar_color = (133, 77, 14)
        else:
            apgar_label = "DISFUNCIÓN SEVERA (0-3 pts)"
            apgar_color = (153, 27, 27)

    pdf.ln(3)
    pdf.set_font('helvetica', 'B', 10)
    pdf.set_text_color(*apgar_color)
    pdf.cell(100, 7, f"TOTAL APGAR: {apgar_total} puntos", border=0)
    pdf.cell(90, 7, f"INTERPRETACIÓN: {apgar_label}", border=0, align='R', ln=True)
    pdf.set_text_color(0, 0, 0)
    pdf.ln(5)

    # Interpretación APGAR
    pdf.set_font('helvetica', 'B', 8)
    pdf.set_fill_color(240, 240, 240)
    pdf.cell(0, 6, "TABLA DE INTERPRETACIÓN APGAR", ln=True, fill=True)
    pdf.set_font('helvetica', '', 8)
    pdf.cell(60, 6, "7 - 10 pts", border=1, align='C')
    pdf.cell(130, 6, "Familia Funcional - Funcionamiento familiar adecuado.", border=1, ln=True)
    pdf.cell(60, 6, "4 - 6 pts", border=1, align='C')
    pdf.cell(130, 6, "Disfuncion Leve - Dificultades moderadas que requieren seguimiento.", border=1, ln=True)
    pdf.cell(60, 6, "0 - 3 pts", border=1, align='C')
    pdf.cell(130, 6, "Disfuncion Severa - Alteracion grave del funcionamiento familiar.", border=1, ln=True)
    pdf.ln(8)

    # Observaciones APGAR
    pdf.set_font('helvetica', 'B', 9)
    pdf.cell(0, 6, "OBSERVACIONES / INTERPRETACIÓN CLÍNICA:", ln=True)
    pdf.set_font('helvetica', '', 9)
    if is_blank:
        for _ in range(4):
            pdf.cell(0, 7, "", border="B", ln=True)
            pdf.ln(2)
    else:
        pdf.multi_cell(0, 7, data.get('observaciones_apgar', ''))
    pdf.ln(5)

    # =====================================================================
    # INSTRUMENTO 2: GENOGRAMA FAMILIAR
    # =====================================================================
    pdf.add_page()
    draw_header(pdf, data, "INSTRUMENTO 2: GENOGRAMA", is_blank=is_blank)
    pdf.ln(8)
    pdf.set_font('helvetica', 'B', 11)
    pdf.set_fill_color(220, 255, 230)
    pdf.cell(0, 8, "INSTRUMENTO 2: GENOGRAMA FAMILIAR", ln=True, fill=True, border=1, align='C')
    pdf.ln(3)

    pdf.set_font('helvetica', 'I', 9)
    pdf.set_text_color(80, 80, 80)
    if is_blank:
        pdf.multi_cell(0, 4,
            "El Genograma (Murray Bowen, 1978) es una representacion grafica de la estructura y "
            "dinamica de una familia a traves de al menos tres generaciones. Permite visualizar patrones de "
            "relaciones, enfermedades hereditarias, ciclos vitales y dinamicas familiares."
        )
    else:
        pdf.multi_cell(0, 4,
            "El Genograma (Murray Bowen, 1978) es una representacion grafica de la estructura y "
            "dinamica de una familia a traves de al menos tres generaciones. Permite visualizar patrones de "
            "relaciones, enfermedades hereditarias, ciclos vitales y dinamicas familiares. "
            "Es generado automaticamente por el sistema a partir del Grupo Familiar registrado."
        )
    pdf.set_text_color(0, 0, 0)
    pdf.ln(4)

    # Simbología
    pdf.set_font('helvetica', 'B', 8)
    pdf.set_fill_color(240, 240, 240)
    pdf.cell(0, 6, "SIMBOLOGÍA BÁSICA DEL GENOGRAMA", ln=True, fill=True)
    pdf.set_font('helvetica', '', 8)
    simbolos = [
        ("[ ] (cuadrado)", "Hombre"),
        ("( ) (circulo)", "Mujer"),
        ("<> (rombo)", "Identidad No Binaria / Transgénero / Otra"),
        (r"/\ (triangulo)", "Gestacion / Embarazo"),
        (r"/\+X (triangulo con X)", "Aborto Espontaneo"),
        (r"/\+* (triangulo con punto)", "Aborto Provocado"),
        ("Doble borde", "Persona indice del caso (Resp)"),
        ("Borde rojo", "Enfermedad cronica (Cron)"),
        ("Simbolo relleno", "Fallecido/a"),
        ("=== linea doble", "Matrimonio"),
        ("--- linea simple", "Convivencia"),
        ("= / = linea cortada", "Separacion/Divorcio"),
    ]
    col_w = [60, 130]
    for sym, desc in simbolos:
        pdf.cell(col_w[0], 6, sym, border=1)
        pdf.cell(col_w[1], 6, desc, border=1, ln=True)
    pdf.ln(4)

    pdf.set_font('helvetica', 'I', 8)
    pdf.set_text_color(100, 100, 100)
    if is_blank:
        pdf.multi_cell(0, 4,
            "Instrucciones: Utilice la simbologia de arriba para dibujar el genograma familiar "
            "en el espacio en blanco de abajo. Incluya al menos tres generaciones cuando sea posible."
        )
    else:
        pdf.multi_cell(0, 4,
            "NOTA: El genograma ha sido generado automaticamente por el sistema "
            "a partir de los datos del Grupo Familiar registrado."
        )
    pdf.set_text_color(0, 0, 0)
    pdf.ln(4)

    # Espacio para genograma manual
    pdf.set_font('helvetica', 'B', 9)
    pdf.cell(0, 6, "ESPACIO PARA DIBUJO DEL GENOGRAMA:", ln=True)
    y_start_box = pdf.get_y()
    pdf.rect(pdf.get_x(), y_start_box, 190, 80)
    pdf.ln(85)

    # =====================================================================
    # INSTRUMENTO 3: ECOMAPA FAMILIAR
    # =====================================================================
    pdf.add_page()
    draw_header(pdf, data, "INSTRUMENTO 3: ECOMAPA", is_blank=is_blank)
    pdf.ln(8)
    pdf.set_font('helvetica', 'B', 11)
    pdf.set_fill_color(255, 235, 205)
    pdf.cell(0, 8, "INSTRUMENTO 3: ECOMAPA FAMILIAR", ln=True, fill=True, border=1, align='C')
    pdf.ln(3)

    pdf.set_font('helvetica', 'I', 9)
    pdf.set_text_color(80, 80, 80)
    if is_blank:
        pdf.multi_cell(0, 4,
            "El Ecomapa (Ann Hartman, 1978) es una representacion grafica de las relaciones "
            "y recursos que una familia tiene con sistemas externos (instituciones, redes, comunidad). "
            "Permite identificar redes de apoyo, recursos disponibles e identificar areas de aislamiento."
        )
    else:
        pdf.multi_cell(0, 4,
            "El Ecomapa (Ann Hartman, 1978) es una representacion grafica de las relaciones "
            "y recursos que una familia tiene con sistemas externos (instituciones, redes, comunidad). "
            "Permite identificar redes de apoyo, recursos disponibles e identificar areas de aislamiento. "
            "Es generado automaticamente por el sistema segun los sistemas vinculados."
        )
    pdf.set_text_color(0, 0, 0)
    pdf.ln(4)

    pdf.set_font('helvetica', 'B', 8)
    pdf.set_fill_color(240, 240, 240)
    pdf.cell(0, 6, "SISTEMAS EXTERNOS Y TIPO DE VINCULO", ln=True, fill=True)
    pdf.set_font('helvetica', '', 8)
    sistemas = [
        ("CESFAM", "Sistema de salud primaria"),
        ("RELIGION", "Comunidades religiosas o espirituales"),
        ("TRABAJO", "Empleadores y entornos laborales"),
        ("ESCUELA", "Establecimientos educativos"),
        ("COMUNIDAD", "Redes comunitarias, juntas de vecinos"),
        ("JUSTICIA", "Instituciones judiciales o policiales"),
        ("RED FAMILIAR", "Familia extensa fuera del hogar"),
        ("VECINOS", "Entorno vecinal inmediato"),
        ("OTRO", "Otros sistemas relevantes"),
    ]
    for sis, desc in sistemas:
        # Fila 1: Sistema + Descripcion
        pdf.cell(50, 5, sis, border='LRT', align='C')
        pdf.cell(140, 5, desc, border='LRT', ln=True)
        # Fila 2: Vinculo (ocupa toda la fila debajo)
        pdf.cell(50, 5, "", border='LRB')
        pdf.cell(140, 5, "Vinculo: [ ] Reciproco  [ ] Hacia Familia  [ ] Desde Familia  [ ] Sin flujo", border='LRB', ln=True)
    pdf.ln(4)

    pdf.set_font('helvetica', 'I', 8)
    pdf.set_text_color(100, 100, 100)
    if is_blank:
        pdf.multi_cell(0, 4,
            "Instrucciones: Marque con X el tipo de vinculo para cada sistema externo "
            "que tenga relacion con la familia. Utilice el espacio de abajo para dibujar "
            "el ecomapa con los sistemas seleccionados y su familia al centro."
        )
    else:
        pdf.multi_cell(0, 4,
            "NOTA: El ecomapa ha sido generado automaticamente por el sistema "
            "segun los sistemas vinculados registrados en la vista Analisis Familiar."
        )
    pdf.set_text_color(0, 0, 0)
    pdf.ln(4)

    # Espacio para ecomapa manual
    pdf.set_font('helvetica', 'B', 9)
    pdf.cell(0, 6, "ESPACIO PARA DIBUJO DEL ECOMAPA:", ln=True)
    y_start_box2 = pdf.get_y()
    pdf.rect(pdf.get_x(), y_start_box2, 190, 90)
    pdf.ln(95)


    # --- 4. PLAN INTERVENCIÓN (OTRA PÁGINA) ---
    pdf.add_page()
    draw_header(pdf, data, "PLAN DE TRABAJO", is_blank=is_blank)
    pdf.ln(10)
    
    pdf.set_font('helvetica', 'B', 10)
    pdf.set_fill_color(240, 240, 240)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 6, "4. PLAN DE INTERVENCIÓN", ln=True, fill=True)
    pdf.set_fill_color(255, 255, 255)
    pdf.ln(2)

    if plan_df is not None and len(plan_df) > 0:
        pdf.set_font('helvetica', 'B', 8)
        pdf.set_text_color(0, 0, 0)
        pdf.set_draw_color(0, 0, 0)
        # Cols: Objetivo, Actividad, Fecha Prog, Responsable, Fecha Real, Evaluación
        cols = ["Objetivo", "Actividad", "Fecha P.", "Responsable", "Fecha R.", "Evaluación"]
        w = [40, 45, 20, 30, 20, 35] # ~190
        
        for i, c in enumerate(cols):
            pdf.cell(w[i], 6, c, border=1, align='C')
        pdf.ln()

        pdf.set_font('helvetica', '', 8)
        for index, row in plan_df.iterrows():
            f_prog = str(row.get("Fecha Prog", ""))
            if " 00:00:00" in f_prog: f_prog = f_prog.split(" ")[0]
            
            f_real = str(row.get("Fecha Real", ""))
            if " 00:00:00" in f_real: f_real = f_real.split(" ")[0]

            pdf.cell(w[0], 6, str(row.get("Objetivo", "")), border=1)
            pdf.cell(w[1], 6, str(row.get("Actividad", "")), border=1)
            pdf.cell(w[2], 6, f_prog, border=1)
            pdf.cell(w[3], 6, str(row.get("Responsable", "")), border=1)
            pdf.cell(w[4], 6, f_real, border=1)
            pdf.cell(w[5], 6, str(row.get("Evaluación", "")), border=1)
            pdf.ln()
    else:
        pdf.set_font('helvetica', 'I', 8)
        pdf.set_text_color(0, 0, 0)
        pdf.cell(0, 6, "Sin plan registrado.", ln=True)
    
    pdf.ln(5)

    # --- OBSERVACIONES ---
    pdf.set_font('helvetica', 'B', 10)
    pdf.set_fill_color(240, 240, 240)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 6, "OBSERVACIONES", ln=True, fill=True)
    pdf.set_fill_color(255, 255, 255)
    pdf.ln(2)
    
    obs = str(data.get('observaciones', ''))
    if obs:
        pdf.set_font('helvetica', '', 9)
        pdf.multi_cell(0, 5, obs)
    else:
        pdf.set_font('helvetica', 'I', 9)
        pdf.cell(0, 5, "Sin observaciones.", ln=True)
    
    # Link carpeta digital (Drive)
    link_drive = str(data.get('link_drive', ''))
    if link_drive:
        pdf.set_font('helvetica', 'I', 7)
        pdf.set_text_color(0, 0, 200)
        pdf.cell(0, 5, f"Carpeta Digital: {link_drive}", ln=True)
        pdf.set_text_color(0, 0, 0)
    
    pdf.ln(4)

    # --- SEGUIMIENTO DEL PLAN ---
    pdf.set_font('helvetica', 'B', 10)
    pdf.set_fill_color(230, 240, 255)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 6, "SEGUIMIENTO DEL PLAN DE INTERVENCIÓN", ln=True, fill=True)
    pdf.set_fill_color(255, 255, 255)
    pdf.ln(2)

    if plan_df is not None and len(plan_df) > 0:
        pdf.set_font('helvetica', 'B', 7)
        seg_cols = ["Objetivo", "Actividad", "Estado", "F. Seguimiento", "Obs. Seguimiento"]
        seg_w    = [52, 48, 28, 24, 38]  # 190 total
        for i, c in enumerate(seg_cols):
            pdf.cell(seg_w[i], 8, c, border=1, align='C')
        pdf.ln()

        pdf.set_font('helvetica', '', 7)
        for _, row in plan_df.iterrows():
            estado_val = str(row.get("Estado", ""))
            f_seg = str(row.get("F. Seguimiento", ""))
            if " 00:00:00" in f_seg: f_seg = f_seg.split(" ")[0]
            obs_seg = str(row.get("Obs. Seguimiento", ""))
            obj_val = str(row.get("Objetivo", ""))
            act_val = str(row.get("Actividad", ""))
            pdf.cell(seg_w[0], 9, obj_val[:26], border=1)
            pdf.cell(seg_w[1], 9, act_val[:24], border=1)
            pdf.cell(seg_w[2], 9, estado_val[:12], border=1, align='C')
            pdf.cell(seg_w[3], 9, f_seg[:10], border=1, align='C')
            pdf.cell(seg_w[4], 9, obs_seg[:20], border=1)
            pdf.ln()
    else:
        pdf.set_font('helvetica', 'I', 8)
        pdf.cell(0, 6, "Sin seguimiento registrado.", ln=True)

    pdf.ln(5)

    # --- FIRMAS EQUIPO (Dynamic) ---
    # --- FIRMAS EQUIPO (Table Format) ---
    pdf.ln(10) # Space before section
    
    # Table Header
    pdf.set_font('helvetica', 'B', 8)
    # Col Widths: [Name Col, Signature Col]
    w_sig = [100, 70] 
    
    pdf.cell(w_sig[0], 6, "NOMBRES Y FIRMAS EQUIPO SALUD PARTICIPANTE", border=1, align='C')
    pdf.cell(w_sig[1], 6, "FIRMA", border=1, align='C', ln=True)
    
    if team_df is not None and len(team_df) > 0:
        pdf.set_font('helvetica', '', 8)
        
        for index, row in team_df.iterrows():
            # Try new column first
            content = str(row.get("Nombre y Profesión", ""))
            
            # Fallback for old structure if needed
            if not content or content == "nan":
                 n = str(row.get("Nombre", ""))
                 c = str(row.get("Cargo", ""))
                 if n or c:
                     content = f"{n}\n({c})"
            
            # Row height
            h_row = 20
            
            # Save current position
            x_start = pdf.get_x()
            y_start = pdf.get_y()
            
            # Check page break
            if y_start + h_row > 270: 
                pdf.add_page()
                y_start = pdf.get_y()
                # Re-draw header if needed (optional, keeping simple)
            
            # Col 1: Name + Cargo (Vertically centered roughly)
            pdf.cell(w_sig[0], h_row, "", border=1) # Box
            
            # Print text inside
            pdf.set_xy(x_start + 2, y_start + 5)
            pdf.multi_cell(w_sig[0]-4, 4, content, align='L')
            
            # Col 2: Empty Signature Box
            pdf.set_xy(x_start + w_sig[0], y_start)
            pdf.cell(w_sig[1], h_row, "", border=1, ln=True)
            
    else:
        # Empty row placeholder
        pdf.cell(w_sig[0], 20, "(Sin integrantes)", border=1, align='C')
        pdf.cell(w_sig[1], 20, "", border=1, ln=True)

    pdf.ln(10)

    # Jefe Equipo (Separate)
    if pdf.get_y() > 250: pdf.add_page()
    
    pdf.ln(15)
    
    y = pdf.get_y()
    # If not blank, draw a line for signature. If blank, the underscores are the line.
    if not is_blank:
        pdf.line(60, y, 150, y) # Centered line
    
    pdf.set_xy(60, y+2)
    pdf.set_font('helvetica', '', 9)
    # Name from input
    sig_jefe_val = data.get('sig_jefe','')
    if is_blank and not sig_jefe_val: sig_jefe_val = "____________________________________"
    pdf.multi_cell(90, 4, f"{sig_jefe_val}", align='C')
    
    # Title below name
    pdf.set_x(60)
    pdf.set_font('helvetica', 'B', 8)
    pdf.multi_cell(90, 4, "JEFE EQUIPO DE CABECERA", align='C')

    pdf.ln(10)
    
    # --- 5. COMPROMISO Y FIRMAS ---
    pdf.set_font('helvetica', 'B', 10)
    pdf.set_fill_color(240, 240, 240)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 6, "5. COMPROMISO DE TRABAJO CONJUNTO", ln=True, fill=True)
    pdf.set_fill_color(255, 255, 255)
    pdf.ln(5)
    
    pdf.set_font('helvetica', '', 9)
    pdf.set_text_color(0, 0, 0)

    def _v(key, blank="__________________________"):
        v = str(data.get(key, "" if not is_blank else blank)).strip()
        return v if v else blank

    # Build inline paragraph with underlined fill-in slots
    # We use write() calls to mix normal and underlined segments
    def write_plain(txt):
        pdf.set_font('helvetica', '', 9)
        pdf.write(5.5, txt)

    def write_blank(val, width_chars=28):
        """Write a value (or underscores) with underline border."""
        pdf.set_font('helvetica', '', 9)
        display = val if (val and val != "__________________________") else ("_" * width_chars)
        pdf.write(5.5, display)

    # Line 1: sector + rep equipo
    write_plain("El equipo de cabecera del sector ")
    write_blank(_v('comp_sector', '_______'), 10)
    write_plain(", representado por don(ña) ")
    write_blank(_v('comp_rep_sector', '________________________________'), 30)
    pdf.ln(6)

    # Line 2: familia + direccion
    write_plain("y la familia ")
    write_blank(_v('comp_familia', '________________________'), 22)
    write_plain(", domiciliada en ")
    write_blank(_v('comp_dir', '____________________________________'), 35)
    pdf.ln(6)

    # Line 3: rep familia + rut
    write_plain("representada por don(ña) ")
    write_blank(_v('comp_rep_fam', '________________________________'), 30)
    write_plain("  RUT N° ")
    write_blank(_v('comp_rut', '___________________'), 18)
    pdf.ln(6)

    pdf.ln(3)
    pdf.set_font('helvetica', '', 8)
    pdf.set_text_color(80, 80, 80)
    pdf.multi_cell(0, 4,
        "Mediante el presente documento manifiestan el acuerdo de ejecutar el Plan de Trabajo "
        "elaborado en conjunto con el equipo de salud, con fecha de entrada en vigencia:")
    pdf.set_text_color(0, 0, 0)
    pdf.ln(2)

    fecha_comp_val = _v('comp_fecha', '___/___/______')
    write_plain("Fecha de entrada en vigencia: ")
    write_blank(fecha_comp_val, 14)
    pdf.ln(8)
    
    # Firmas Compromiso
    pdf.ln(25) # More space for signing
    y = pdf.get_y()
    pdf.line(20, y, 90, y)
    
    pdf.line(110, y, 180, y)
    
    pdf.set_xy(20, y+2)
    pdf.cell(70, 5, f"Nombre Funcionario Firmante: {data.get('sig_func','')}", align='C')
    pdf.set_xy(110, y+2)
    pdf.cell(70, 5, f"Beneficiario Firmante: {data.get('sig_benef','')}", align='C')
    
    pdf.ln(15)
    
    # --- FOOTER / EGRESO ---
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(2)
    pdf.set_font('helvetica', 'B', 9)
    pdf.cell(30, 6, "FECHA EGRESO:", border=0)
    pdf.set_font('helvetica', '', 9)
    pdf.cell(30, 6, str(data.get('fechaEgreso', '') if data.get('fechaEgreso') else "___/___/___"), border=0)
    
    pdf.set_font('helvetica', 'B', 9)
    pdf.cell(20, 6, "ESTADO:", border=0)
    
    # Checkbox style for state
    states = [
        ("Alta", data.get('egreso_alta')),
        ("Traslado", data.get('egreso_traslado')),
        ("Derivación", data.get('egreso_derivacion')),
        ("Abandono", data.get('egreso_abandono'))
    ]
    
    pdf.set_font('helvetica', '', 9)
    for label, val in states:
        chk = "X" if val else " "
        pdf.cell(25, 6, f"[{chk}] {label}", border=0)
        
    pdf.ln()

    return bytes(pdf.output())

def generate_blank_pdf():
    """Genera un archivo PDF con la pauta en blanco para llenado manual."""
    # Data con campos vacíos y placeholders para líneas
    l = "____________________________________"
    blank_data = {
        'idEvaluacion': '______________',
        'fechaEvaluacion': '______________',
        'familia': l,
        'direccion': l,
        'establecimiento': l,
        'sector': '________________',
        'parentesco': '________________',
        'programa_unidad': '________________',
        'total_points': '___',
        'level': '_______________',
        'tipo_union': '________________',
        'evaluador_nombre': l,
        'apgar_total': '___',
        'apgar_a1': 0, 'apgar_a2': 0, 'apgar_a3': 0, 'apgar_a4': 0, 'apgar_a5': 0,
        'observaciones': '\n' * 5,
        'sig_jefe': l
    }
    
    # Dataframes vacíos con filas en blanco para que se vean las tablas
    import pandas as pd
    blank_family = pd.DataFrame([{"Nombre y Apellidos": "", "RUT": "", "Identidad de género": "", "Pueblo Originario": "", "Nacionalidad": "", "Parentesco": "", "E. Civil": "", "Ocupacion": ""}] * 10)
    blank_plan = pd.DataFrame([{"Objetivo": "", "Actividad": "", "Fecha Prog": "", "Responsable": "", "Fecha Real": "", "Evaluación": "", "Estado": "", "F. Seguimiento": "", "Obs. Seguimiento": ""}] * 5)
    
    # Equipo salud en blanco
    blank_team = pd.DataFrame([{"Nombre y Profesión": "", "Firma": ""}] * 5)
    
    return generate_pdf_report(blank_data, blank_family, blank_plan, team_df=blank_team, is_blank=True)
