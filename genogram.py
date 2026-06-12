"""
genogram.py — Generador de Genograma clínico (Graphviz).
Implementado según la guía oficial:
  "Procedimiento de Construcción de Genogramas" — Gobierno de Chile.
"""
import graphviz
from datetime import date

# ─── Paleta Clínica Oficial ───────────────────────────────────────────────────
BORDER_DARK    = "#1A365D"
FILL_MALE      = "#EBF4FF"
FILL_FEMALE    = "#FFF0F6"
FILL_INDEX     = "#FFFBEB"
FILL_DECEASED  = "#E2E8F0"
EDGE_COLOR     = "#2D3748"
EDGE_UNION     = "#1A365D"
UNION_COLOR    = "#1A365D"

def get_generation_level(parentesco: str) -> int:
    """Nivel generacional (1=Abuelos → 5=Nietos)."""
    p = str(parentesco).strip().upper()
    if any(x in p for x in ["ABUEL", "BISABUEL"]): return 1
    if any(x in p for x in ["PADRE", "MADRE", "SUEGR", "TÍO", "TIA", "TIO", "TUAT"]): return 2
    if any(x in p for x in ["JEFE", "CÓNYUGE", "CONYUGUE", "PAREJA", "CONVIV", "HERMANO", "HERMANA", "HERMAN"]): return 3
    if any(x in p for x in ["HIJO", "HIJA", "NIÑO", "SOBRIN", "ADOP", "ACOGIDA"]): return 4
    if any(x in p for x in ["NIETO", "NIETA", "BIZNIETO"]): return 5
    return 3

def _detect_sex(sexo_raw: str) -> str:
    s = str(sexo_raw).strip().upper()
    if s in ("G", "GESTACION", "GESTACIÓN", "EMBARAZO", "GESTACIÓN/ABORTO"): return "G"
    if s in ("F", "FEM", "FEMENINO", "MUJER"): return "F"
    if s in ("M", "MAS", "MASCULINO", "HOMBRE", "H"): return "M"
    if s in ("NO BINARIO", "TRANSGÉNERO", "TRANSGENERO", "OTRO", "NB"): return "NB"
    return "?"

def _build_node_label(nombre: str, edad: str, parentesco: str, is_deceased: bool, 
                      is_index: bool, y_nac: str, y_def: str, sex: str) -> str:
    """Construye el label HTML del nodo con info clínica y años en las esquinas inferiores."""
    nombre_corto = nombre[:22]
    # Si falta info vital (edad), usar "?"
    display_edad = edad if edad and str(edad).isdigit() else "?"
    if sex == "?":
        display_edad = "?"

    n_text = f"n. {y_nac}" if y_nac else ""
    d_text = f"d. {y_def}" if y_def and is_deceased else ""
    fallecido_tag = '<BR/><FONT POINT-SIZE="9" COLOR="#C53030">[✝ Fallecido/a]</FONT>' if is_deceased else ""

    # Usar tabla HTML invisible para posicionar texto dentro de la figura principal
    label_html = f'''<<TABLE BORDER="0" CELLBORDER="0" CELLSPACING="0" CELLPADDING="0">
    <TR>
        <TD COLSPAN="3" ALIGN="CENTER" VALIGN="BOTTOM">
            <B>{nombre_corto}</B><BR/>
            <FONT POINT-SIZE="8">{parentesco}</FONT>{fallecido_tag}
            <BR/><BR/><FONT POINT-SIZE="14"><B>{display_edad}</B></FONT><BR/>
        </TD>
    </TR>
    <TR>
        <TD ALIGN="LEFT" VALIGN="BOTTOM" WIDTH="25"><FONT POINT-SIZE="8" COLOR="#4A5568">{n_text}</FONT></TD>
        <TD ALIGN="CENTER" VALIGN="BOTTOM" WIDTH="10"></TD>
        <TD ALIGN="RIGHT" VALIGN="BOTTOM" WIDTH="25"><FONT POINT-SIZE="8" COLOR="#4A5568">{d_text}</FONT></TD>
    </TR>
    </TABLE>>'''
    return label_html

