"""
analytics.py — Dashboard estadístico para encuesta_riesgo.
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


def load_evaluaciones_df():
    """Carga el DataFrame de evaluaciones con caché inteligente de datos crudos + filtrado dinámico RBAC."""
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
            SHEET_URL = "https://docs.google.com/spreadsheets/d/1JjYw2W6c-N2swGPuIHbz0CU7aDhh1pA-6VH1WuXV41w/edit"
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
            if 'encargado' in user_cargo_clean and 'postas' in user_cargo_clean:
                df = df[df['Sector'].str.strip().str.lower() == 'luna']
            elif 'sector sol' in user_unit_clean or 'sector sol' in user_cargo_clean:
                df = df[df['Sector'].str.strip().str.lower() == 'sol']
            elif 'sector luna' in user_unit_clean or 'sector luna' in user_cargo_clean:
                df = df[df['Sector'].str.strip().str.lower() == 'luna']
            # Filtro por Programa
            elif user_unit_clean:
                 if 'Programa/Unidad' in df.columns:
                     df = df[df['Programa/Unidad'].str.strip().str.lower().str.contains(user_unit_clean)]
    
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
        margin=dict(l=10, r=10, t=70, b=10),
        font=dict(family="Roboto, Arial"),
        showlegend=True,
        legend=dict(orientation="h", y=-0.1, x=0.5, xanchor="center", font_size=11),
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
        vals = [len(df[(df["Sector"]==s) & (df["Nivel"]==nivel)]) for s in sectores]
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
        title=dict(text="<b>Riesgo familiar por sector territorial</b><br><span style='font-size:11px;color:#666'>Sol=Urbano · Luna=Rural</span>",
                   font=dict(size=14, color=AZUL_OSCURO), x=0, xanchor='left'),
        plot_bgcolor="white", paper_bgcolor="white",
        margin=dict(l=10, r=10, t=70, b=10),
        font=dict(family="Roboto, Arial"),
        showlegend=True,
        legend=dict(orientation="h", y=1.12, x=1, xanchor="right", font_size=11),
        xaxis=dict(showgrid=False, showline=False),
        yaxis=dict(showgrid=True, gridcolor="#F0F0F0", title="N° Familias"),
    )
    return fig


def chart_top_risk_factors(df, top_n=12):
    """
    BAR HORIZONTAL ordenado: Top N factores de riesgo más frecuentes.
    SWD: "Show what matters" — resaltar los top 3, resto en gris. Etiquetas directas.
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
        margin=dict(l=10, r=80, t=70, b=10),
        font=dict(family="Roboto, Arial"),
        showlegend=False,
        xaxis=dict(showgrid=False, showline=False, zeroline=False, tickfont_size=10),
        yaxis=dict(showgrid=False, showline=False, autorange="reversed", tickfont_size=10),
        height=max(300, top_n * 32),
    )
    return fig


def chart_intervention_gap(df):
    """
    BAR APILADO: Familias con vs sin plan de intervención por nivel de riesgo.
    SWD: Muestra la "brecha de intervención" — insight accionable.
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
        title=dict(text="<b>Brecha de intervención por nivel de riesgo</b><br><span style='font-size:11px;color:#666'>Familias con plan vs. sin plan asignado</span>",
                   font=dict(size=14, color=AZUL_OSCURO), x=0, xanchor='left'),
        plot_bgcolor="white", paper_bgcolor="white",
        margin=dict(l=10, r=10, t=70, b=10),
        font=dict(family="Roboto, Arial"),
        showlegend=True,
        legend=dict(orientation="h", y=1.12, x=1, xanchor="right", font_size=11),
        xaxis=dict(showgrid=False, showline=False),
        yaxis=dict(showgrid=True, gridcolor="#F0F0F0", title="N° Familias"),
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
        margin=dict(l=10, r=10, t=70, b=10),
        font=dict(family="Roboto, Arial"),
        showlegend=False,
        xaxis=dict(showgrid=False, showline=False, tickformat="%b %Y"),
        yaxis=dict(showgrid=True, gridcolor="#F0F0F0", title="Evaluaciones", rangemode="tozero"),
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
        margin=dict(l=10, r=10, t=70, b=10),
        font=dict(family="Roboto, Arial"),
        showlegend=False,
        xaxis=dict(title="Puntaje", showgrid=False, showline=False, range=[0, 60]),
        yaxis=dict(title="N° Familias", showgrid=True, gridcolor="#F0F0F0"),
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
        margin=dict(l=10, r=80, t=70, b=10),
        font=dict(family="Roboto, Arial"),
        showlegend=False,
        xaxis=dict(showgrid=False, showline=False, zeroline=False, title="Puntaje promedio"),
        yaxis=dict(showgrid=False, showline=False, tickfont_size=10),
        height=max(250, len(grp) * 35),
    )
    return fig


def render_analytics():
    """Renderiza el dashboard analítico completo en Streamlit."""
    st.markdown("""
    <div style='background: linear-gradient(135deg,#1F3864,#2E75B6); padding:16px 20px;
                border-radius:8px; margin-bottom:16px;'>
        <h2 style='color:white !important;margin:0;font-size:1.4rem;'>📊 Dashboard Analítico — Riesgo Familiar</h2>
        <p style='color:#BDD7EE;margin:4px 0 0;font-size:0.85rem;'>
            Datos en tiempo real del Google Sheet · Actualizar con el botón del sidebar
        </p>
    </div>
    """, unsafe_allow_html=True)

    with st.spinner("Cargando datos del servidor..."):
        df = load_evaluaciones_df()

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

    st.markdown("---")

    # Fila 1: Donut + Barras sector
    c1, c2 = st.columns(2)
    with c1:
        with st.container(border=True):
            fig = chart_risk_distribution(df)
            if fig: st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    with c2:
        with st.container(border=True):
            fig = chart_risk_by_sector(df)
            if fig: st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    # Fila 2: Top factores de riesgo (ancho completo)
    with st.container(border=True):
        fig = chart_top_risk_factors(df, top_n=12)
        if fig:
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    # Fila 3: Brecha intervención + Histograma puntajes
    c3, c4 = st.columns(2)
    with c3:
        with st.container(border=True):
            fig = chart_intervention_gap(df)
            if fig: st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    with c4:
        with st.container(border=True):
            fig = chart_score_distribution(df)
            if fig: st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    # Fila 4: Temporal + Por programa
    c5, c6 = st.columns(2)
    with c5:
        with st.container(border=True):
            fig = chart_evaluations_over_time(df)
            if fig: st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    with c6:
        with st.container(border=True):
            fig = chart_by_program(df)
            if fig: st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    st.markdown(
        f"<div style='text-align:right;font-size:0.75rem;color:#999;margin-top:8px;'>"
        f"Datos actualizados · {len(df)} evaluaciones cargadas</div>",
        unsafe_allow_html=True
    )
