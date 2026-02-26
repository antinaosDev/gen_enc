from fpdf import FPDF
from datetime import date
import pandas as pd
import os

class PDF(FPDF):
    def footer(self):
        self.set_y(-15)
        self.set_font('helvetica', 'I', 8)
        self.cell(0, 10, f'Página {self.page_no()}/{{nb}}', align='C')

def generate_pdf_report(data, family_df, plan_df, team_df=None):
    pdf = PDF()
    pdf.alias_nb_pages()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    # --- HEADER ---
    pdf.set_font('helvetica', 'B', 12)
    
    # Logo
    logo_path = r"D:\PROYECTOS PROGRAMACIÓN\ANTIGRAVITY_PROJECTS\encuesta_riesgo\NUEVO LOGO.png"
    if os.path.exists(logo_path):
        pdf.image(logo_path, 10, 8, 25)
    else:
        pdf.set_xy(10, 10)
        pdf.cell(25, 10, "LOGO", border=1, align='C')

    # Title
    pdf.set_xy(40, 10)
    pdf.cell(0, 5, "ILUSTRE MUNICIPALIDAD DE CHOLCHOL", ln=True, align='C')
    pdf.set_font('helvetica', '', 10)
    pdf.set_x(40)
    pdf.cell(0, 5, "Departamento de Salud | CESFAM Cholchol", ln=True, align='C')
    
    # ID Box
    pdf.set_xy(150, 20)
    pdf.set_font('helvetica', 'B', 10)
    pdf.cell(50, 6, "FICHA DE INGRESO", border=0, align='C', ln=True)
    pdf.set_x(150)
    pdf.set_font('helvetica', '', 9)
    pdf.cell(20, 6, "ID Eval:", border=1)
    pdf.cell(30, 6, str(data.get('idEvaluacion', '')), border=1, ln=True)
    pdf.set_x(150)
    pdf.cell(20, 6, "Fecha:", border=1)
    pdf.cell(30, 6, str(data.get('fechaEvaluacion', '')), border=1)

    pdf.ln(15)
    
    # --- 1. IDENTIFICACIÓN ---
    pdf.set_font('helvetica', 'B', 10)
    pdf.cell(0, 6, "1. DATOS DE IDENTIFICACIÓN", ln=True, fill=False)
    pdf.ln(2)
    
    pdf.set_font('helvetica', '', 9)
    # Row 1
    pdf.cell(25, 6, "FAMILIA:", border=0)
    pdf.cell(70, 6, str(data.get('familia', '')), border="B")
    pdf.cell(5, 6, "")
    pdf.cell(35, 6, "ESTABLECIMIENTO:", border=0)
    pdf.cell(55, 6, str(data.get('establecimiento', '')), border="B", ln=True)
    pdf.ln(2)
    # Row 2
    pdf.cell(25, 6, "DIRECCIÓN:", border=0)
    pdf.cell(70, 6, str(data.get('direccion', '')), border="B")
    pdf.cell(5, 6, "")
    pdf.cell(35, 6, "SECTOR:", border=0)
    pdf.cell(55, 6, str(data.get('sector', '')), border="B", ln=True)
    pdf.ln(2)
    # Row 3 (New)
    pdf.cell(25, 6, "TIPO UNIÓN:", border=0)
    pdf.cell(70, 6, str(data.get('tipo_union', 'Casados')), border="B", ln=True)
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
        pdf.set_font('helvetica', 'B', 8)
        pdf.set_text_color(0, 0, 0)
        pdf.set_draw_color(0, 0, 0)
        cols = ["Nombre y Apellidos", "RUT", "Sexo", "Parentesco", "E. Civil", "Ocupación"]
        w = [55, 25, 10, 30, 15, 55] # Total ~190
        
        for i, c in enumerate(cols):
            pdf.cell(w[i], 6, c, border=1, align='C')
        pdf.ln()
        
        # Table Rows
        pdf.set_font('helvetica', '', 8)
        for index, row in family_df.iterrows():
            pdf.cell(w[0], 6, str(row.get("Nombre y Apellidos", "")), border=1)
            pdf.cell(w[1], 6, str(row.get("RUT", "")), border=1)
            pdf.cell(w[2], 6, str(row.get("Sexo", "")), border=1)
            pdf.cell(w[3], 6, str(row.get("Parentesco", "")), border=1)
            pdf.cell(w[4], 6, str(row.get("E. Civil", "")), border=1)
            pdf.cell(w[5], 6, str(row.get("Ocupación", "")), border=1)
            pdf.ln()
    else:
        pdf.set_font('helvetica', 'I', 8)
        pdf.set_text_color(0, 0, 0)
        pdf.cell(0, 6, "Sin integrantes registrados.", ln=True)

    pdf.ln(5)

    # --- 3. FACTORES DE RIESGO (FULL FORM) ---
    pdf.set_font('helvetica', 'B', 10)
    pdf.set_fill_color(240, 240, 240)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 6, "3. PAUTA DE EVALUACIÓN DE RIESGO FAMILIAR", ln=True, fill=True)
    pdf.set_fill_color(255, 255, 255)
    pdf.ln(2)

    def print_risk_table(title, items, color_rgb=None):
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
            checked1 = "X" if data.get(key1) is True else " "
            pdf.cell(5, 5, f"[{checked1}]", border=0)
            pdf.cell(col_width - 5, 5, label1, border=0)
            
            # Right Item
            if i + 1 < len(items):
                key2, label2 = items[i+1]
                checked2 = "X" if data.get(key2) is True else " "
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
    print_risk_table("TABLA 1: FACTORES DE RIESGO MÁXIMO (NO OTORGAN PTS.)", t1_items, (254, 226, 226))
    pdf.ln(2)

    # TABLA 2
    t2_items = [
        ('t2_enfermedadGrave', "Enfermedad grave o terminal integrante"),
        ('t2_altoRiesgoHosp', "Paciente con alto riesgo de hospitalizar"),
        ('t2_discapacidad', "Discapacidad física y/o mental (Bartel 35 o menos)"),
        ('t2_saludMentalLeve', "Patología de salud mental leve o moderada"),
        ('t2_judicial', "Conflictos o problemas con la justicia"),
        ('t2_rolesParentales', "Incumplimiento de roles parentales"),
        ('t2_adultosRiesgo', "Adultos en riesgo biopsicosocial a cargo de niños")
    ]
    print_risk_table("TABLA 2: FACTORES DE RIESGO ALTO (NO OTORGAN PTS.)", t2_items, (255, 237, 213))
    pdf.ln(2)

    # TABLA 3
    t3_items = [
        ('t3_patologiaCronica', "Patología crónica descompensada sintomática"),
        ('t3_discapacidadLeve', "Miembro con discapacidad leve/moderada (40-55pts)"),
        ('t3_rezago', "Rezago desarrollo psicomotor"),
        ('t3_madreAdolescente', "Madre adolescente"),
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
    print_risk_table("TABLA 3: FACTORES DE RIESGO MEDIO (4 PTS. C/U)", t3_items, (254, 249, 195))
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
    print_risk_table("TABLA 4: FACTORES DE RIESGO BAJO (3 PTS. C/U)", t4_items, (220, 252, 231))
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
    print_risk_table("TABLA 5: FACTORES PROTECTORES (NO OTORGAN PTS.)", t5_items, (219, 234, 254))
    
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
    
    pdf.cell(0, 5, f"Factores Riesgo Medio (T3): {c_t3} x 4 = {s_t3} pts.", ln=True)
    pdf.cell(0, 5, f"Factores Riesgo Bajo  (T4): {c_t4} x 3 = {s_t4} pts.", ln=True)
    pdf.ln(2)

    pdf.set_font('helvetica', 'B', 10)
    pdf.cell(40, 8, "PUNTAJE TOTAL:", border=1, align='R')
    pdf.cell(20, 8, str(data.get('total_points', 0)), border=1, align='C')
    pdf.cell(40, 8, "NIVEL DE RIESGO:", border=1, align='R')
    pdf.cell(50, 8, str(data.get('level', 'SIN RIESGO')), border=1, align='C')
    pdf.ln(8)

    # Evaluator Sig Area
    pdf.ln(15) # Increased space
    pdf.set_font('helvetica', '', 9)
    pdf.cell(100, 5, "", border=0)
    pdf.cell(80, 5, "____________________________________", border=0, align='C', ln=True)
    pdf.cell(100, 5, "", border=0)
    sig_eval = data.get('sig_evaluador_input', '') or data.get('evaluador_nombre', '')
    pdf.cell(80, 5, f"Evaluador: {sig_eval}", border=0, align='C', ln=True)
    pdf.ln(5)

    # --- 4. PLAN INTERVENCIÓN ---
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
    # Ensure we have space if the loop broke page? Auto-page break handles it usually, but let's be safe.
    if pdf.get_y() > 250: pdf.add_page()
    
    pdf.ln(15)
    
    y = pdf.get_y()
    pdf.line(60, y, 150, y) # Centered line
    
    pdf.set_xy(60, y+2)
    pdf.set_font('helvetica', '', 9)
    # Name from input
    pdf.multi_cell(90, 4, f"{data.get('sig_jefe','')}", align='C')
    
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
    text = (
        f"El equipo de cabecera del sector {data.get('comp_sector','')} representado por {data.get('comp_rep_sector','')} "
        f"y la familia {data.get('comp_familia','')} domiciliada en {data.get('comp_dir','')} "
        f"representada por {data.get('comp_rep_fam','')} (RUT {data.get('comp_rut','')}) "
        f"mediante el presente documento manifiestan el acuerdo de ejecutar el Plan de Trabajo elaborado en conjunto con el equipo de salud, con fecha: {data.get('comp_fecha','')}."
    )
    pdf.multi_cell(0, 5, text)
    
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