def generate_genogram_dot(members: list, family_name: str = "", nivel_riesgo: str = "",
                           tipo_union: str = "Casados", interpersonal_relations: list = None):
    dot = graphviz.Digraph(
        comment=f"Genograma {family_name}",
        graph_attr={
            "rankdir": "TB", "splines": "ortho", "nodesep": "0.9", "ranksep": "0.7",
            "newrank": "true", "bgcolor": "white", "fontname": "Arial",
            "label": f"Genograma Familiar — {family_name}", "labelloc": "t", "fontsize": "14",
        }
    )
    dot.attr("node", fontname="Arial", style="filled", penwidth="2", color=BORDER_DARK)

    nodes_info: dict[str, dict] = {}
    levels: dict[int, list[str]] = {1: [], 2: [], 3: [], 4: [], 5: []}
    today_year = date.today().year

    for i, m in enumerate(members):
        nombre = str(m.get("Nombre y Apellidos", f"Miembro {i+1}"))
        sexo_raw = str(m.get("Identidad de género", m.get("Sexo", "?")))
        is_index = bool(m.get("Resp", False)) or str(m.get("Resp", "")).upper() == "TRUE"
        parentesco = str(m.get("Parentesco", "Familiar"))
        
        edad_val = str(m.get("Edad", ""))
        fnac = str(m.get("F. Nac", ""))
        y_nac = fnac.split("/")[-1] if "/" in fnac else fnac[:4]
        if not edad_val and y_nac.isdigit():
            edad_val = str(today_year - int(y_nac))
            
        is_deceased = any(x in str(m.get("E. Civil", "")).upper() for x in ["FALLEC", "F"]) or "FALLEC" in str(m.get("Estado", "")).upper()
        fdef = str(m.get("F. Def", m.get("Fecha Defunción", "")))
        y_def = fdef.split("/")[-1] if "/" in fdef else fdef[:4]

        sex = _detect_sex(sexo_raw)
        nid = f"m{i}"
        level = get_generation_level(parentesco)
        levels[level].append(nid)

        if sex == "M":
            shape, fillcolor = "box", FILL_MALE
        elif sex == "F":
            shape, fillcolor = "ellipse", FILL_FEMALE
        elif sex == "G":
            shape, fillcolor = "triangle", "white"
            if "MORTINATO" in str(m.get("E. Civil", "")).upper() or "MORTINATO" in str(m.get("Estado", "")).upper(): 
                shape = "square"
        elif sex == "NB":
            shape, fillcolor = "diamond", "#E9D8FD"
        else:
            shape, fillcolor = "diamond", "white"

        if is_deceased: fillcolor = FILL_DECEASED
        
        raw_chronic = m.get("Cronico")
        is_chronic = raw_chronic if isinstance(raw_chronic, bool) else str(raw_chronic).upper() in ("TRUE", "1", "SÍ", "SI", "X")
        if not is_chronic: is_chronic = str(m.get("Enfermedad", "")).upper() in ("TRUE", "1", "SÍ", "SI", "X")
        
        color = "#C53030" if is_chronic else BORDER_DARK
        penwidth = "4" if is_chronic else "2"
        peripheries = "2" if is_index else "1"

        status = str(m.get("E. Civil", "")).upper()
        label = _build_node_label(nombre, edad_val, parentesco, is_deceased, is_index, 
                                  y_nac if y_nac.isdigit() else "", 
                                  y_def if y_def.isdigit() else "", sex)
        if sex == "G":
            if "ESPONT" in status: label = "●"
            elif "PROVOC" in status or "INDUC" in status or "MORTINATO" in status: label = "X"
            else: label = ""

        dot.node(nid, label=label, shape=shape, fillcolor=fillcolor, color=color,
                 penwidth=penwidth, peripheries=peripheries,
                 fontsize="10" if sex == "G" else "14",
                 width="0.3" if "MORTINATO" in status else "0.75",
                 height="0.3" if "MORTINATO" in status else "0.75")

        nodes_info[nid] = {
            "level": level, "parentesco": parentesco.upper(), "is_index": is_index,
            "sex": sex, "is_deceased": is_deceased, "edad": int(edad_val) if str(edad_val).isdigit() else -1,
            "y_nac": int(y_nac) if y_nac.isdigit() else 0
        }

    # ── 2. LÓGICA DE NODOS FANTASMAS (Generación 2) ───────────────────────────
    jefe_ids = [nid for nid, info in nodes_info.items() if "JEFE" in info["parentesco"]]
    pareja_ids = [nid for nid, info in nodes_info.items() if any(x in info["parentesco"] for x in ["CÓNYUGE", "CONYUGUE", "PAREJA", "CONVIV"])]
    colaterales_ids = [nid for nid in levels[3] if nid not in jefe_ids and nid not in pareja_ids and "HERMAN" in nodes_info[nid]["parentesco"]]
    
    jefe_id = jefe_ids[0] if jefe_ids else None
    pareja_id = pareja_ids[0] if pareja_ids else None

    # Si hay jefe y hermanos pero no hay padres, crear padres fantasmas (Regla 3 Generaciones Mínimas)
    if jefe_id and colaterales_ids and not levels[2]:
        ghost_padre = "ghost_padre"
        ghost_madre = "ghost_madre"
        dot.node(ghost_padre, label="?", shape="box", style="dashed", color=EDGE_COLOR, fillcolor="white")
        dot.node(ghost_madre, label="?", shape="ellipse", style="dashed", color=EDGE_COLOR, fillcolor="white")
        
        levels[2].extend([ghost_padre, ghost_madre])
        nodes_info[ghost_padre] = {"sex": "M", "level": 2}
        nodes_info[ghost_madre] = {"sex": "F", "level": 2}

    # ── 3. DELIMITACIÓN DE HOGAR (CLUSTER) ────────────────────────────────────
    with dot.subgraph(name="cluster_hogar") as hogar:
        hogar.attr(style="dashed", color="#4A5568", penwidth="2", 
                   label="Límite del Hogar", fontcolor="#4A5568", fontsize="12", margin="20")
        for nid in nodes_info.keys():
            if not nid.startswith("ghost_"):  # No encerrar fantasmas
                hogar.node(nid)

    # ── 4. FORZAR NIVELES (rank=same) ─────────────────────────────────────────
    for lvl in range(1, 6):
        if levels[lvl]:
            with dot.subgraph() as s:
                s.attr(rank="same")
                for nid in levels[lvl]: 
                    s.node(nid)

    # ── 5. LÍNEA DE UNIÓN CONYUGAL Y POSICIONAMIENTO ESPACIAL ─────────────────
    union_id = None
    if jefe_id and pareja_id:
        union_id = "union_central"
        dot.node(union_id, label="", shape="point", width="0.08", height="0.08", style="filled", fillcolor=UNION_COLOR)

        tipo = str(tipo_union).lower()
        if "conviv" in tipo: edge_style, edge_label = "dashed", ""
        elif "separ" in tipo: edge_style, edge_label = "solid", "s."
        elif "divorc" in tipo: edge_style, edge_label = "solid", "d."
        else: edge_style, edge_label = "solid", "m." # Por defecto "m." para casados

        # Hombre izquierda, Mujer derecha
        sex_j = nodes_info[jefe_id]["sex"]
        sex_p = nodes_info[pareja_id]["sex"]
        left_node, right_node = jefe_id, pareja_id
        if sex_j == "F" and sex_p == "M":
            left_node, right_node = pareja_id, jefe_id
            
        with dot.subgraph() as s:
            s.attr(rank="same")
            s.edge(left_node, right_node, style="invis", weight="100")

        # Se inyecta la etiqueta en uno de los lados de la unión
        dot.edge(left_node, union_id, arrowhead="none", color=EDGE_UNION, penwidth="2", style=edge_style)
        dot.edge(right_node, union_id, arrowhead="none", color=EDGE_UNION, penwidth="2", style=edge_style,
                 label=f" {edge_label} ", fontsize="11", fontcolor=BORDER_DARK)
    elif jefe_id:
        # Check si es viudo para añadir fantasma viudo
        is_viudo = False
        for m in members:
            if "JEFE" in str(m.get("Parentesco", "")).upper() and "VIUD" in str(m.get("E. Civil", "")).upper():
                is_viudo = True
                break
        if is_viudo:
            ghost_id = "ghost_viudo"
            dot.node(ghost_id, label="X", shape="ellipse" if nodes_info[jefe_id]["sex"] == "M" else "box", 
                     style="dashed", color=EDGE_COLOR, fillcolor=FILL_DECEASED)
            union_id = "union_central"
            dot.node(union_id, label="", shape="point", width="0.08", height="0.08", style="filled", fillcolor=UNION_COLOR)
            
            left_n, right_n = jefe_id, ghost_id
            if nodes_info[jefe_id]["sex"] == "F":
                left_n, right_n = ghost_id, jefe_id
                
            with dot.subgraph() as s:
                s.attr(rank="same")
                s.edge(left_n, right_n, style="invis", weight="100")
            dot.edge(left_n, union_id, arrowhead="none", color=EDGE_UNION, penwidth="2", style="solid")
            dot.edge(right_n, union_id, arrowhead="none", color=EDGE_UNION, penwidth="2", style="solid")
        else:
            union_id = jefe_id

    # ── 6. HIJOS Y GEMELOS (Nivel 4) ──────────────────────────────────────────
    target_for_hijos = union_id or jefe_id
    hijos_propios_ids = [n for n in levels[4] if "SOBRIN" not in nodes_info[n]["parentesco"]]
    sobrinos_ids = [n for n in levels[4] if "SOBRIN" in nodes_info[n]["parentesco"]]
    
    if target_for_hijos and hijos_propios_ids:
        # Ordenar por edad/nacimiento mayor a menor (izquierda a derecha)
        hijos_propios_ids.sort(key=lambda nid: nodes_info[nid].get("edad", -1), reverse=True)
        
        # Enlazar ordenadamente con invisibles para forzar Izquierda->Derecha
        with dot.subgraph() as s:
            s.attr(rank="same")
            for i in range(len(hijos_propios_ids)-1):
                s.edge(hijos_propios_ids[i], hijos_propios_ids[i+1], style="invis", weight="100")

        i = 0
        while i < len(hijos_propios_ids):
            nid1 = hijos_propios_ids[i]
            p1 = nodes_info[nid1]["parentesco"]
            y_nac1 = nodes_info[nid1]["y_nac"]
            
            # Detectar Gemelos (mismo año de nacimiento o palabra "GEMELO")
            is_twin = False
            if i + 1 < len(hijos_propios_ids):
                nid2 = hijos_propios_ids[i+1]
                y_nac2 = nodes_info[nid2]["y_nac"]
                p2 = nodes_info[nid2]["parentesco"]
                
                # Considerar gemelos si dice explícitamente o comparten año de nacimiento válido
                if "GEMELO" in p1 or "GEMELA" in p1 or (y_nac1 > 0 and y_nac1 == y_nac2):
                    is_twin = True
                    
                    mid_id = f"twin_mid_{i}"
                    dot.node(mid_id, label="", shape="point", width="0.01")
                    dot.edge(target_for_hijos, mid_id, arrowhead="none", color=EDGE_COLOR, penwidth="1.5")
                    
                    dot.edge(mid_id, nid1, arrowhead="none", color=EDGE_COLOR, penwidth="1.5")
                    dot.edge(mid_id, nid2, arrowhead="none", color=EDGE_COLOR, penwidth="1.5")
                    
                    if "IDÉNTICO" in p1 or "IDENTICO" in p1:
                        dot.edge(nid1, nid2, arrowhead="none", color=EDGE_COLOR, penwidth="1.5", constraint="false")
                    
                    i += 2
                    continue
                    
            if not is_twin:
                estilo = "solid"
                if "ADOP" in p1: estilo = "dashed"
                elif "ACOGIDA" in p1 or "FOSTER" in p1: estilo = "dotted"
                
                dot.edge(target_for_hijos, nid1, arrowhead="none", color=EDGE_COLOR, penwidth="1.5", style=estilo)
                i += 1

    # ── 7. FILIACIÓN ESTRICTA DE SOBRINOS ─────────────────────────────────────
    if sobrinos_ids and colaterales_ids:
        # Colgar sobrinos del primer hermano disponible, NO del Jefe
        target_hermano = colaterales_ids[0]
        
        # Ordenar sobrinos de mayor a menor
        sobrinos_ids.sort(key=lambda nid: nodes_info[nid].get("edad", -1), reverse=True)
        with dot.subgraph() as s:
            s.attr(rank="same")
            for i in range(len(sobrinos_ids)-1):
                s.edge(sobrinos_ids[i], sobrinos_ids[i+1], style="invis", weight="100")
                
        for s_id in sobrinos_ids:
            dot.edge(target_hermano, s_id, arrowhead="none", color=EDGE_COLOR, penwidth="1.5", style="solid")

    # ── 8. ASCENDENCIA Y PADRES A HIJOS ───────────────────────────────────────
    abuelos_ids = levels[1]
    padres_ids  = levels[2]
    
    if padres_ids:
        union_padres = "union_padres_top"
        dot.node(union_padres, label="", shape="point", width="0.05")
        
        # Posicionar Padre izq, Madre der si se sabe sexo
        left_p, right_p = padres_ids[0], padres_ids[-1]
        for p in padres_ids:
            if nodes_info.get(p, {}).get("sex") == "M": left_p = p
            elif nodes_info.get(p, {}).get("sex") == "F": right_p = p
            
        if left_p != right_p:
            with dot.subgraph() as s:
                s.attr(rank="same")
                s.edge(left_p, right_p, style="invis", weight="100")
            
        for p in padres_ids:
            dot.edge(p, union_padres, arrowhead="none", color=EDGE_COLOR, penwidth="1.5", style="solid" if "ghost" not in p else "dashed")
            
        # Conectar a hijos (Jefe y hermanos)
        if jefe_id:
            dot.edge(union_padres, jefe_id, arrowhead="none", color=EDGE_COLOR, penwidth="1.5")
        for c in colaterales_ids:
            dot.edge(union_padres, c, arrowhead="none", color=EDGE_COLOR, penwidth="1.5")
            
        # Abuelos a padres
        if abuelos_ids:
            for a in abuelos_ids:
                dot.edge(a, union_padres, arrowhead="none", color=EDGE_COLOR, penwidth="1.5")
    else:
        # Si no hay padres ni fantasmas, conectar abuelos al jefe
        if abuelos_ids and jefe_id:
            for a in abuelos_ids:
                dot.edge(a, jefe_id, arrowhead="none", color=EDGE_COLOR, penwidth="1.5")

    # ── 9. NIETOS (nivel 5) ───────────────────────────────────────────────────
    if levels[5] and hijos_propios_ids:
        fallback_nietos = hijos_propios_ids[0]
        for nid in levels[5]:
            dot.edge(fallback_nietos, nid, arrowhead="none", color=EDGE_COLOR, penwidth="1.5")

    # ── 10. RELACIONES INTERPERSONALES ─────────────────────────────────────────
    if interpersonal_relations:
        for rel in interpersonal_relations:
            f, t, rtype = rel.get('from'), rel.get('to'), str(rel.get('type', '')).lower()
            attrs = {"arrowhead": "none", "penwidth": "2", "color": EDGE_COLOR}
            
            if "fusionada" in rtype and "conflictiva" in rtype:
                attrs.update({"penwidth": "6", "color": "#C53030", "label": " ⚡⚡⚡ ", "fontcolor": "white", "fontsize": "10"})
            elif "conflictiva" in rtype:
                attrs.update({"color": "#C53030", "penwidth": "3", "label": " ⚡ ", "fontcolor": "#C53030"})
            elif "estrecha" in rtype or "fusionada" in rtype:
                attrs.update({"penwidth": "6", "color": "#2F855A"})
            elif "cercana" in rtype:
                attrs.update({"penwidth": "4", "color": "#2F855A"})
            elif "armoniosa" in rtype or "normal" in rtype:
                attrs.update({"penwidth": "2", "color": "#2D3748", "style": "solid"})
            elif "quiebre" in rtype or "ruptura" in rtype:
                attrs.update({"style": "solid", "label": " // ", "fontcolor": "#C53030", "penwidth": "2"})
            elif "distante" in rtype:
                attrs.update({"style": "dotted", "penwidth": "2", "color": "#718096"})
                
            if f in nodes_info and t in nodes_info:
                dot.edge(f, t, constraint="false", **attrs)

    # ── 11. LEYENDA ────────────────────────────────────────────────────────────
    with dot.subgraph(name="cluster_legend") as leg:
        leg.attr(label="Leyenda Clínica (Norma Técnica)", style="dashed", color="#A0AEC0", fontsize="10", fontcolor="#4A5568", bgcolor="#F7FAFC")
        leg.attr("node", shape="plaintext", style="", fontsize="9", fontcolor="#4A5568", color="white", penwidth="0")
        leg.node("leg_text", label='''<<TABLE BORDER="0" CELLBORDER="0" CELLSPACING="2">
<TR><TD>□</TD><TD> Hombre</TD><TD>○</TD><TD> Mujer</TD><TD>□□</TD><TD> P. índice</TD></TR>
<TR><TD>✝</TD><TD colspan="2"> Fallecido/a</TD><TD>┄</TD><TD colspan="2"> Adoptivo / Acogida</TD></TR>
<TR><TD>△</TD><TD> Gestación</TD><TD>● / X</TD><TD> Aborto</TD><TD>○</TD><TD> Enf. Crónica</TD></TR>
<TR><TD>—</TD><TD> Casados</TD><TD>···</TD><TD> Convivencia</TD><TD>—/—</TD><TD> Sep/Div</TD></TR>
<TR><TD>≡</TD><TD> Fusionada</TD><TD>⚡</TD><TD> Conflictiva</TD><TD>//</TD><TD> Quiebre</TD></TR>
</TABLE>>''')

    return dot
