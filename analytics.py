"""
analytics.py - Dashboard estadístico para encuesta_riesgo.
Principios Storytelling with Data (SWD) de Cole Nussbaumer Knaflic:
  - Eliminar el clutter (sin gridlines, sin marcos, sin leyendas redundantes)
  - Color con propósito: rojo=alto, amarillo=medio, verde=bajo; azul institucional para contexto
  - Anotaciones directas en las barras (sin leyenda externa si es posible)
  - Título + subtítulo de insight en cada gráfico
  - Reducir la carga cognitiva: menos es más
"""
import streamlit as st
import pandas as pd
import json
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime

# Paleta institucional
AZUL_OSCURO = "#1F3864"
AZUL_MED    = "#2E75B6"
CELESTE     = "#BDD7EE"
AMARILLO    = "#FFD966"
ROJO        = "#C00000"
VERDE_OK    = "#375623"
NARANJA     = "#ED7D31"
GRIS        = "#A6A6A6"

RISK_COLORS = {
    "RIESGO ALTO":  ROJO,
    "RIESGO MEDIO": AMARILLO,
    "RIESGO BAJO":  VERDE_OK,
}

FACTOR_LABELS = {
    't1_vif':                  'VIF (violencia intrafamiliar)',
    't1_drogas':               'Consumo drogas',
    't1_alcohol':              'Consumo alcohol (AUDIT>13)',
    't1_saludMentalDescomp':   'Salud mental descompensada',
    't1_abusoSexual':          'Abuso sexual',
    't1_riesgoBiopsicoGrave':  'Riesgo biopsicosocial grave',
    't1_epsaRiesgo':           'EPSA en riesgo',
    't1_vulnerabilidadExtrema':'Vulnerabilidad extrema',
    't1_trabajoInfantil':      'Trabajo infantil',
    't2_enfermedadGrave':      'Enfermedad grave',
    't2_altoRiesgoHosp':       'Alto riesgo hospitalario',
    't2_discapacidad':         'Discapacidad severa',
    't2_saludMentalLeve':      'Salud mental leve',
    't2_judicial':             'Problema judicial',
    't2_rolesParentales':      'Dificultad roles parentales',
    't2_adultosRiesgo':        'Adultos en riesgo',
    't3_patologiaCronica':     'Patología crónica',
    't3_discapacidadLeve':     'Discapacidad leve',
    't3_rezago':               'Rezago/déficit desarrollo',
    't3_madreAdolescente':     'Madre adolescente',
    't3_sinRedApoyo':          'Sin red de apoyo',
    't3_cesantia':             'Cesantía',
    't3_vulneNoExtrema':       'Vulnerabilidad no extrema',
    't3_precariedadLaboral':   'Precariedad laboral',
    't3_hacinamiento':         'Hacinamiento',
    't3_entornoInseguro':      'Entorno inseguro',
    't3_adultoSolo':           'Adulto solo',
    't3_desercionEscolar':     'Deserción escolar',
    't3_analfabetismo':        'Analfabetismo',
    't3_escolaridadIncompleta':'Escolaridad incompleta',
    't3_dificultadAcceso':     'Dificultad acceso servicios',
    't4_monoparental':         'Familia monoparental',
    't4_riesgoCardio':         'Riesgo cardiovascular',
    't4_contaminacion':        'Contaminación ambiental',
    't4_higiene':              'Problemas de higiene',
    't4_sinRecreacion':        'Sin espacios de recreación',
    't4_sinEspaciosSeguros':   'Sin espacios seguros',
    't4_endeudamiento':        'Endeudamiento familiar',
    't4_serviciosIncompletos': 'Servicios incompletos',
    't5_lactancia':            'Lactancia materna',
    't5_habitos':              'Hábitos saludables',
    't5_redesSociales':        'Redes sociales activas',
    't5_redFamiliar':          'Red familiar de apoyo',
    't5_comunicacion':         'Comunicación familiar',
    't5_recursosSuficientes':  'Recursos suficientes',
    't5_resiliencia':          'Resiliencia familiar',
    't5_viviendaAdecuada':     'Vivienda adecuada',
}

def _clean_layout(fig, title, subtitle=""):
    """Aplica estilo SWD a un gráfico Plotly: sin clutter, tipografía web Inter, transparente."""
    full_title = f"<span style='font-family: Inter, sans-serif; font-weight: 700;'>{title}</span>"
    if subtitle:
        full_title += f"<br><span style='font-family: Inter, sans-serif; font-size:11px;color:#64748b;font-weight:normal'>{subtitle}</span>"
    fig.update_layout(
        title=dict(text=full_title, font=dict(size=14, color="#0f172a"), x=0, xanchor='left'),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=10, r=10, t=60, b=10),
        font=dict(family="Inter, sans-serif", size=11, color="#334155"),
        showlegend=False,
        xaxis=dict(showgrid=False, zeroline=False, showline=False, tickfont=dict(size=10, color="#64748b")),
        yaxis=dict(showgrid=True, gridcolor="#f1f5f9", zeroline=False, showline=False, tickfont=dict(size=10, color="#64748b")),
    )
    return fig


def load_evaluaciones_df(est_filter=None):
    """Carga el DataFrame de evaluaciones con caché inteligente de datos crudos + filtrado dinámico RBAC + filtro establecimiento."""
    # 1. Intentar obtener datos crudos del caché (5 min)
    raw_df = None
    if 'raw_analytics_df' in st.session_state and 'raw_df_ts' in st.session_state:
        age_min = (datetime.now() - st.session_state['raw_df_ts']).seconds / 60
        if age_min < 5:
            raw_df = st.session_state['raw_analytics_df']

    # 2. Si no hay caché o expiró, cargar de Google Sheets
    if raw_df is None:
        try:
            import gspread
            from oauth2client.service_account import ServiceAccountCredentials
            secrets = st.secrets["gcp_service_account"]
            creds_dict = {k: secrets[k] for k in secrets}
            scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
            creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
            client = gspread.authorize(creds)
            SHEET_URL = st.secrets["SHEET_URL"]
            sh = client.open_by_url(SHEET_URL)
            data = sh.worksheet("Evaluaciones").get_all_values()
            if len(data) > 1:
                raw_df = pd.DataFrame(data[1:], columns=data[0])
                st.session_state['raw_analytics_df'] = raw_df
                st.session_state['raw_df_ts'] = datetime.now()
            else:
                return pd.DataFrame()
        except Exception as e:
            st.error(f"Error cargando datos: {e}")
            return pd.DataFrame()

    # 3. APLICAR FILTRO RBAC SIEMPRE (Dinámico por Sesión Actual)
    df = raw_df.copy()
    if 'authenticated' in st.session_state and st.session_state.authenticated:
        user_info = st.session_state.user_info
        role = str(user_info.get('rol', '')).lower()
        cargo = str(user_info.get('cargo', '')).lower()
        user_unit = str(user_info.get('Programa/Unidad', '')).lower()

        # Programador y Encargados MAIS ven todo
        if not (role in ['programador', 'encargado_mais'] or 'mais' in cargo):
            user_unit_clean = user_unit.strip().lower()
            user_cargo_clean = cargo.strip().lower()
            
            # Filtro por Sector (Prioridad: Encargado Postas ve Sector Luna)
            import re
            full_context = f"{user_unit_clean} {user_cargo_clean}"
            
            if 'encargado' in user_cargo_clean and 'postas' in user_cargo_clean:
                if 'Establecimiento' in df.columns:
                    df = df[df['Establecimiento'].str.strip().str.lower() != 'cesfam cholchol']
                else:
                    df = df[df['Sector'].str.strip().str.lower() == 'luna']
            elif re.search(r'\bsol\b', full_context):
                df = df[df['Sector'].str.strip().str.lower() == 'sol']
            elif re.search(r'\bluna\b', full_context) or 'postas' in full_context:
                df = df[df['Sector'].str.strip().str.lower() == 'luna']
            # Filtro por Programa
            elif user_unit_clean:
                 if 'Programa/Unidad' in df.columns:
                     df = df[df['Programa/Unidad'].str.strip().str.lower().str.contains(user_unit_clean)]
    
    
    # 4. APLICAR FILTRO DE ESTABLECIMIENTO (Global de la UI)
    if est_filter and est_filter != "Todos":
        if 'Establecimiento' in df.columns:
            df = df[df['Establecimiento'].str.strip().str.lower() == est_filter.lower()]
        elif 'Establecimiento Base' in df.columns:
            df = df[df['Establecimiento Base'].str.strip().str.lower() == est_filter.lower()]
            
    return df


def chart_risk_distribution(df):
    """
    DONUT: Distribución de familias por nivel de riesgo.
    SWD: Show the big number, minimal text, annot directas.
    """
    if df.empty or "Nivel" not in df.columns:
        return None
    counts = df["Nivel"].value_counts()
    labels = [k for k in ["RIESGO ALTO", "RIESGO MEDIO", "RIESGO BAJO"] if k in counts.index]
    values = [counts.get(k, 0) for k in labels]
    colors = [RISK_COLORS.get(k, GRIS) for k in labels]
    labels_short = [l.replace("RIESGO ", "") for l in labels]

    fig = go.Figure(go.Pie(
        labels=labels_short,
        values=values,
        hole=0.60,
        marker_colors=colors,
        textinfo="value+percent",
        textfont_size=12,
        hovertemplate="%{label}: %{value} familias (%{percent})<extra></extra>",
    ))
    # Texto central
    total = sum(values)
    fig.add_annotation(text=f"<b>{total}</b><br><span style='font-size:10px'>familias</span>",
                       x=0.5, y=0.5, showarrow=False, font_size=18, font_color=AZUL_OSCURO)
    fig.update_layout(
        title=dict(text="<b>Distribución de riesgo familiar</b><br><span style='font-size:11px;color:#666'>¿Cuántas familias están en cada nivel de riesgo?</span>",
                   font=dict(size=14, color=AZUL_OSCURO), x=0, xanchor='left'),
        plot_bgcolor="white", paper_bgcolor="white",
        margin=dict(l=80, r=30, t=70, b=60),
        font=dict(family="Roboto, Arial"),
        showlegend=True,
        legend=dict(orientation="h", y=-0.15, x=0.5, xanchor="center", font_size=11),
    )
    return fig


