import re

ruta = r'D:\PROYECTOS PROGRAMACIÓN\ANTIGRAVITY_PROJECTS\encuesta_riesgo\analytics.py'

with open(ruta, 'r', encoding='utf-8') as f:
    content = f.read()

# ============================================================
# CAMBIO 1: Insertar dos funciones ANTES de def render_analytics():
# ============================================================

funcs_code = '''

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
    
    sector_cols = []
    if "Sector" in df.columns:
        sector_cols = ["Sol", "Luna"]
        sector_data = {}
        for col in available:
            sector_data[col] = {}
            for s in sector_cols:
                mask = (df["Sector"].str.strip().str.lower() == s.lower()) & \
                       (df[col].astype(str).str.strip().str.upper().isin(["TRUE","1","VERDADERO"]))
                sector_data[col][s] = int(mask.sum())
    
    colors_egress = {
        'egreso_alta': VERDE_OK,
        'egreso_traslado': AZUL_MED,
        'egreso_derivacion': NARANJA,
        'egreso_abandono': ROJO
    }
    
    fig = go.Figure()
    for col in available:
        if sector_cols:
            vals = [sector_data[col].get(s, 0) for s in sector_cols]
        else:
            total_val = int((df[col].astype(str).str.strip().str.upper().isin(["TRUE","1","VERDADERO"])).sum())
            vals = [total_val]
        
        fig.add_trace(go.Bar(
            name=egreso_labels.get(col, col),
            x=sector_cols if sector_cols else ["Total"],
            y=vals,
            marker_color=colors_egress.get(col, GRIS),
            text=vals,
            textposition="inside",
            textfont=dict(color="white", size=11, family="Roboto Bold"),
            hovertemplate=f"{egreso_labels.get(col, col)}: %{{y}} familias<extra></extra>",
        ))
    
    fig.update_layout(
        barmode="group",
        title=dict(
            text="<b>Egresos de planes de intervencion por tipo y sector</b><br>"
                 "<span style='font-size:11px;color:#64748b;font-weight:normal'>"
                 "REM-P7: Causas de egreso (Alta, Traslado, Derivacion, Abandono)</span>",
            font=dict(size=14, color=AZUL_OSCURO), x=0, xanchor='left'
        ),
        plot_bgcolor="white", paper_bgcolor="white",
        margin=dict(l=10, r=10, t=75, b=10),
        font=dict(family="Roboto, Arial"),
        showlegend=True,
        legend=dict(orientation="h", y=1.15, x=0.5, xanchor="center", font_size=10),
        xaxis=dict(showgrid=False, showline=False),
        yaxis=dict(showgrid=True, gridcolor="#F0F0F0", title="N° Familias", rangemode="tozero"),
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
            plan = json.loads(row.get("Plan Intervencion JSON", "[]"))
            return len(plan) > 0
        except:
            return False
    
    df = df.copy()
    if "Plan Intervencion JSON" in df.columns:
        df["tiene_plan"] = df.apply(has_plan, axis=1)
    else:
        df["tiene_plan"] = False
    
    sectores = ["Sol", "Luna"]
    labels_map = {"Sol": "Sol (Urbano)", "Luna": "Luna (Rural)"}
    available_sectors = [s for s in sectores if s in df["Sector"].unique()]
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
                 "<span style='font-size:11px;color:#64748b;font-weight:normal'>"
                 "REM-P7: Familias con y sin plan de intervencion por sector</span>",
            font=dict(size=14, color=AZUL_OSCURO), x=0, xanchor='left'
        ),
        plot_bgcolor="white", paper_bgcolor="white",
        margin=dict(l=10, r=30, t=75, b=10),
        font=dict(family="Roboto, Arial"),
        showlegend=True,
        legend=dict(orientation="h", y=1.12, x=1, xanchor="right", font_size=11),
        xaxis=dict(showgrid=False, showline=False),
        yaxis=dict(showgrid=True, gridcolor="#F0F0F0", title="N° Familias", rangemode="tozero"),
    )
    return fig

'''

content = content.replace('def render_analytics():', funcs_code + '\ndef render_analytics():', 1)

# ============================================================
# CAMBIO 2: Reemplazar st.html(kpi_html)\\n\\n    st.markdown("---")
# with new KPI block
# ============================================================

old_kpi = '''    st.html(kpi_html)

    st.markdown("---")'''

