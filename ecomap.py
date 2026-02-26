"""
ecomap.py — Generador de Ecomapa clínico (Graphviz Open Source).
Basado exactamente en la Imagen 1 con soporte para construcción manual.
"""
import graphviz

# Paleta Estándar (Protocolo San Juan)
FAMILY_CORE_BG = "#E2E8F0" # Gris azulado suave
SYSTEM_BG      = "#EDF2F7" # Gris muy claro
LINK_STRONG    = "#1F3864" # Azul Intenso
LINK_MODERATE  = "#718096" # Gris
LINK_STRESS    = "#C53030" # Rojo Alerta
LINK_WEAK      = "#CBD5E0" # Gris claro

def generate_ecomap_dot(family_name: str, members: list, active_risks: dict, programa: str, nivel_riesgo: str, selected_systems: list = None, system_flows: dict = None):
    """
    Genera el código DOT de Graphviz para el Ecomapa (Layout Radial).
    system_flows: dict { 'Sistema': 'in'|'out'|'both' }
    """
    dot = graphviz.Digraph(comment=f'Ecomapa {family_name}', engine='twopi')
    dot.attr(ranksep='2.5', overlap='false', splines='true', bgcolor='white')
    
    # Nodo Central (Familia)
    dot.node('family_core', 
             label=f'FAMILIA\n{family_name}', 
             shape='ellipse', 
             style='filled,bold', 
             fillcolor=FAMILY_CORE_BG, 
             fontname='Inter, Arial Bold',
             fontsize='14',
             width='2.5',
             height='1.8')
    
    # Definición de Redes según Protocolo SJ
    # Primarias (más cerca) / Secundarias (más lejos)
    redes_info = {
        "AMIGOS": {"tipo": "PRIMARIA", "default": "MODERATE"},
        "VECINOS": {"tipo": "PRIMARIA", "default": "MODERATE"},
        "RED FAMILIAR": {"tipo": "PRIMARIA", "default": "STRONG"},
        "CESFAM": {"tipo": "SECUNDARIA", "default": "MODERATE"},
        "RELIGIÓN": {"tipo": "SECUNDARIA", "default": "MODERATE"},
        "TRABAJO": {"tipo": "SECUNDARIA", "default": "MODERATE"},
        "ESCUELA": {"tipo": "SECUNDARIA", "default": "MODERATE"},
        "COMUNIDAD": {"tipo": "SECUNDARIA", "default": "MODERATE"},
        "JUSTICIA": {"tipo": "SECUNDARIA", "default": "MODERATE"}
    }

    # Dinamismo basado en riesgos
    if any(k in active_risks for k in ['t1_vif', 't2_judicial']): redes_info["JUSTICIA"]["default"] = "STRESS"
    if active_risks.get('t3_cesantia'): redes_info["TRABAJO"]["default"] = "WEAK"
    if active_risks.get('t3_desercionEscolar'): redes_info["ESCUELA"]["default"] = "STRESS"

    # Determinar qué renderizar
    if selected_systems:
        systems_to_render = {k: redes_info.get(k, {"tipo": "SECUNDARIA", "default": "MODERATE"}) for k in selected_systems}
    else:
        # Default de la guía
        systems_to_render = {k: v for k, v in redes_info.items() if k in ["CESFAM", "TRABAJO", "RED FAMILIAR", "COMUNIDAD"]}

    for name, info in systems_to_render.items():
        etype = info["default"]
        is_primary = info["tipo"] == "PRIMARIA"
        
        # Estilo de arista
        color = LINK_MODERATE
        width = "2"
        style = "solid"
        
        if etype == "STRONG":
            color = LINK_STRONG
            width = "6" 
        elif etype == "STRESS":
            color = LINK_STRESS
            width = "3"
            style = "dashed"
        elif etype == "WEAK":
            color = LINK_WEAK
            width = "1"
            style = "dotted"

        # Flujo de energía (Flechas)
        flow = (system_flows or {}).get(name, "both")
        arrowhead = "normal"
        dir_attr = "both" # Default bidireccional
        
        if flow == "in": dir_attr = "back"
        elif flow == "out": dir_attr = "forward"
        elif flow == "none": arrowhead = "none"; dir_attr = "none"

        # Nodo Sistema
        dist = "1.2" if is_primary else "2.2"
        dot.node(name, shape='ellipse', style='filled', fillcolor=SYSTEM_BG, 
                 fontname='Inter, Arial', fontsize='10', width='1.4',
                 tooltip=f"Red {info['tipo']}")
        
        # Relación
        dot.edge('family_core', name, color=color, penwidth=width, style=style, 
                 arrowhead=arrowhead, dir=dir_attr, arrowsize="0.8")
        
    return dot