def chart_risk_by_sector(df):
    """
    BAR AGRUPADO H: Comparativa riesgo por sector Sol (Urbano) vs Luna (Rural).
    SWD: Destaca la diferencia, colores de riesgo, anotaciones directas.
    """
    if df.empty or "Sector" not in df.columns:
        return None
    niveles = ["RIESGO ALTO", "RIESGO MEDIO", "RIESGO BAJO"]
    sectores = ["Sol", "Luna"]
    sector_labels = {"Sol": "Sol (Urbano)", "Luna": "Luna (Rural)"}

    fig = go.Figure()
    for nivel in niveles:
        vals = [len(df[(df["Sector"].str.strip().str.lower()==s.lower()) & (df["Nivel"].str.strip().str.upper()==nivel)]) for s in sectores]
        fig.add_trace(go.Bar(
            name=nivel.replace("RIESGO ", ""),
            x=[sector_labels[s] for s in sectores],
            y=vals,
            marker_color=RISK_COLORS[nivel],
            text=vals,
            textposition="inside",
            textfont=dict(color="white", size=12, family="Roboto Bold"),
            hovertemplate=f"{nivel}: %{{y}} familias<extra></extra>",
        ))

    fig.update_layout(
        barmode="stack",
        title=dict(text="<b>Riesgo familiar por sector territorial</b><br><span style='font-size:10px;color:#94a3b8'>Sol=Urbano · Luna=Rural</span>",
                   font=dict(size=13, color=AZUL_OSCURO), x=0, xanchor='left'),
        plot_bgcolor="white", paper_bgcolor="white",
        margin=dict(l=80, r=30, t=85, b=60),
        font=dict(family="Roboto, Arial"),
        showlegend=True,
        legend=dict(orientation="h", y=-0.25, x=0.5, xanchor="center", font_size=10),
        xaxis=dict(showgrid=False, showline=False, automargin=True),
        yaxis=dict(showgrid=True, gridcolor="#F0F0F0", title="N° Familias", automargin=True),
    )
    return fig


def chart_risk_by_establishment(df):
    """
    BAR AGRUPADO H: Comparativa riesgo por Establecimiento (Postas/EMR).
    Útil para el Encargado de Postas.
    """
    if df.empty or "Establecimiento" not in df.columns:
        return None
    
    niveles = ["RIESGO ALTO", "RIESGO MEDIO", "RIESGO BAJO"]
    # Obtener establecimientos únicos con datos
    ests = sorted(df["Establecimiento"].unique())
    
    fig = go.Figure()
    for nivel in niveles:
        vals = [len(df[(df["Establecimiento"]==e) & (df["Nivel"]==nivel)]) for e in ests]
        fig.add_trace(go.Bar(
            name=nivel.replace("RIESGO ", ""),
            y=ests,
            x=vals,
            orientation="h",
            marker_color=RISK_COLORS[nivel],
            text=vals,
            textposition="inside",
            textfont=dict(color="white", size=11),
            hovertemplate=f"{nivel} en %{{y}}: %{{x}} familias<extra></extra>",
        ))

    fig.update_layout(
        barmode="stack",
        title=dict(text="<b>Riesgo familiar por Establecimiento</b><br><span style='font-size:11px;color:#666'>Distribución en Postas y EMR</span>",
                   font=dict(size=14, color=AZUL_OSCURO), x=0, xanchor='left'),
        plot_bgcolor="white", paper_bgcolor="white",
        margin=dict(l=120, r=30, t=70, b=80),
        font=dict(family="Inter, Roboto, Arial"),
        showlegend=True,
        legend=dict(orientation="h", y=-0.15, x=0.5, xanchor="center", font_size=10),
        xaxis=dict(showgrid=True, gridcolor="#F0F0F0", automargin=True),
        yaxis=dict(showgrid=False, showline=False, autorange="reversed", automargin=True),
    )
    return fig


def chart_top_risk_factors(df, top_n=12):
    """
    BAR HORIZONTAL ordenado: Top N factores de riesgo más frecuentes.
    SWD: "Show what matters" - resaltar los top 3, resto en gris. Etiquetas directas.
    """
    if df.empty:
        return None
    risk_keys = [c for c in df.columns if c.startswith(('t1_','t2_','t3_','t4_'))]
    counts = {}
    for k in risk_keys:
        n = (df[k].astype(str).str.strip().str.upper().isin(["TRUE","1","VERDADERO"])).sum()
        if n > 0:
            counts[k] = int(n)
    if not counts:
        return None
    sorted_items = sorted(counts.items(), key=lambda x: x[1], reverse=True)[:top_n]
    labels = [FACTOR_LABELS.get(k, k) for k, _ in sorted_items]
    values = [v for _, v in sorted_items]
    # Top 3 highlighted, rest gray
    colors = [AZUL_OSCURO if i < 3 else CELESTE for i in range(len(values))]

    fig = go.Figure(go.Bar(
        x=values,
        y=labels,
        orientation="h",
        marker_color=colors,
        text=values,
        textposition="outside",
        textfont=dict(size=11),
        hovertemplate="%{y}: %{x} familias<extra></extra>",
    ))
    fig.update_layout(
        title=dict(text=f"<b>Top {top_n} factores de riesgo más frecuentes</b><br><span style='font-size:11px;color:#666'>Los 3 primeros representan las mayores urgencias de intervención</span>",
                   font=dict(size=14, color=AZUL_OSCURO), x=0, xanchor='left'),
        plot_bgcolor="white", paper_bgcolor="white",
        margin=dict(l=130, r=80, t=70, b=40),
        font=dict(family="Roboto, Arial"),
        showlegend=False,
        xaxis=dict(showgrid=False, showline=False, zeroline=False, tickfont_size=10, automargin=True),
        yaxis=dict(showgrid=False, showline=False, autorange="reversed", tickfont_size=10, automargin=True),
        height=max(300, top_n * 32),
    )
    return fig


def chart_intervention_gap(df):
    """
    BAR APILADO: Familias con vs sin plan de intervención por nivel de riesgo.
    SWD: Muestra la "brecha de intervención" - insight accionable.
    """
    if df.empty:
        return None
    # Familias con plan (tienen datos en Planes de Intervención)
    niveles = ["RIESGO ALTO", "RIESGO MEDIO", "RIESGO BAJO"]
    # Usamos campo Plan Intervención JSON para detectar si tiene plan
    def has_plan(row):
        try:
            plan = json.loads(row.get("Plan Intervención JSON", "[]"))
            return len(plan) > 0
        except:
            return False

    df = df.copy()
    if "Plan Intervención JSON" in df.columns:
        df["tiene_plan"] = df.apply(has_plan, axis=1)
    else:
        df["tiene_plan"] = False

    con_plan   = [len(df[(df["Nivel"]==n) & (df["tiene_plan"]==True)])  for n in niveles]
    sin_plan   = [len(df[(df["Nivel"]==n) & (df["tiene_plan"]==False)]) for n in niveles]
    labels_s   = [n.replace("RIESGO ", "") for n in niveles]

    fig = go.Figure()
    fig.add_trace(go.Bar(
        name="Con plan", x=labels_s, y=con_plan,
        marker_color=AZUL_MED, text=con_plan, textposition="inside",
        textfont=dict(color="white", size=12),
        hovertemplate="Con plan: %{y}<extra></extra>",
    ))
    fig.add_trace(go.Bar(
        name="Sin plan (brecha)", x=labels_s, y=sin_plan,
        marker_color=CELESTE, text=sin_plan, textposition="inside",
        textfont=dict(color=AZUL_OSCURO, size=12),
        hovertemplate="Sin plan: %{y}<extra></extra>",
    ))
    fig.update_layout(
        barmode="stack",
        title=dict(text="<b>Brecha de intervención por nivel de riesgo</b><br><span style='font-size:10px;color:#94a3b8'>Familias con plan vs. sin plan asignado</span>",
                   font=dict(size=13, color=AZUL_OSCURO), x=0, xanchor='left'),
        plot_bgcolor="white", paper_bgcolor="white",
        margin=dict(l=80, r=30, t=85, b=60),
        font=dict(family="Roboto, Arial"),
        showlegend=True,
        legend=dict(orientation="h", y=-0.25, x=0.5, xanchor="center", font_size=10),
        xaxis=dict(showgrid=False, showline=False, automargin=True),
        yaxis=dict(showgrid=True, gridcolor="#F0F0F0", title="N° Familias", automargin=True),
    )
    return fig