new_kpi = '''    st.html(kpi_html)

    # ---- REM-P7 KPIs ----
    def _has_plan(row):
        try:
            plan = json.loads(row.get("Plan Intervenci\u00f3n JSON", "[]"))
            return len(plan) > 0
        except:
            return False

    df_rem = df.copy()
    if "Plan Intervenci\u00f3n JSON" in df.columns:
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

    kpi_rem_html = f\"""
    <div style="margin-top: 8px; margin-bottom: 8px;">
        <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 12px;">
            <span style="font-size:0.8rem; font-weight:700; color:#1F3864; text-transform:uppercase; letter-spacing:0.04em;">
            \U0001f4cb REM-P7 \u2014 M\u00e9tricas del reporte oficial MINSAL
            </span>
            <span style="flex:1; border-bottom:2px solid #BDD7EE;"></span>
        </div>
        <div style="display: flex; gap: 12px; font-family: 'Inter', sans-serif;">
            <div style="flex: 1; min-width: 140px; background: white; padding: 16px 18px; border-radius: 12px; border: 1px solid #e2e8f0; box-shadow: 0 2px 4px -1px rgba(0,0,0,0.04);">
                <div style="color: #64748b; font-size: 0.75rem; font-weight: 600; text-transform: uppercase;">Con plan de intervenci\u00f3n</div>
                <div style="color: #2E75B6; font-size: 1.6rem; font-weight: 800; margin-top: 4px;">{con_plan_total}</div>
            </div>
            <div style="flex: 1; min-width: 140px; background: white; padding: 16px 18px; border-radius: 12px; border: 1px solid #e2e8f0; box-shadow: 0 2px 4px -1px rgba(0,0,0,0.04);">
                <div style="color: #64748b; font-size: 0.75rem; font-weight: 600; text-transform: uppercase;">Sin plan (brecha)</div>
                <div style="color: #BDD7EE; font-size: 1.6rem; font-weight: 800; margin-top: 4px;">{sin_plan_total}</div>
            </div>
            <div style="flex: 1; min-width: 140px; background: white; padding: 16px 18px; border-radius: 12px; border: 1px solid #e2e8f0; box-shadow: 0 2px 4px -1px rgba(0,0,0,0.04);">
                <div style="color: #64748b; font-size: 0.75rem; font-weight: 600; text-transform: uppercase;">Cobertura de intervenci\u00f3n</div>
                <div style="color: #1F3864; font-size: 1.6rem; font-weight: 800; margin-top: 4px;">{cobertura_pct}</div>
            </div>
            <div style="flex: 1; min-width: 140px; background: white; padding: 16px 18px; border-radius: 12px; border: 1px solid #fecaca; box-shadow: 0 2px 4px -1px rgba(0,0,0,0.04); border-left: 3px solid #C00000;">
                <div style="color: #64748b; font-size: 0.75rem; font-weight: 600; text-transform: uppercase;">Total egresos</div>
                <div style="color: #C00000; font-size: 1.6rem; font-weight: 800; margin-top: 4px;">{egresos_total_rem}</div>
            </div>
        </div>
    </div>
    \"""
    st.html(kpi_rem_html)

    st.markdown("---")'''

content = content.replace(old_kpi, new_kpi, 1)

# ============================================================
# CAMBIO 3: Añadir Fila REM-P7 después de Fila 4
# ============================================================

old_fila4 = '''    # Fila 4: Temporal + Por programa
    c5, c6 = st.columns(2)
    with c5:
        with st.container(border=True):
            fig = chart_evaluations_over_time(df)
            if fig: st.plotly_chart(fig, width='stretch', config={"displayModeBar": False})
    with c6:
        with st.container(border=True):
            fig = chart_by_program(df)
            if fig: st.plotly_chart(fig, width='stretch', config={"displayModeBar": False})

    st.markdown('''

new_fila4 = '''    # Fila 4: Temporal + Por programa
    c5, c6 = st.columns(2)
    with c5:
        with st.container(border=True):
            fig = chart_evaluations_over_time(df)
            if fig: st.plotly_chart(fig, width='stretch', config={"displayModeBar": False})
    with c6:
        with st.container(border=True):
            fig = chart_by_program(df)
            if fig: st.plotly_chart(fig, width='stretch', config={"displayModeBar": False})

    # Fila 5: REM-P7 — Egresos + Cobertura por sector
    st.markdown("### \U0001f4cb An\u00e1lisis REM-P7")
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

    st.markdown('''

content = content.replace(old_fila4, new_fila4, 1)

# ============================================================
# Verify
# ============================================================

assert 'def chart_egress_analysis(df):' in content, 'Change 1 FAILED: chart_egress_analysis not found'
assert 'def chart_intervention_coverage_by_sector(df):' in content, 'Change 1 FAILED: chart_intervention_coverage_by_sector not found'
assert 'kpi_rem_html' in content, 'Change 2 FAILED: kpi_rem_html not found'
assert 'st.html(kpi_rem_html)' in content, 'Change 2 FAILED: st.html(kpi_rem_html) not found'
assert 'An\u00e1lisis REM-P7' in content, 'Change 3 FAILED: "An\u00e1lisis REM-P7" not found'
assert 'chart_egress_analysis(df)' in content, 'Change 3 FAILED: chart_egress_analysis call not found'

with open(ruta, 'w', encoding='utf-8') as f:
    f.write(content)

compile(content, 'analytics.py', 'exec')

print('=== All 3 changes applied successfully ===')
print(f'File size: {len(content)} chars, ~{content.count(chr(10))+1} lines')
print('Compilation: OK')
print('Verification: chart_egress_analysis found =', 'def chart_egress_analysis(df):' in content)
print('Verification: chart_intervention_coverage_by_sector found =', 'def chart_intervention_coverage_by_sector(df):' in content)
print('Verification: kpi_rem_html found =', 'kpi_rem_html' in content)
print('Verification: Análisis REM-P7 found =', 'An\u00e1lisis REM-P7' in content)
