import streamlit as st
import pandas as pd

@st.fragment
def render_family_fragment():
    edited_family = st.data_editor(
        st.session_state.family_members,
        num_rows="dynamic",
        width='stretch',
        key="family_editor",
        hide_index=True,
        column_config={
            "Nombre y Apellidos": st.column_config.TextColumn("Nombre y Apellidos", width="large"),
            "RUT": st.column_config.TextColumn("RUT", width="medium"),
            "F. Nac": st.column_config.DateColumn("F. Nac", width="small", format="DD/MM/YYYY"),
            "Identidad de género": st.column_config.SelectboxColumn(
                "Identidad de género", 
                options=["Masculino", "Femenino", "No binario", "Transgénero", "Prefiero no decir", "Gestación/Aborto"], 
                width="medium"
            ),
            "Pueblo Originario": st.column_config.SelectboxColumn(
                "Etnia",
                options=PUEBLO_ORIGINARIO_OPTIONS,
                width="medium"
            ),
            "Nacionalidad": st.column_config.TextColumn("Nacionalidad", width="medium"),
            "E. Civil": st.column_config.SelectboxColumn(
                "E. Civil", 
                options=["Soltero/a (S)", "Casado/a (C)", "Conviviente (Co)", "Divorciado/a (D)", "Separado/a (Sep)", "Viudo/a (V)", "Fallecido/a (F)", "Espontáneo", "Provocado"], 
                width="medium"
            ),
            "Ocupación": st.column_config.TextColumn("Ocupación", width="medium"),
            "Parentesco": st.column_config.SelectboxColumn(
                "Parentesco",
                options=PARENTESCO_FAMILIA_OPTIONS,
                width="medium"
            ),
            "Cronico": st.column_config.CheckboxColumn("Cron.", width="small", default=False),
            "Resp": st.column_config.CheckboxColumn("Resp", width="small", default=False),
        }
    )
    if edited_family is not None and 'F. Nac' in edited_family.columns:
        def to_date_safe_fnac(x):
            try:
                return pd.to_datetime(x, dayfirst=True).date() if pd.notnull(x) and str(x).strip() != "" else None
            except:
                return None
        edited_family['F. Nac'] = edited_family['F. Nac'].apply(to_date_safe_fnac)
        
    st.session_state.family_members = edited_family
    
    # --- VALIDACIÓN DE RUTS DUPLICADOS ---
    all_ruts = get_all_ruts_mapping()
    current_eval_id = st.session_state.get('idEvaluacion', '')
    
    dupes_found = []
    for idx, m_row in edited_family.iterrows():
        m_rut = str(m_row.get("RUT", "")).strip().upper()
        if m_rut in all_ruts:
            fam_name, other_id = all_ruts[m_rut]
            if other_id != current_eval_id:
                dupes_found.append(f"• **{m_rut}** ({m_row.get('Nombre y Apellidos', 'Sin nombre')}) ya existe en la familia: **{fam_name}** (ID: {other_id})")
    if dupes_found:
        st.warning("⚠️ **Alerta de Duplicidad detectada:**\n\n" + "\n".join(dupes_found))

@st.fragment
def render_plan_fragment():
    edited_plan = st.data_editor(
        st.session_state.intervention_plan,
        num_rows="dynamic",
        width='stretch',
        key="intervention_editor",
        hide_index=True,
        column_config={
            "Objetivo": st.column_config.TextColumn("OBJETIVO"),
            "Actividad": st.column_config.TextColumn("ACTIVIDAD"),
            "Fecha Prog": st.column_config.DateColumn("FECHA PROG."),
            "Responsable": st.column_config.TextColumn("RESPONSABLE"),
            "Fecha Real": st.column_config.DateColumn("FECHA REAL."),
            "Evaluación": st.column_config.TextColumn("EVALUACIÓN"),
            "Estado": st.column_config.SelectboxColumn(
                "ESTADO",
                options=["Pendiente", "En progreso", "Completado", "Cancelado"],
                width="medium"
            ),
            "F. Seguimiento": st.column_config.DateColumn("F. SEGUIMIENTO"),
            "Obs. Seguimiento": st.column_config.TextColumn("OBS. SEGUIMIENTO"),
        }
    )
    if edited_plan is not None:
        for col in ["Fecha Prog", "Fecha Real"]:
            if col in edited_plan.columns:
                 def to_date_safe(x):
                     try:
                         return pd.to_datetime(x).date() if pd.notnull(x) else None
                     except:
                         return None
                 edited_plan[col] = edited_plan[col].apply(to_date_safe)
        st.session_state.intervention_plan = edited_plan

@st.fragment
def render_seg_fragment():
    if 'seguimiento_plan' not in st.session_state:
        st.session_state.seguimiento_plan = pd.DataFrame({
            "Objetivo": pd.Series(dtype='str'),
            "Actividad": pd.Series(dtype='str'),
            "Estado": pd.Series(dtype='str'),
            "F. Seguimiento": pd.Series(dtype='object'),
            "Obs. Seguimiento": pd.Series(dtype='str'),
        })
    edited_seg = st.data_editor(
        st.session_state.seguimiento_plan,
        num_rows="dynamic",
        width='stretch',
        key="seguimiento_editor",
        hide_index=True,
        column_config={
            "Objetivo": st.column_config.TextColumn("OBJETIVO", width="large"),
            "Actividad": st.column_config.TextColumn("ACTIVIDAD", width="large"),
            "Estado": st.column_config.SelectboxColumn(
                "ESTADO",
                options=["Pendiente", "En progreso", "Completado", "Cancelado"],
                width="medium",
            ),
            "F. Seguimiento": st.column_config.DateColumn("FECHA SEGUIMIENTO", width="medium"),
            "Obs. Seguimiento": st.column_config.TextColumn("OBSERVACIONES", width="large"),
        }
    )
    st.session_state.seguimiento_plan = edited_seg

@st.fragment
def render_team_fragment():
    edited_team = st.data_editor(
        st.session_state.team_members,
        num_rows="dynamic",
        width='stretch',
        key="team_editor",
        hide_index=True,
        column_config={
            "Nombre y Profesión": st.column_config.TextColumn("Registrar Nombre Completo", width="large"),
            "Firma": st.column_config.CheckboxColumn("Firma Digital", width="small"),
        }
    )
    st.session_state.team_members = edited_team