def chart_evaluations_over_time(df):
    """
    LÍNEA: Evaluaciones por mes.
    SWD: Una sola línea limpia, eje X = tiempo, punto destacado en el último mes.
    """
    if df.empty or "Fecha" not in df.columns:
        return None
    df = df.copy()
    df["Fecha"] = pd.to_datetime(df["Fecha"], errors="coerce")
    df = df.dropna(subset=["Fecha"])
    if df.empty:
        return None
    df["Mes"] = df["Fecha"].dt.to_period("M").dt.to_timestamp()
    monthly = df.groupby("Mes").size().reset_index(name="N")

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=monthly["Mes"], y=monthly["N"],
        mode="lines+markers",
        line=dict(color=AZUL_OSCURO, width=2.5),
        marker=dict(color=AZUL_OSCURO, size=7),
        fill="tozeroy", fillcolor="rgba(31,56,100,0.08)",
        hovertemplate="%{x|%B %Y}: %{y} evaluaciones<extra></extra>",
    ))
    # Destacar el último punto
    if not monthly.empty:
        last = monthly.iloc[-1]
        fig.add_annotation(text=f"<b>{last['N']}</b>",
                           x=last['Mes'], y=last['N'],
                           showarrow=True, arrowhead=2, ay=-25,
                           font=dict(size=12, color=AZUL_OSCURO))

    fig.update_layout(
        title=dict(text="<b>Evolución de evaluaciones familiares</b><br><span style='font-size:11px;color:#666'>Número de evaluaciones realizadas por mes</span>",
                   font=dict(size=14, color=AZUL_OSCURO), x=0, xanchor='left'),
        plot_bgcolor="white", paper_bgcolor="white",
        margin=dict(l=80, r=30, t=70, b=60),
        font=dict(family="Roboto, Arial"),
        showlegend=False,
        xaxis=dict(showgrid=False, showline=False, tickformat="%b %Y", automargin=True),
        yaxis=dict(showgrid=True, gridcolor="#F0F0F0", title="Evaluaciones", rangemode="tozero", automargin=True),
    )
    return fig


def chart_score_distribution(df):
    """
    HISTOGRAMA: Distribución de puntajes de riesgo.
    SWD: Zonas de color para contextualizar los cortes bajo/medio/alto.
    """
    if df.empty or "Puntaje" not in df.columns:
        return None
    df = df.copy()
    df["Puntaje"] = pd.to_numeric(df["Puntaje"], errors="coerce").dropna()
    if df["Puntaje"].empty:
        return None

    fig = go.Figure()
    # Zonas de riesgo como fondo
    fig.add_vrect(x0=0, x1=16, fillcolor="rgba(55,86,35,0.08)", layer="below", line_width=0,
                  annotation_text="Bajo", annotation_position="top left",
                  annotation_font=dict(color=VERDE_OK, size=10))
    fig.add_vrect(x0=17, x1=25, fillcolor="rgba(255,217,102,0.15)", layer="below", line_width=0,
                  annotation_text="Medio", annotation_position="top left",
                  annotation_font=dict(color="#7F6000", size=10))
    fig.add_vrect(x0=26, x1=60, fillcolor="rgba(192,0,0,0.08)", layer="below", line_width=0,
                  annotation_text="Alto", annotation_position="top left",
                  annotation_font=dict(color=ROJO, size=10))

    fig.add_trace(go.Histogram(
        x=df["Puntaje"], nbinsx=20,
        marker_color=AZUL_MED, opacity=0.85,
        hovertemplate="Puntaje %{x}: %{y} familias<extra></extra>",
    ))
    fig.update_layout(
        title=dict(text="<b>Distribución de puntajes de riesgo</b><br><span style='font-size:11px;color:#666'>Bajo: 0-16 pts · Medio: 17-25 pts · Alto: ≥26 pts</span>",
                   font=dict(size=14, color=AZUL_OSCURO), x=0, xanchor='left'),
        plot_bgcolor="white", paper_bgcolor="white",
        margin=dict(l=80, r=30, t=70, b=60),
        font=dict(family="Roboto, Arial"),
        showlegend=False,
        xaxis=dict(title="Puntaje", showgrid=False, showline=False, range=[0, 60], automargin=True),
        yaxis=dict(title="N° Familias", showgrid=True, gridcolor="#F0F0F0", automargin=True),
        bargap=0.05,
    )
    return fig


def chart_by_program(df):
    """
    BAR H: Puntaje promedio por programa/unidad.
    SWD: Ordena descendente, barra del máximo highlighted.
    """
    if df.empty or "Programa/Unidad" not in df.columns:
        return None
    df = df.copy()
    df["Puntaje"] = pd.to_numeric(df["Puntaje"], errors="coerce")
    grp = df.groupby("Programa/Unidad").agg(
        Puntaje_prom=("Puntaje", "mean"),
        N=("Puntaje", "count")
    ).reset_index().sort_values("Puntaje_prom", ascending=True)
    grp = grp[grp["N"] >= 1]
    if grp.empty:
        return None

    max_idx = grp["Puntaje_prom"].idxmax()
    colors = [AZUL_OSCURO if i == max_idx else CELESTE for i in grp.index]

    fig = go.Figure(go.Bar(
        x=grp["Puntaje_prom"].round(1),
        y=grp["Programa/Unidad"],
        orientation="h",
        marker_color=colors,
        text=[f"{v:.1f} ({n})" for v, n in zip(grp["Puntaje_prom"], grp["N"])],
        textposition="outside",
        textfont=dict(size=10),
        hovertemplate="%{y}: prom %{x:.1f} pts<extra></extra>",
    ))
    fig.update_layout(
        title=dict(text="<b>Puntaje promedio de riesgo por programa CESFAM</b><br><span style='font-size:11px;color:#666'>Etiqueta: promedio (n familias)</span>",
                   font=dict(size=14, color=AZUL_OSCURO), x=0, xanchor='left'),
        plot_bgcolor="white", paper_bgcolor="white",
        margin=dict(l=130, r=80, t=70, b=40),
        font=dict(family="Roboto, Arial"),
        showlegend=False,
        xaxis=dict(showgrid=False, showline=False, zeroline=False, title="Puntaje promedio", automargin=True),
        yaxis=dict(showgrid=False, showline=False, tickfont_size=10, automargin=True),
        height=max(250, len(grp) * 35),
    )
    return fig




def chart_egress_analysis(df):
    """
    BAR AGRUPADO: Analisis de egresos de planes de intervencion por tipo y sector.
    Basado en las variables del reporte REM-P7 (egreso_alta, egreso_traslado,
    egreso_derivacion, egreso_abandono).
    """
    if df.empty:
        return None
    
    egreso_cols = ['egreso_alta', 'egreso_traslado', 'egreso_derivacion', 'egreso_abandono']
    egreso_labels = {
        'egreso_alta': 'Alta por cumplir plan',
        'egreso_traslado': 'Traslado',
        'egreso_derivacion': 'Derivacion',
        'egreso_abandono': 'Abandono'
    }
    available = [c for c in egreso_cols if c in df.columns]
    if not available:
        return None
    
    colors_egress = {
        'egreso_alta': VERDE_OK,
        'egreso_traslado': AZUL_MED,
        'egreso_derivacion': NARANJA,
        'egreso_abandono': ROJO
    }

    labels_map = {"Sol": "Sol (Urbano)", "Luna": "Luna (Rural)"}

    if "Sector" in df.columns:
        sectores_posibles = ["Sol", "Luna"]
        available_sectors = [s for s in sectores_posibles
                             if df["Sector"].str.strip().str.lower().eq(s.lower()).any()]
        if not available_sectors:
            all_sectors = df["Sector"].dropna().unique()
            available_sectors = [str(s).strip() for s in all_sectors if str(s).strip()]
    else:
        available_sectors = []

    sector_data = {}
    if available_sectors:
        for col in available:
            sector_data[col] = {}
            for s in available_sectors:
                mask = (df["Sector"].str.strip().str.lower() == s.lower()) & \
                       (df[col].astype(str).str.strip().str.upper().isin(["TRUE", "1", "VERDADERO"]))
                sector_data[col][s] = int(mask.sum())

    fig = go.Figure()
    for col in available:
        if available_sectors:
            vals = [sector_data[col].get(s, 0) for s in available_sectors]
            x_labels = [labels_map.get(s, s) for s in available_sectors]
        else:
            total_val = int((df[col].astype(str).str.strip().str.upper().isin(["TRUE", "1", "VERDADERO"])).sum())
            vals = [total_val]
            x_labels = ["Total"]

        fig.add_trace(go.Bar(
            name=egreso_labels.get(col, col),
            x=x_labels,
            y=vals,
            marker_color=colors_egress.get(col, GRIS),
            text=vals,
            textposition="outside",
            textfont=dict(size=10),
            hovertemplate=f"{egreso_labels.get(col, col)}: %{{y}} familias<extra></extra>",
        ))

    fig.update_layout(
        barmode="group",
        title=dict(
            text="<b>Egresos de planes de intervencion por tipo y sector</b><br>"
                 "<span style='font-size:10px;color:#94a3b8;font-weight:normal'>"
                 "REM-P7: Causas de egreso (Alta, Traslado, Derivacion, Abandono)</span>",
            font=dict(size=13, color=AZUL_OSCURO), x=0, xanchor='left'
        ),
        plot_bgcolor="white", paper_bgcolor="white",
        margin=dict(l=80, r=30, t=85, b=60),
        font=dict(family="Roboto, Arial"),
        showlegend=True,
        legend=dict(orientation="h", y=-0.25, x=0.5, xanchor="center", font_size=9),
        xaxis=dict(showgrid=False, showline=False, tickfont_size=11, automargin=True),
        yaxis=dict(showgrid=True, gridcolor="#F0F0F0", title="N° Familias", rangemode="tozero", automargin=True),
        bargap=0.2,
        bargroupgap=0.15,
    )
    return fig


def chart_intervention_coverage_by_sector(df):
    """
    BAR APILADO: Cobertura de intervencion por sector (con plan vs sin plan).
    Basado en la Seccion B del reporte REM-P7.
    Muestra el porcentaje de cobertura sobre cada barra.
    """
    if df.empty or "Sector" not in df.columns:
        return None
    
    def has_plan(row):
        try:
            plan = json.loads(row.get("Plan Intervención JSON", "[]"))
            return len(plan) > 0
        except:
            return False
    
    df = df.copy()
    if "Plan Intervención JSON" in df.columns:
        df["tiene_plan"] = df.apply(has_plan, axis=1)
    else:
        df["tiene_plan"] = False
    
    sectores = ["Sol", "Luna"]
    labels_map = {"Sol": "Sol (Urbano)", "Luna": "Luna (Rural)"}
    available_sectors = [s for s in sectores if df["Sector"].str.strip().str.lower().eq(s.lower()).any()]
    if not available_sectors:
        all_sect = df["Sector"].dropna().unique()
        available_sectors = [str(s).strip() for s in all_sect if str(s).strip()]
    if not available_sectors:
        return None
    
    con_plan = [len(df[(df["Sector"].str.strip().str.lower()==s.lower()) & (df["tiene_plan"]==True)]) for s in available_sectors]
    sin_plan = [len(df[(df["Sector"].str.strip().str.lower()==s.lower()) & (df["tiene_plan"]==False)]) for s in available_sectors]
    totales = [con_plan[i] + sin_plan[i] for i in range(len(available_sectors))]
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        name="Con plan de intervencion",
        x=[labels_map.get(s, s) for s in available_sectors],
        y=con_plan,
        marker_color=AZUL_MED,
        text=con_plan,
        textposition="inside",
        textfont=dict(color="white", size=13, family="Roboto Bold"),
        hovertemplate="Con plan: %{y} familias<extra></extra>",
    ))
    fig.add_trace(go.Bar(
        name="Sin plan (brecha)",
        x=[labels_map.get(s, s) for s in available_sectors],
        y=sin_plan,
        marker_color=CELESTE,
        text=sin_plan,
        textposition="inside",
        textfont=dict(color=AZUL_OSCURO, size=13),
        hovertemplate="Sin plan: %{y} familias<extra></extra>",
    ))
    
    max_y = max(totales) if totales else 1
    for i, s in enumerate(available_sectors):
        total = totales[i]
        if total > 0:
            pct = con_plan[i] / total * 100
            fig.add_annotation(
                x=labels_map.get(s, s),
                y=total + max_y * 0.08,
                text=f"<b>{pct:.0f}%</b> cobertura",
                showarrow=False,
                font=dict(size=11, color=AZUL_OSCURO),
            )
    
    fig.update_layout(
        barmode="stack",
        title=dict(
            text="<b>Cobertura de intervencion por sector territorial</b><br>"
                 "<span style='font-size:10px;color:#94a3b8;font-weight:normal'>"
                 "REM-P7: Familias con y sin plan de intervencion por sector</span>",
            font=dict(size=13, color=AZUL_OSCURO), x=0, xanchor='left'
        ),
        plot_bgcolor="white", paper_bgcolor="white",
        margin=dict(l=80, r=30, t=85, b=60),
        font=dict(family="Roboto, Arial"),
        showlegend=True,
        legend=dict(orientation="h", y=-0.25, x=0.5, xanchor="center", font_size=10),
        xaxis=dict(showgrid=False, showline=False, tickfont_size=11, automargin=True),
        yaxis=dict(showgrid=True, gridcolor="#F0F0F0", title="N° Familias", rangemode="tozero", automargin=True),
    )
    return fig


# ─────────────────────────────────────────────────────────────────────────────
# GRÁFICOS REM-P7 ADICIONALES
# ─────────────────────────────────────────────────────────────────────────────

def chart_rem_ingresos_egresos_mensual(df):
    """
    LÍNEA DOBLE: Evolución mensual de ingresos vs. egresos.
    REM-P7: Flujo mensual de familias en el programa MAIS.
    """
    if df.empty or "Fecha" not in df.columns:
        return None
    df = df.copy()
    df["Fecha"] = pd.to_datetime(df["Fecha"], errors="coerce")
    df = df.dropna(subset=["Fecha"])
    if df.empty:
        return None
    df["Mes"] = df["Fecha"].dt.to_period("M").dt.to_timestamp()

    ingresos = df.groupby("Mes").size().reset_index(name="Ingresos")

    egreso_cols = ['egreso_alta', 'egreso_traslado', 'egreso_derivacion', 'egreso_abandono']
    available_egr = [c for c in egreso_cols if c in df.columns]
    if available_egr:
        df["es_egreso"] = df[available_egr].apply(
            lambda row: any(str(v).strip().upper() in ["TRUE", "1", "VERDADERO"] for v in row), axis=1
        )
        egresos = df[df["es_egreso"]].groupby("Mes").size().reset_index(name="Egresos")
    else:
        egresos = pd.DataFrame(columns=["Mes", "Egresos"])

    monthly = ingresos.merge(egresos, on="Mes", how="left").fillna(0)

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=monthly["Mes"], y=monthly["Ingresos"],
        name="Ingresos", mode="lines+markers",
        line=dict(color=AZUL_MED, width=2.5),
        marker=dict(size=7),
        fill="tozeroy", fillcolor="rgba(46,117,182,0.07)",
        hovertemplate="%{x|%b %Y}: %{y} ingresos<extra></extra>",
    ))
    fig.add_trace(go.Scatter(
        x=monthly["Mes"], y=monthly["Egresos"],
        name="Egresos", mode="lines+markers",
        line=dict(color=ROJO, width=2.5, dash="dot"),
        marker=dict(size=7),
        hovertemplate="%{x|%b %Y}: %{y} egresos<extra></extra>",
    ))
    fig.update_layout(
        title=dict(
            text="<b>Evolución mensual: Ingresos vs. Egresos</b><br>"
                 "<span style='font-size:10px;color:#94a3b8;font-weight:normal'>"
                 "REM-P7: Flujo mensual de familias en programa MAIS</span>",
            font=dict(size=13, color=AZUL_OSCURO), x=0, xanchor='left'
        ),
        plot_bgcolor="white", paper_bgcolor="white",
        margin=dict(l=80, r=30, t=85, b=60),
        font=dict(family="Roboto, Arial"),
        showlegend=True,
        legend=dict(orientation="h", y=-0.25, x=0.5, xanchor="center", font_size=10),
        xaxis=dict(showgrid=False, showline=False, tickformat="%b %Y", tickangle=-45, automargin=True),
        yaxis=dict(showgrid=True, gridcolor="#F0F0F0", title="N° Familias", rangemode="tozero", automargin=True),
    )
    return fig


def chart_rem_apgar_distribution(df):
    """
    BAR HORIZONTAL: Distribución de niveles de funcionalidad APGAR Familiar.
    REM-P7: Funcional / Disfunción Leve / Disfunción Severa.
    """
    if df.empty or "APGAR Total" not in df.columns:
        return None
    df = df.copy()
    df["apgar_num"] = pd.to_numeric(df["APGAR Total"], errors="coerce")
    df = df.dropna(subset=["apgar_num"])
    if df.empty:
        return None

    funcional = int((df["apgar_num"] >= 7).sum())
    leve      = int(((df["apgar_num"] >= 4) & (df["apgar_num"] <= 6)).sum())
    severo    = int((df["apgar_num"] <= 3).sum())

    labels = ["Funcional (7-10)", "Disfunción Leve (4-6)", "Disfunción Severa (0-3)"]
    values = [funcional, leve, severo]
    colors = [VERDE_OK, AMARILLO, ROJO]

    fig = go.Figure(go.Bar(
        x=values, y=labels,
        orientation="h",
        marker_color=colors,
        text=values,
        textposition="outside",
        textfont=dict(size=13, family="Roboto Bold"),
        hovertemplate="%{y}: %{x} familias<extra></extra>",
    ))
    fig.update_layout(
        title=dict(
            text="<b>Funcionalidad familiar (APGAR)</b><br>"
                 "<span style='font-size:10px;color:#94a3b8;font-weight:normal'>"
                 "REM-P7: Distribución de familias por nivel APGAR</span>",
            font=dict(size=13, color=AZUL_OSCURO), x=0, xanchor='left'
        ),
        plot_bgcolor="white", paper_bgcolor="white",
        margin=dict(l=110, r=80, t=85, b=40),
        font=dict(family="Roboto, Arial"),
        showlegend=False,
        xaxis=dict(showgrid=False, showline=False, zeroline=False, title="N° Familias", automargin=True),
        yaxis=dict(showgrid=False, showline=False, autorange="reversed", tickfont_size=12, automargin=True),
    )
    return fig


def chart_rem_coverage_by_program(df):
    """
    BAR HORIZONTAL: % de cobertura de intervención por programa/unidad.
    REM-P7: Familias con plan activo vs total por unidad CESFAM. Línea meta 70%.
    """
    if df.empty or "Programa/Unidad" not in df.columns:
        return None

    def has_plan(row):
        try:
            plan = json.loads(row.get("Plan Intervención JSON", "[]"))
            return len(plan) > 0
        except:
            return False

    df = df.copy()
    if "Plan Intervención JSON" in df.columns:
        df["tiene_plan"] = df.apply(has_plan, axis=1)
    else:
        df["tiene_plan"] = False

    grp = df.groupby("Programa/Unidad").agg(
        total=("tiene_plan", "count"),
        con_plan=("tiene_plan", "sum")
    ).reset_index()
    grp = grp[grp["total"] >= 1]
    if grp.empty:
        return None

    grp["cobertura_pct"] = (grp["con_plan"] / grp["total"] * 100).round(1)
    grp = grp.sort_values("cobertura_pct", ascending=True)

    colors = [AZUL_MED if p >= 70 else AMARILLO if p >= 40 else ROJO for p in grp["cobertura_pct"]]

    fig = go.Figure(go.Bar(
        x=grp["cobertura_pct"],
        y=grp["Programa/Unidad"],
        orientation="h",
        marker_color=colors,
        text=[f"{p:.0f}% ({int(c)}/{int(t)})" for p, c, t in zip(grp["cobertura_pct"], grp["con_plan"], grp["total"])],
        textposition="outside",
        textfont=dict(size=10),
        hovertemplate="%{y}: %{x:.1f}% cobertura<extra></extra>",
    ))
    fig.add_vline(
        x=70, line_dash="dash", line_color=AZUL_MED, opacity=0.6,
        annotation_text="Meta 70%", annotation_font_size=9,
        annotation_position="top right"
    )
    fig.update_layout(
        title=dict(
            text="<b>Cobertura de intervención por programa</b><br>"
                 "<span style='font-size:10px;color:#94a3b8;font-weight:normal'>"
                 "REM-P7: % familias con plan activo por unidad CESFAM</span>",
            font=dict(size=13, color=AZUL_OSCURO), x=0, xanchor='left'
        ),
        plot_bgcolor="white", paper_bgcolor="white",
        margin=dict(l=150, r=100, t=85, b=40),
        font=dict(family="Roboto, Arial"),
        showlegend=False,
        xaxis=dict(showgrid=False, showline=False, zeroline=False, title="% Cobertura", range=[0, 120]),
        yaxis=dict(showgrid=False, showline=False, tickfont_size=9, automargin=True),
        height=max(300, len(grp) * 40),
    )
    return fig


def chart_rem_egress_pie(df):
    """
    DONUT: Proporción de tipos de egreso (Alta / Traslado / Derivación / Abandono).
    REM-P7: Causas de cierre del plan de intervención.
    """
    egreso_cols = ['egreso_alta', 'egreso_traslado', 'egreso_derivacion', 'egreso_abandono']
    labels_map = {
        'egreso_alta':      'Alta por cumplir plan',
        'egreso_traslado':  'Traslado',
        'egreso_derivacion':'Derivación',
        'egreso_abandono':  'Abandono',
    }
    colors_map = {
        'egreso_alta':      VERDE_OK,
        'egreso_traslado':  AZUL_MED,
        'egreso_derivacion':NARANJA,
        'egreso_abandono':  ROJO,
    }

    available = [c for c in egreso_cols if c in df.columns]
    if not available:
        return None

    values, labels, colors = [], [], []
    for col in available:
        n = int((df[col].astype(str).str.strip().str.upper().isin(["TRUE", "1", "VERDADERO"])).sum())
        if n > 0:
            values.append(n)
            labels.append(labels_map.get(col, col))
            colors.append(colors_map.get(col, GRIS))

    if not values:
        return None

    total_egr = sum(values)
    fig = go.Figure(go.Pie(
        labels=labels,
        values=values,
        hole=0.55,
        marker_colors=colors,
        textinfo="value+percent",
        textposition="outside",
        textfont_size=11,
        insidetextorientation="auto",
        pull=[0.03] * len(values),
        hovertemplate="%{label}: %{value} (%{percent})<extra></extra>",
    ))
    fig.add_annotation(
        text=f"<b>{total_egr}</b><br><span style='font-size:10px'>egresos</span>",
        x=0.5, y=0.5, showarrow=False, font_size=18, font_color=AZUL_OSCURO
    )
    fig.update_layout(
        title=dict(
            text="<b>Distribución de tipos de egreso</b><br>"
                 "<span style='font-size:10px;color:#94a3b8;font-weight:normal'>"
                 "REM-P7: Causas de cierre del plan de intervención</span>",
            font=dict(size=13, color=AZUL_OSCURO), x=0, xanchor='left'
        ),
        plot_bgcolor="white", paper_bgcolor="white",
        margin=dict(l=80, r=30, t=85, b=60),
        font=dict(family="Roboto, Arial"),
        showlegend=True,
        legend=dict(orientation="h", y=-0.2, x=0.5, xanchor="center", font_size=9),
    )
    return fig


# ─────────────────────────────────────────────────────────────────────────────
# HELPERS INTERNOS PARA EL PDF DEL DASHBOARD
# ─────────────────────────────────────────────────────────────────────────────

def _pdf_section_title(pdf, title):
    """Imprime un título de sección con fondo azul institucional."""
    pdf.set_font('helvetica', 'B', 10)
    pdf.set_fill_color(31, 56, 100)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(0, 7, f"  {title}", border=0, ln=True, fill=True)
    pdf.set_text_color(0, 0, 0)
    pdf.ln(3)


def _pdf_kpi_row(pdf, kpis):
    """
    Imprime una fila de tarjetas KPI en el PDF.
    kpis: lista de tuplas (label, value, color_rgb)
    """
    n = len(kpis)
    w = 190 // n
    y0_row = pdf.get_y()
    for idx, (label, value, color) in enumerate(kpis):
        x0 = 10 + idx * w
        pdf.set_xy(x0, y0_row)
        pdf.set_fill_color(248, 250, 252)
        pdf.cell(w - 2, 18, "", border=1, fill=True)
        # Label
        pdf.set_xy(x0 + 2, y0_row + 2)
        pdf.set_font('helvetica', '', 7)
        pdf.set_text_color(100, 116, 139)
        pdf.cell(w - 6, 4, label.upper())
        # Value
        pdf.set_xy(x0 + 2, y0_row + 7)
        pdf.set_font('helvetica', 'B', 14)
        pdf.set_text_color(*color)
        pdf.cell(w - 6, 9, str(value))
        pdf.set_text_color(0, 0, 0)
    pdf.set_xy(10, y0_row + 20)


# ─────────────────────────────────────────────────────────────────────────────
# GENERADOR DE PDF DEL DASHBOARD (Solo Programador)
# ─────────────────────────────────────────────────────────────────────────────

def generate_dashboard_pdf(df):
    """
    Genera un reporte PDF ejecutivo del dashboard analítico.
    Acceso restringido al rol 'programador'.

    Estrategia de imágenes:
      - Si kaleido está instalado → gráficos Plotly como PNG en el PDF.
      - Si no está disponible    → tablas de datos equivalentes (fallback robusto).

    Returns:
        bytes: contenido del PDF listo para st.download_button.
    """
    from fpdf import FPDF
    import os as _os
    import tempfile

    # ── Detectar kaleido ──────────────────────────────────────────────────────
    _kaleido_ok = False
    try:
        import plotly.io as _pio
        _ = _pio.kaleido.scope
        _kaleido_ok = True
    except Exception:
        pass

    def _fig_to_png(fig):
        """Exporta figura Plotly a PNG temporal. Retorna ruta o None."""
        if not _kaleido_ok or fig is None:
            return None
        try:
            import plotly.io as _pio2
            tmp = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
            _pio2.write_image(fig, tmp.name, width=720, height=360, scale=1.5)
            tmp.close()
            return tmp.name
        except Exception:
            return None

    # ── Cálculo de métricas base ──────────────────────────────────────────────
    total = len(df)
    alto  = int((df["Nivel"] == "RIESGO ALTO").sum())  if "Nivel" in df.columns else 0
    medio = int((df["Nivel"] == "RIESGO MEDIO").sum()) if "Nivel" in df.columns else 0
    bajo  = int((df["Nivel"] == "RIESGO BAJO").sum())  if "Nivel" in df.columns else 0

    def _has_plan(row):
        try:
            plan = json.loads(row.get("Plan Intervención JSON", "[]"))
            return len(plan) > 0
        except:
            return False

    df2 = df.copy()
    if "Plan Intervención JSON" in df.columns:
        df2["tiene_plan"] = df2.apply(_has_plan, axis=1)
    else:
        df2["tiene_plan"] = False

    con_plan    = int(df2["tiene_plan"].sum())
    sin_plan    = total - con_plan
    cobertura_p = f"{con_plan / total * 100:.0f}%" if total > 0 else "0%"

    egreso_cols_r = ['egreso_alta', 'egreso_traslado', 'egreso_derivacion', 'egreso_abandono']
    egreso_labels = {
        'egreso_alta': 'Alta por cumplir plan',
        'egreso_traslado': 'Traslado',
        'egreso_derivacion': 'Derivación',
        'egreso_abandono': 'Abandono',
    }
    egresos_total = 0
    egreso_breakdown = {}
    for col in egreso_cols_r:
        if col in df.columns:
            n = int((df[col].astype(str).str.strip().str.upper().isin(["TRUE", "1", "VERDADERO"])).sum())
            egresos_total += n
            egreso_breakdown[egreso_labels.get(col, col)] = n

    fecha_desde, fecha_hasta = "-", "-"
    if "Fecha" in df.columns:
        fechas = pd.to_datetime(df["Fecha"], errors="coerce").dropna()
        if not fechas.empty:
            fecha_desde = fechas.min().strftime("%d/%m/%Y")
            fecha_hasta = fechas.max().strftime("%d/%m/%Y")

    from datetime import datetime as _dt
    generado = _dt.now().strftime("%d/%m/%Y")

    # ── Clase PDF con footer ──────────────────────────────────────────────────
    class DashPDF(FPDF):
        def footer(self):
            self.set_y(-15)
            self.set_font('helvetica', 'I', 7)
            self.set_text_color(150, 150, 150)
            self.cell(0, 10,
                f"Dashboard Analítico ERBI - CESFAM Cholchol  |  "
                f"Página {self.page_no()}/{{nb}}  |  "
                f"Generado: {generado}  |  "
                f"Jefatura Técnica - CESFAM Cholchol",
                align='C')
            self.set_text_color(0, 0, 0)

    pdf = DashPDF(orientation='P', unit='mm', format='A4')
    pdf.alias_nb_pages()
    pdf.set_auto_page_break(auto=True, margin=18)

    base_dir = _os.path.dirname(_os.path.abspath(__file__))
    logo_path = _os.path.join(base_dir, "NUEVO LOGO.png")

    # ═════════════════════════════════════════════════════════════════════════
    # PORTADA
    # ═════════════════════════════════════════════════════════════════════════
    pdf.add_page()

    if _os.path.exists(logo_path):
        pdf.image(logo_path, 10, 10, 22)

    pdf.set_xy(38, 12)
    pdf.set_font('helvetica', 'B', 12)
    pdf.cell(0, 6, "ILUSTRE MUNICIPALIDAD DE CHOLCHOL", ln=True, align='C')
    pdf.set_xy(38, 19)
    pdf.set_font('helvetica', '', 9)
    pdf.cell(0, 5, "Departamento de Salud  |  CESFAM Cholchol  |  Sistema ERBI Analytics", ln=True, align='C')
    pdf.ln(6)

    # Título
    pdf.set_fill_color(31, 56, 100)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font('helvetica', 'B', 15)
    pdf.cell(0, 13, "  DASHBOARD ANALÍTICO - RIESGO FAMILIAR", ln=True, fill=True)
    pdf.set_text_color(0, 0, 0)
    pdf.ln(3)

    # Metadatos
    pdf.set_font('helvetica', '', 9)
    pdf.set_fill_color(240, 245, 255)
    pdf.cell(95, 7, f"  Generado: {generado}", border=0, fill=True)
    pdf.cell(95, 7, f"  Período: {fecha_desde} - {fecha_hasta}", border=0, fill=True, ln=True)
    pdf.cell(95, 7, f"  Total evaluaciones: {total}", border=0, fill=True)
    pdf.cell(95, 7, "", border=0, fill=True, ln=True)
    pdf.ln(6)

    # ═════════════════════════════════════════════════════════════════════════
    # SECCIÓN 1 – INDICADORES GENERALES
    # ═════════════════════════════════════════════════════════════════════════
    _pdf_section_title(pdf, "1. INDICADORES GENERALES DE RIESGO FAMILIAR")
    _pdf_kpi_row(pdf, [
        ("Total Evaluaciones",  str(total),                         (31, 56, 100)),
        ("Riesgo Alto",          f"{alto} ({alto*100//total if total else 0}%)",   (192, 0, 0)),
        ("Riesgo Medio",         f"{medio} ({medio*100//total if total else 0}%)", (163, 100, 0)),
        ("Riesgo Bajo",          f"{bajo} ({bajo*100//total if total else 0}%)",   (55, 86, 35)),
    ])

    # Top 10 factores de riesgo
    _pdf_section_title(pdf, "Top 10 Factores de Riesgo más Frecuentes")
    risk_keys_loc = [c for c in df.columns if c.startswith(('t1_', 't2_', 't3_', 't4_'))]
    factor_counts = {}
    for k in risk_keys_loc:
        n = int((df[k].astype(str).str.strip().str.upper().isin(["TRUE", "1", "VERDADERO"])).sum())
        if n > 0:
            factor_counts[k] = n
    top_factors = sorted(factor_counts.items(), key=lambda x: x[1], reverse=True)[:10]

    if top_factors:
        pdf.set_font('helvetica', 'B', 7)
        pdf.set_fill_color(189, 215, 238)
        pdf.cell(125, 6, "Factor de Riesgo", border=1, fill=True, align='C')
        pdf.cell(35, 6, "N° Familias", border=1, fill=True, align='C')
        pdf.cell(30, 6, "% Total", border=1, fill=True, align='C', ln=True)
        pdf.set_font('helvetica', '', 7)
        for i, (k, n) in enumerate(top_factors):
            fill = i % 2 == 0
            pdf.set_fill_color(248, 250, 252) if fill else pdf.set_fill_color(255, 255, 255)
            label = FACTOR_LABELS.get(k, k)
            pct = f"{n / total * 100:.1f}%" if total else "-"
            pdf.cell(125, 5, f"  {label[:80]}", border=1, fill=fill)
            pdf.cell(35, 5, str(n), border=1, fill=fill, align='C')
            pdf.cell(30, 5, pct, border=1, fill=fill, align='C', ln=True)
    pdf.ln(2)

    # ── Gráficos de riesgo (solo con kaleido) ────────────────────────────────
    _pdf_section_title(pdf, "Distribución del Riesgo Familiar")
    for _fn in [chart_risk_distribution, chart_risk_by_sector, chart_risk_by_establishment]:
        _img_p = _fig_to_png(_fn(df))
        if _img_p:
            pdf.add_page()
            pdf.image(_img_p, x=15, w=180)
            pdf.ln(5)
            _os.unlink(_img_p)

    # ── Gráficos adicionales del dashboard (solo con kaleido) ─────────────────
    for _fn in [chart_intervention_gap, chart_score_distribution,
                chart_evaluations_over_time, chart_by_program]:
        _img_p = _fig_to_png(_fn(df))
        if _img_p:
            pdf.add_page()
            pdf.image(_img_p, x=15, w=180)
            pdf.ln(5)
            _os.unlink(_img_p)

    # ── Evaluaciones por Establecimiento ──────────────────────────────────────
    _pdf_section_title(pdf, "Evaluaciones por Establecimiento")
    if "Establecimiento" in df.columns:
        _est_counts = df["Establecimiento"].value_counts().sort_values(ascending=False)
        pdf.set_font('helvetica', 'B', 8)
        pdf.set_fill_color(189, 215, 238)
        pdf.cell(90, 6, "Establecimiento", border=1, fill=True, align='C')
        pdf.cell(30, 6, "Evaluaciones", border=1, fill=True, align='C')
        pdf.cell(30, 6, "% del Total", border=1, fill=True, align='C')
        pdf.cell(40, 6, "Estratificación", border=1, fill=True, align='C', ln=True)
        pdf.set_font('helvetica', '', 7.5)
        for _i, (_est, _cnt) in enumerate(_est_counts.items()):
            _fill = _i % 2 == 0
            pdf.set_fill_color(248, 250, 252) if _fill else pdf.set_fill_color(255, 255, 255)
            _pct_est = f"{_cnt / total * 100:.1f}%" if total else "-"
            # Estratificación: contar niveles dentro del establecimiento
            _est_df = df[df["Establecimiento"] == _est]
            _a = int((_est_df["Nivel"] == "RIESGO ALTO").sum()) if "Nivel" in _est_df.columns else 0
            _m = int((_est_df["Nivel"] == "RIESGO MEDIO").sum()) if "Nivel" in _est_df.columns else 0
            _b = int((_est_df["Nivel"] == "RIESGO BAJO").sum()) if "Nivel" in _est_df.columns else 0
            _estrat = f"Alto:{_a}  Medio:{_m}  Bajo:{_b}"
            pdf.cell(90, 5, f"  {_est[:50]}", border=1, fill=_fill)
            pdf.cell(30, 5, str(_cnt), border=1, fill=_fill, align='C')
            pdf.cell(30, 5, _pct_est, border=1, fill=_fill, align='C')
            pdf.cell(40, 5, _estrat, border=1, fill=_fill, align='C', ln=True)
    else:
        pdf.set_font('helvetica', 'I', 9)
        pdf.cell(0, 6, "No hay datos de establecimiento disponibles.", ln=True)
    pdf.ln(4)

    # ═════════════════════════════════════════════════════════════════════════
    # SECCIÓN 2 – MÉTRICAS REM-P7
    # ═════════════════════════════════════════════════════════════════════════
    pdf.add_page()
    _pdf_section_title(pdf, "2. MÉTRICAS REM-P7 - REPORTE OFICIAL MINSAL")
    _pdf_kpi_row(pdf, [
        ("Con Plan de Intervención", str(con_plan),    (46, 117, 182)),
        ("Sin Plan (Brecha)",        str(sin_plan),    (100, 140, 180)),
        ("Cobertura %",              cobertura_p,      (31, 56, 100)),
        ("Total Egresos",            str(egresos_total),(192, 0, 0)),
    ])

    # Tabla egresos por tipo
    _pdf_section_title(pdf, "Desglose de Egresos por Tipo")
    if egreso_breakdown:
        pdf.set_font('helvetica', 'B', 8)
        pdf.set_fill_color(189, 215, 238)
        pdf.cell(95, 6, "Tipo de Egreso", border=1, fill=True, align='C')
        pdf.cell(47, 6, "N° Familias", border=1, fill=True, align='C')
        pdf.cell(48, 6, "% del Total Egresos", border=1, fill=True, align='C', ln=True)
        pdf.set_font('helvetica', '', 9)
        for i, (label, n) in enumerate(egreso_breakdown.items()):
            fill = i % 2 == 0
            pdf.set_fill_color(248, 250, 252) if fill else pdf.set_fill_color(255, 255, 255)
            pct = f"{n / egresos_total * 100:.1f}%" if egresos_total else "-"
            pdf.cell(95, 7, f"  {label}", border=1, fill=fill)
            pdf.cell(47, 7, str(n), border=1, fill=fill, align='C')
            pdf.cell(48, 7, pct, border=1, fill=fill, align='C', ln=True)
    else:
        pdf.set_font('helvetica', 'I', 9)
        pdf.cell(0, 6, "Sin egresos registrados en el período.", ln=True)
    pdf.ln(4)

    # Tabla cobertura por sector
    _pdf_section_title(pdf, "Cobertura de Intervención por Sector Territorial")
    if "Sector" in df.columns:
        pdf.set_font('helvetica', 'B', 8)
        pdf.set_fill_color(189, 215, 238)
        pdf.cell(70, 6, "Sector", border=1, fill=True, align='C')
        pdf.cell(40, 6, "Con Plan", border=1, fill=True, align='C')
        pdf.cell(40, 6, "Sin Plan", border=1, fill=True, align='C')
        pdf.cell(40, 6, "% Cobertura", border=1, fill=True, align='C', ln=True)
        pdf.set_font('helvetica', '', 9)
        for i, sector in enumerate(["Sol", "Luna"]):
            df_s = df2[df2["Sector"].str.strip().str.lower() == sector.lower()]
            cp_s = int(df_s["tiene_plan"].sum()) if "tiene_plan" in df2.columns else 0
            sp_s = len(df_s) - cp_s
            tt_s = len(df_s)
            pct_s = f"{cp_s / tt_s * 100:.0f}%" if tt_s > 0 else "-"
            fill = i % 2 == 0
            pdf.set_fill_color(248, 250, 252) if fill else pdf.set_fill_color(255, 255, 255)
            pdf.cell(70, 7, f"  {sector} ({'Urbano' if sector == 'Sol' else 'Rural'})", border=1, fill=fill)
            pdf.cell(40, 7, str(cp_s), border=1, fill=fill, align='C')
            pdf.cell(40, 7, str(sp_s), border=1, fill=fill, align='C')
            pdf.cell(40, 7, pct_s, border=1, fill=fill, align='C', ln=True)
    pdf.ln(2)

    # ── Gráficos REM-P7 (solo con kaleido) ────────────────────────────────────
    for _fn in [chart_egress_analysis, chart_intervention_coverage_by_sector,
                chart_rem_egress_pie, chart_rem_ingresos_egresos_mensual]:
        _img_p = _fig_to_png(_fn(df))
        if _img_p:
            pdf.add_page()
            pdf.image(_img_p, x=15, w=180)
            pdf.ln(5)
            _os.unlink(_img_p)

    # ═════════════════════════════════════════════════════════════════════════
    # SECCIÓN 3 – COBERTURA POR PROGRAMA
    # ═════════════════════════════════════════════════════════════════════════
    if "Programa/Unidad" in df.columns:
        if pdf.get_y() > 200:
            pdf.add_page()
        _pdf_section_title(pdf, "3. COBERTURA DE INTERVENCIÓN POR PROGRAMA/UNIDAD")
        grp_prog = df2.groupby("Programa/Unidad").agg(
            total=("tiene_plan", "count"),
            con_plan=("tiene_plan", "sum")
        ).reset_index()
        grp_prog = grp_prog[grp_prog["total"] >= 1].copy()
        grp_prog["pct"] = (grp_prog["con_plan"] / grp_prog["total"] * 100).round(1)
        grp_prog = grp_prog.sort_values("pct", ascending=False)

        if not grp_prog.empty:
            pdf.set_font('helvetica', 'B', 7)
            pdf.set_fill_color(189, 215, 238)
            pdf.cell(100, 6, "Programa / Unidad", border=1, fill=True, align='C')
            pdf.cell(32, 6, "Total", border=1, fill=True, align='C')
            pdf.cell(32, 6, "Con Plan", border=1, fill=True, align='C')
            pdf.cell(26, 6, "Cobertura %", border=1, fill=True, align='C', ln=True)
            pdf.set_font('helvetica', '', 7)
            for i, row_p in grp_prog.iterrows():
                fill = int(i) % 2 == 0
                pdf.set_fill_color(248, 250, 252) if fill else pdf.set_fill_color(255, 255, 255)
                pdf.cell(100, 5, f"  {str(row_p['Programa/Unidad'])[:60]}", border=1, fill=fill)
                pdf.cell(32, 5, str(int(row_p['total'])), border=1, fill=fill, align='C')
                pdf.cell(32, 5, str(int(row_p['con_plan'])), border=1, fill=fill, align='C')
                pdf.cell(26, 5, f"{row_p['pct']:.1f}%", border=1, fill=fill, align='C', ln=True)
            pdf.ln(2)

            # ── Gráfico cobertura por programa (solo con kaleido) ────────
            _img_prog = _fig_to_png(chart_rem_coverage_by_program(df))
            if _img_prog:
                pdf.add_page()
                pdf.image(_img_prog, x=15, w=180)
                pdf.ln(5)
                _os.unlink(_img_prog)

    return bytes(pdf.output())


def render_analytics():
    """Renderiza el dashboard analítico completo en Streamlit."""
    st.html("""
    <div style='background: linear-gradient(135deg,#1F3864,#2E75B6); padding:16px 20px;
                border-radius:8px; margin-bottom:16px;'>
        <h2 style='color:white !important;margin:0;font-size:1.4rem;'>📊 Dashboard Analítico - Riesgo Familiar</h2>
        <p style='color:#BDD7EE !important;margin:4px 0 0;font-size:0.85rem;'>
            Datos en tiempo real del Google Sheet · Actualizar con el botón del sidebar
        </p>
    </div>
    """)

    with st.spinner("Cargando datos del servidor..."):
        # Sincronizar con el filtro global de la app si existe
        est_filter = st.session_state.get('filter_est_main', 'Todos')
        df = load_evaluaciones_df(est_filter=est_filter)

    if df.empty:
        st.info("No hay datos disponibles. Ingresa evaluaciones para ver el análisis.")
        return

    # KPI Row (SaaS Premium Metrics)
    total = len(df)
    alto  = len(df[df["Nivel"]=="RIESGO ALTO"])  if "Nivel" in df.columns else 0
    medio = len(df[df["Nivel"]=="RIESGO MEDIO"]) if "Nivel" in df.columns else 0
    bajo  = len(df[df["Nivel"]=="RIESGO BAJO"])  if "Nivel" in df.columns else 0

    p_alto = f"{alto/total*100:.0f}%" if total else "0%"
    p_medio = f"{medio/total*100:.0f}%" if total else "0%"
    p_bajo = f"{bajo/total*100:.0f}%" if total else "0%"

    kpi_html = f"""
    <div style="display: flex; gap: 16px; margin-bottom: 24px; font-family: 'Inter', sans-serif;">
        <div style="flex: 1; min-width: 150px; background: white; padding: 20px; border-radius: 16px; border: 1px solid #e2e8f0; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);">
            <div style="color: #64748b; font-size: 0.85rem; font-weight: 600; text-transform: uppercase;">Total Evaluaciones</div>
            <div style="color: #0f172a; font-size: 2rem; font-weight: 800; margin-top: 8px; letter-spacing: -0.02em;">{total}</div>
        </div>
        <div style="flex: 1; min-width: 150px; background: white; padding: 20px; border-radius: 16px; border: 1px solid #fecaca; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05); border-left: 4px solid #ef4444;">
            <div style="color: #64748b; font-size: 0.85rem; font-weight: 600; text-transform: uppercase;">Riesgo Alto 🔴</div>
            <div style="display: flex; align-items: baseline; gap: 8px; margin-top: 8px;">
                <div style="color: #ef4444; font-size: 2rem; font-weight: 800; letter-spacing: -0.02em;">{alto}</div>
                <div style="color: #ef4444; font-size: 0.9rem; font-weight: 600; background: #fee2e2; padding: 2px 8px; border-radius: 12px;">{p_alto}</div>
            </div>
        </div>
        <div style="flex: 1; min-width: 150px; background: white; padding: 20px; border-radius: 16px; border: 1px solid #fef08a; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05); border-left: 4px solid #eab308;">
            <div style="color: #64748b; font-size: 0.85rem; font-weight: 600; text-transform: uppercase;">Riesgo Medio 🟡</div>
            <div style="display: flex; align-items: baseline; gap: 8px; margin-top: 8px;">
                <div style="color: #eab308; font-size: 2rem; font-weight: 800; letter-spacing: -0.02em;">{medio}</div>
                <div style="color: #eab308; font-size: 0.9rem; font-weight: 600; background: #fef9c3; padding: 2px 8px; border-radius: 12px;">{p_medio}</div>
            </div>
        </div>
        <div style="flex: 1; min-width: 150px; background: white; padding: 20px; border-radius: 16px; border: 1px solid #bbf7d0; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05); border-left: 4px solid #22c55e;">
            <div style="color: #64748b; font-size: 0.85rem; font-weight: 600; text-transform: uppercase;">Riesgo Bajo 🟢</div>
            <div style="display: flex; align-items: baseline; gap: 8px; margin-top: 8px;">
                <div style="color: #22c55e; font-size: 2rem; font-weight: 800; letter-spacing: -0.02em;">{bajo}</div>
                <div style="color: #22c55e; font-size: 0.9rem; font-weight: 600; background: #dcfce7; padding: 2px 8px; border-radius: 12px;">{p_bajo}</div>
            </div>
        </div>
    </div>
    """
    st.html(kpi_html)

    # ---- REM-P7 KPIs ----
    def _has_plan(row):
        try:
            plan = json.loads(row.get("Plan Intervención JSON", "[]"))
            return len(plan) > 0
        except:
            return False

    df_rem = df.copy()
    if "Plan Intervención JSON" in df.columns:
        df_rem["tiene_plan"] = df_rem.apply(_has_plan, axis=1)
    else:
        df_rem["tiene_plan"] = False

    con_plan_total = int(df_rem["tiene_plan"].sum()) if "tiene_plan" in df_rem.columns else 0
    sin_plan_total = len(df_rem) - con_plan_total
    cobertura_pct = f"{con_plan_total/(con_plan_total+sin_plan_total)*100:.0f}%" if (con_plan_total+sin_plan_total) > 0 else "0%"

    egreso_cols_rem = ['egreso_alta', 'egreso_traslado', 'egreso_derivacion', 'egreso_abandono']
    egresos_total_rem = 0
    for col in egreso_cols_rem:
        if col in df_rem.columns:
            egresos_total_rem += int((df_rem[col].astype(str).str.strip().str.upper().isin(["TRUE","1","VERDADERO"])).sum())

    kpi_rem_html = f"""
    <div style="margin-top: 8px; margin-bottom: 8px;">
        <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 12px;">
            <span style="font-size:0.8rem; font-weight:700; color:#1F3864; text-transform:uppercase; letter-spacing:0.04em;">
            📋 REM-P7 - Métricas del reporte oficial MINSAL
            </span>
            <span style="flex:1; border-bottom:2px solid #BDD7EE;"></span>
        </div>
        <div style="display: flex; gap: 12px; font-family: 'Inter', sans-serif;">
            <div style="flex: 1; min-width: 140px; background: white; padding: 16px 18px; border-radius: 12px; border: 1px solid #e2e8f0; box-shadow: 0 2px 4px -1px rgba(0,0,0,0.04);">
                <div style="color: #64748b; font-size: 0.75rem; font-weight: 600; text-transform: uppercase;">Con plan de intervención</div>
                <div style="color: #2E75B6; font-size: 1.6rem; font-weight: 800; margin-top: 4px;">{con_plan_total}</div>
            </div>
            <div style="flex: 1; min-width: 140px; background: white; padding: 16px 18px; border-radius: 12px; border: 1px solid #e2e8f0; box-shadow: 0 2px 4px -1px rgba(0,0,0,0.04);">
                <div style="color: #64748b; font-size: 0.75rem; font-weight: 600; text-transform: uppercase;">Sin plan (brecha)</div>
                <div style="color: #BDD7EE; font-size: 1.6rem; font-weight: 800; margin-top: 4px;">{sin_plan_total}</div>
            </div>
            <div style="flex: 1; min-width: 140px; background: white; padding: 16px 18px; border-radius: 12px; border: 1px solid #e2e8f0; box-shadow: 0 2px 4px -1px rgba(0,0,0,0.04);">
                <div style="color: #64748b; font-size: 0.75rem; font-weight: 600; text-transform: uppercase;">Cobertura de intervención</div>
                <div style="color: #1F3864; font-size: 1.6rem; font-weight: 800; margin-top: 4px;">{cobertura_pct}</div>
            </div>
            <div style="flex: 1; min-width: 140px; background: white; padding: 16px 18px; border-radius: 12px; border: 1px solid #fecaca; box-shadow: 0 2px 4px -1px rgba(0,0,0,0.04); border-left: 3px solid #C00000;">
                <div style="color: #64748b; font-size: 0.75rem; font-weight: 600; text-transform: uppercase;">Total egresos</div>
                <div style="color: #C00000; font-size: 1.6rem; font-weight: 800; margin-top: 4px;">{egresos_total_rem}</div>
            </div>
        </div>
    </div>
    """
    st.html(kpi_rem_html)

    st.markdown("---")

    # Fila 1: Donut + Barras por sector
    c1, c2 = st.columns(2)
    with c1:
        with st.container(border=True):
            fig = chart_risk_distribution(df)
            if fig: st.plotly_chart(fig, width='stretch', config={"displayModeBar": False})
    with c2:
        with st.container(border=True):
            fig = chart_risk_by_sector(df)
            if fig: st.plotly_chart(fig, width='stretch', config={"displayModeBar": False})

    # Fila 1b: Estratificación por establecimiento
    with st.container(border=True):
        fig = chart_risk_by_establishment(df)
        if fig:
            st.plotly_chart(fig, width='stretch', config={"displayModeBar": False})

    # Fila 2: Top factores de riesgo (ancho completo)
    with st.container(border=True):
        fig = chart_top_risk_factors(df, top_n=12)
        if fig:
            st.plotly_chart(fig, width='stretch', config={"displayModeBar": False})

    # Fila 3: Brecha intervención + Histograma puntajes
    c3, c4 = st.columns(2)
    with c3:
        with st.container(border=True):
            fig = chart_intervention_gap(df)
            if fig: st.plotly_chart(fig, width='stretch', config={"displayModeBar": False})
    with c4:
        with st.container(border=True):
            fig = chart_score_distribution(df)
            if fig: st.plotly_chart(fig, width='stretch', config={"displayModeBar": False})

    # Fila 4: Temporal + Por programa
    c5, c6 = st.columns(2)
    with c5:
        with st.container(border=True):
            fig = chart_evaluations_over_time(df)
            if fig: st.plotly_chart(fig, width='stretch', config={"displayModeBar": False})
    with c6:
        with st.container(border=True):
            fig = chart_by_program(df)
            if fig: st.plotly_chart(fig, width='stretch', config={"displayModeBar": False})

    # Fila 5: REM-P7 - Egresos + Cobertura por sector
    st.markdown("### 📋 Análisis REM-P7")
    c7, c8 = st.columns(2)
    with c7:
        with st.container(border=True):
            fig = chart_egress_analysis(df)
            if fig: st.plotly_chart(fig, width='stretch', config={"displayModeBar": False})
            else: st.caption("No hay datos de egresos disponibles")
    with c8:
        with st.container(border=True):
            fig = chart_intervention_coverage_by_sector(df)
            if fig: st.plotly_chart(fig, width='stretch', config={"displayModeBar": False})
            else: st.caption("No hay datos sectoriales disponibles")

    # Fila 6: REM-P7 - Tendencia mensual (ancho completo)
    st.markdown("### 📈 Tendencia Mensual de Ingresos vs. Egresos")
    with st.container(border=True):
        fig = chart_rem_ingresos_egresos_mensual(df)
        if fig: st.plotly_chart(fig, width='stretch', config={"displayModeBar": False})
        else: st.caption("No hay datos temporales disponibles")

    # Fila 7: REM-P7 - Cobertura por programa + Donut tipos de egreso
    c11, c12 = st.columns(2)
    with c11:
        with st.container(border=True):
            fig = chart_rem_coverage_by_program(df)
            if fig: st.plotly_chart(fig, width='stretch', config={"displayModeBar": False})
            else: st.caption("No hay datos de programas disponibles")
    with c12:
        with st.container(border=True):
            fig = chart_rem_egress_pie(df)
            if fig: st.plotly_chart(fig, width='stretch', config={"displayModeBar": False})
            else: st.caption("No hay tipos de egreso registrados")

    # ── EXPORTAR PDF (Exclusivo Programador) ─────────────────────────────────
    current_role = str(st.session_state.get('user_info', {}).get('rol', '')).lower()
    if current_role == 'programador':
        st.markdown("---")
        st.markdown(
            "<div style='background:linear-gradient(90deg,#1F3864,#2E75B6);padding:12px 18px;"
            "border-radius:8px;margin-bottom:12px;'>"
            "<span style='color:white;font-weight:700;font-size:1rem;'>📥 Exportar Dashboard</span>"
            "<span style='color:#BDD7EE;font-size:0.82rem;margin-left:12px;'>"
            "Genera un reporte PDF ejecutivo con todos los indicadores y gráficos</span></div>",
            unsafe_allow_html=True
        )
        col_btn, col_dl, col_info = st.columns([1, 1, 2])
        with col_btn:
            if st.button("🔄 Generar PDF del Dashboard", type="primary", width='stretch'):
                with st.spinner("Generando reporte PDF completo..."):
                    try:
                        pdf_bytes = generate_dashboard_pdf(df)
                        st.session_state['_dashboard_pdf'] = pdf_bytes
                        st.success("✅ PDF generado correctamente")
                    except Exception as _e:
                        st.error(f"❌ Error al generar PDF: {_e}")
        with col_dl:
            if st.session_state.get('_dashboard_pdf'):
                from datetime import datetime as _dt2
                _fname = f"Dashboard_ERBI_Analitycs_{_dt2.now().strftime('%Y%m%d_%H%M')}.pdf"
                st.download_button(
                    label="⬇️ Descargar PDF",
                    data=st.session_state['_dashboard_pdf'],
                    file_name=_fname,
                    mime="application/pdf",
                    width='stretch',
                )
        with col_info:
            st.caption(
                "El PDF incluye: portada institucional · KPIs generales · "
                "métricas REM-P7 · top factores de riesgo · cobertura por sector y programa · "
                "tendencia mensual · gráficos del dashboard."
            )



    st.markdown(
        f"<div style='text-align:right;font-size:0.75rem;color:#999;margin-top:8px;'>"
        f"Datos actualizados · {len(df)} evaluaciones cargadas</div>",
        unsafe_allow_html=True
    )
