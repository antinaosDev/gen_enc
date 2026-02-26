"""
genogram.py — Generador de Genograma clínico (Graphviz).
Implementado según la guía oficial:
  "Procedimiento de Construcción de Genogramas" — Gobierno de Chile.

SIMBOLOGÍA (páginas 2-7 de la guía):
  Hombre       → cuadrado (box)
  Mujer        → círculo  (ellipse)
  Fallecido/a  → figura con X encima
  Persona índice (Resp=True) → doble borde
  Casados       → línea sólida horizontal entre ambos
  Convivientes  → línea de puntos horizontal
  Separados     → línea sólida con 1 barra diagonal ( / )
  Divorciados   → línea sólida con 2 barras ( // )
  Hijos        → cuelgan del nodo de unión, de izquierda a derecha (mayor→menor)
  Generaciones → {Abuelos=rank 1, Padres=rank 2, Central=rank 3, Hijos=rank 4, Nietos=rank 5}
  Hogar compartido → línea punteada envolvente (simulada con cluster)

RELACIONES INTERPERSONALES (páginas 7):
  Muy estrecha           → 3 líneas paralelas
  Cercana                → 2 líneas paralelas
  Conflictiva            → línea zigzag
  Muy estrecha/conflictiva → 3 líneas + zigzag
  Quiebre               → línea con barra
  Distante              → línea punteada
"""
import graphviz

# ─── Paleta Clínica Oficial ───────────────────────────────────────────────────
BORDER_DARK    = "#1A365D"
FILL_MALE      = "#EBF4FF"   # azul muy claro
FILL_FEMALE    = "#FFF0F6"   # rosa muy claro
FILL_INDEX     = "#FFFBEB"   # amarillo suave para persona índice
FILL_DECEASED  = "#E2E8F0"   # gris claro para fallecidos
EDGE_COLOR     = "#2D3748"
EDGE_UNION     = "#1A365D"
UNION_COLOR    = "#1A365D"

# ─── Mapeo de Parentesco → Generación ─────────────────────────────────────────
def get_generation_level(parentesco: str) -> int:
    """
    Nivel generacional (1=Abuelos → 5=Nietos).
    Basado en la guía: "Se deben representar TRES generaciones."
    """
    p = str(parentesco).strip().upper()
    if any(x in p for x in ["ABUEL", "BISABUEL"]):
        return 1
    if any(x in p for x in ["PADRE", "MADRE", "SUEGR", "TÍO", "TIA", "TIO", "TUAT"]):
        return 2
    if any(x in p for x in ["JEFE", "CÓNYUGE", "CONYUGUE", "PAREJA", "CONVIV",
                              "HERMANO", "HERMANA", "HERMAN"]):
        return 3
    if any(x in p for x in ["HIJO", "HIJA", "NIÑO", "SOBRIN", "ADOP"]):
        return 4
    if any(x in p for x in ["NIETO", "NIETA", "BIZNIETO"]):
        return 5
    return 3  # Default → Generación central


def _detect_sex(sexo_raw: str) -> str:
    """Retorna 'M', 'F', 'G' o '?' según el campo Sexo."""
    s = str(sexo_raw).strip().upper()
    # Orden importante: "G" para gestación primero, luego "F", luego "M"
    if s in ("G", "GESTACION", "GESTACIÓN", "EMBARAZO"):
        return "G"
    if s in ("F", "FEM", "FEMENINO", "MUJER"):
        return "F"
    if s in ("M", "MAS", "MASCULINO", "HOMBRE", "H"):
        return "M"
    return "?"


def _build_node_label(nombre: str, edad: str, parentesco: str,
                      is_deceased: bool, is_index: bool) -> str:
    """Construye el label HTML del nodo con info clínica."""
    nombre_corto = nombre[:22]
    lines = [f"<B>{nombre_corto}</B>"]
    if edad:
        lines.append(f"{edad} años")
    lines.append(f'<FONT POINT-SIZE="8">{parentesco}</FONT>')
    if is_deceased:
        lines.append('<FONT POINT-SIZE="9" COLOR="#C53030">[✝ Fallecido/a]</FONT>')
    rows = "".join(f"<TR><TD>{ln}</TD></TR>" for ln in lines)
    return f'<<TABLE BORDER="0" CELLBORDER="0" CELLSPACING="1">{rows}</TABLE>>'


def generate_genogram_dot(members: list,
                           family_name: str = "",
                           nivel_riesgo: str = "",
                           tipo_union: str = "Casados",
                           interpersonal_relations: list = None):
    """
    Genera el Graphviz Digraph del genograma según la guía oficial.

    Args:
        members      : lista de dicts con {'Nombre y Apellidos','Sexo','Parentesco',
                        'F. Nac','Resp','Ocupación','E. Civil'}
        family_name  : nombre de la familia (título)
        nivel_riesgo : 'RIESGO ALTO', 'RIESGO MEDIO', 'RIESGO BAJO' (opcional)
        tipo_union   : 'Casados' | 'Convivencia' | 'Separados' | 'Divorciados'
    """
    from datetime import date

    dot = graphviz.Digraph(
        comment=f"Genograma {family_name}",
        graph_attr={
            "rankdir": "TB",
            "splines": "ortho",
            "nodesep": "0.9",
            "ranksep": "0.7",
            "newrank": "true",
            "bgcolor": "white",
            "fontname": "Arial",
            "label": f"Genograma Familiar — {family_name}",
            "labelloc": "t",
            "fontsize": "14",
        }
    )
    dot.attr("node", fontname="Arial", style="filled", penwidth="2",
             color=BORDER_DARK)

    # ── 1. CREAR NODOS INDIVIDUALES ────────────────────────────────────────────
    nodes_info: dict[str, dict] = {}
    levels: dict[int, list[str]] = {1: [], 2: [], 3: [], 4: [], 5: []}

    today_year = date.today().year

    for i, m in enumerate(members):
        nombre    = str(m.get("Nombre y Apellidos", f"Miembro {i+1}"))
        sexo_raw  = str(m.get("Sexo", "?"))
        is_index  = bool(m.get("Resp", False)) or str(m.get("Resp", "")).upper() == "TRUE"
        parentesco = str(m.get("Parentesco", "Familiar"))
        # Calcular edad desde F. Nac si no viene explícita
        edad_val  = str(m.get("Edad", ""))
        if not edad_val:
            fnac = str(m.get("F. Nac", ""))
            if fnac and len(fnac) >= 4:
                try:
                    y = int(fnac[:4])
                    edad_val = str(today_year - y)
                except ValueError:
                    edad_val = ""

        # Estado vital: si E. Civil contiene "Fallecido", "F" o campo explícito
        is_deceased = any(x in str(m.get("E. Civil", "")).upper() for x in ["FALLEC", "F"]) or \
                      "FALLEC" in str(m.get("Estado", "")).upper()

        sex   = _detect_sex(sexo_raw)
        nid   = f"m{i}"
        level = get_generation_level(parentesco)
        levels[level].append(nid)

        # ── Forma del nodo ──────────────────────────────────────────────────
        if sex == "M":
            shape     = "box"          # Hombre → cuadrado
            fillcolor = FILL_MALE
        elif sex == "F":
            shape     = "ellipse"      # Mujer  → círculo
            fillcolor = FILL_FEMALE
        elif sex == "G":
            shape     = "triangle"     # Gestación (Embarazo/Aborto)
            fillcolor = "white"
        else:
            shape     = "diamond"      # Sexo desconocido
            fillcolor = "white"

        if is_deceased:
            fillcolor = FILL_DECEASED

        # Enfermedad Crónica (Indicator: si existe campo 'Cronico' o 'Enfermedad' en el miembro)
        # Manejo robusto de Booleans y Strings "TRUE"/"1"
        raw_chronic = m.get("Cronico")
        if isinstance(raw_chronic, bool):
            is_chronic = raw_chronic
        else:
            is_chronic = str(raw_chronic).upper() in ("TRUE", "1", "SÍ", "SI", "X")
        
        # También buscar en campo 'Enfermedad' por si acaso
        if not is_chronic:
            is_chronic = str(m.get("Enfermedad", "")).upper() in ("TRUE", "1", "SÍ", "SI", "X")
        
        color = "#C53030" if is_chronic else BORDER_DARK # Rojo si es crónico
        penwidth = "4" if is_chronic else "2" # Un poco menos agresivo que "5" pero notable

        # Persona índice → doble borde (peripheries=2)
        peripheries = "2" if is_index else "1"

        label = _build_node_label(nombre, edad_val, parentesco,
                                   is_deceased, is_index)

        # Si fallecido, agrega una "X" visual mediante el label (Graphviz no
        # soporta X nativa, usamos el color rojo tachado en label + gris)
        # Simbolismo específico de Gestación/Aborto
        status = str(m.get("E. Civil", "")).upper()
        if sex == "G":
            if "ESPONT" in status:
                label = "X" # Aborto espontáneo
            elif "PROVOC" in status or "INDUC" in status:
                label = "●" # Aborto provocado (punto negro)
            else:
                label = ""  # Embarazo normal

        dot.node(nid,
                 label=label,
                 shape=shape,
                 fillcolor=fillcolor,
                 color=color,
                 penwidth=penwidth,
                 peripheries=peripheries)

        nodes_info[nid] = {
            "level": level,
            "parentesco": parentesco.upper(),
            "is_index": is_index,
            "sex": sex,
            "is_deceased": is_deceased,
        }

    # ── 2. FORZAR NIVELES (rank=same) ─────────────────────────────────────────
    for lvl in range(1, 6):
        ids_in_lvl = levels[lvl]
        if ids_in_lvl:
            with dot.subgraph() as s:
                s.attr(rank="same")
                for nid in ids_in_lvl:
                    s.node(nid)

    # ── 3. IDENTIFICAR PAREJA PRINCIPAL ───────────────────────────────────────
    jefe_ids   = [nid for nid, info in nodes_info.items()
                  if "JEFE" in info["parentesco"]]
    pareja_ids = [nid for nid, info in nodes_info.items()
                  if any(x in info["parentesco"]
                         for x in ["CÓNYUGE", "CONYUGUE", "PAREJA", "CONVIV"])]

    jefe_id   = jefe_ids[0]   if jefe_ids   else None
    pareja_id = pareja_ids[0] if pareja_ids else None

    # ── 4. LÍNEA DE UNIÓN CONYUGAL ─────────────────────────────────────────────
    # La guía indica:
    #   Casados    → línea sólida
    #   Convivencia → línea de puntos
    #   Separados  → línea sólida + 1 "/"
    #   Divorciados→ línea sólida + "//"
    union_id = None
    if jefe_id and pareja_id:
        union_id = "union_central"
        dot.node(union_id, label="", shape="point", width="0.08",
                 height="0.08", style="filled", fillcolor=UNION_COLOR)

        # Estilo de la línea según tipo de unión
        tipo = str(tipo_union).lower()
        if "conviv" in tipo:
            edge_style = "dashed"
            edge_label = ""
        elif "separ" in tipo:
            edge_style = "solid"
            edge_label = "/"
        elif "divorc" in tipo:
            edge_style = "solid"
            edge_label = "//"
        else:  # casados (default)
            edge_style = "solid"
            edge_label = ""

        dot.edge(jefe_id,   union_id, arrowhead="none",
                 color=EDGE_UNION, penwidth="2", style=edge_style)
        dot.edge(pareja_id, union_id, arrowhead="none",
                 color=EDGE_UNION, penwidth="2", style=edge_style,
                 label=edge_label, fontsize="12", fontcolor="#C53030")

    elif jefe_id:
        # Monoparental: el jefe es el punto de descendencia
        union_id = jefe_id

    # ── 5. HIJOS (nivel 4) ────────────────────────────────────────────────────
    # Guía: "Los hijos se sitúan de izquierda a derecha desde el mayor al más joven."
    # → el orden en la lista se respeta (por eso usamos la lista original)
    target_for_hijos = union_id or jefe_id
    if target_for_hijos:
        hijo_nids = levels[4]
        
        # Agrupar gemelos por proximidad en la lista (generalmente vienen juntos)
        # o simplemente detectar si son del mismo tipo correlativos
        i = 0
        while i < len(hijo_nids):
            nid1 = hijo_nids[i]
            p1 = nodes_info[nid1]["parentesco"]
            
            # ¿Es gemelo?
            if "GEMELO" in p1:
                # Buscar si el siguiente también es gemelo del mismo tipo
                if i + 1 < len(hijo_nids):
                    nid2 = hijo_nids[i+1]
                    p2 = nodes_info[nid2]["parentesco"]
                    
                    if "GEMELO" in p2:
                        # Crear un punto intermedio para la divergencia
                        mid_id = f"twin_mid_{i}"
                        dot.node(mid_id, label="", shape="point", width="0.01")
                        
                        # Línea desde el tronco al punto de divergencia
                        dot.edge(target_for_hijos, mid_id, arrowhead="none", color=EDGE_COLOR, penwidth="1.5")
                        
                        # Líneas divergentes a los gemelos
                        dot.edge(mid_id, nid1, arrowhead="none", color=EDGE_COLOR, penwidth="1.5")
                        dot.edge(mid_id, nid2, arrowhead="none", color=EDGE_COLOR, penwidth="1.5")
                        
                        # Si son idénticos, conectar las bases
                        if "IDÉNTICO" in p1 or "IDENTICO" in p1:
                            dot.edge(nid1, nid2, arrowhead="none", color=EDGE_COLOR, penwidth="1", constraint="false")
                        
                        i += 2 # Saltar ambos
                        continue
            
            # Hijo estándar
            relacion = nodes_info[nid1]["parentesco"]
            estilo = "dashed" if "ADOP" in relacion else "solid"
            dot.edge(target_for_hijos, nid1,
                     arrowhead="none", color=EDGE_COLOR,
                     penwidth="1.5", style=estilo)
            i += 1

    # ── 6. NIETOS (nivel 5) ───────────────────────────────────────────────────
    hijos_ids_list = levels[4]
    fallback_nietos = hijos_ids_list[0] if hijos_ids_list else target_for_hijos
    if fallback_nietos:
        for nid in levels[5]:
            dot.edge(fallback_nietos, nid,
                     arrowhead="none", color=EDGE_COLOR, penwidth="1.5")

    # ── 7. ASCENDENCIA Y COLATERALES: Abuelos → Padres → Generación central ───
    abuelos_ids = levels[1]
    padres_ids  = levels[2]
    # Colaterales (hermanos, otros en nivel 3 que no son el tronco)
    colaterales_ids = [nid for nid in levels[3] if nid != jefe_id and nid != pareja_id]

    # Abuelos → apuntan a los padres o al jefe si no hay padres
    if abuelos_ids:
        target_abuelo = padres_ids[0] if padres_ids else jefe_id
        if target_abuelo:
            for a in abuelos_ids:
                dot.edge(a, target_abuelo, arrowhead="none", color=EDGE_COLOR,
                         penwidth="1.5", style="solid")

    # Padres → apuntan al Jefe y a los Hermanos
    if padres_ids and jefe_id:
        for p in padres_ids:
            # Padre al Jefe
            dot.edge(p, jefe_id, arrowhead="none", color=EDGE_COLOR,
                     penwidth="1.5", style="solid")
            # Padre a los Hermanos
            for c in colaterales_ids:
                dot.edge(p, c, arrowhead="none", color=EDGE_COLOR,
                         penwidth="1.5", style="solid")
    elif jefe_id and colaterales_ids:
        # Si NO hay padres registrados, conectamos a los hermanos al jefe con una línea temporal/horizontal
        for c in colaterales_ids:
            # constraint="false" evita que rompan el nivel horizontal
            dot.edge(jefe_id, c, arrowhead="none", color=EDGE_COLOR,
                     penwidth="1.5", style="dotted", constraint="false")

    # ── 8. CADENA DE NIVEL INVISIBLE (evita que Graphviz colapse los ranks) ───
    last_anchor = None
    for lvl in range(1, 6):
        if levels[lvl]:
            anchor = levels[lvl][0]
            if last_anchor and last_anchor != anchor:
                dot.edge(last_anchor, anchor, style="invis")
            last_anchor = anchor

    # ── 9. RELACIONES INTERPERSONALES ─────────────────────────────────────────
    # relaciones: lista de dicts [{'from': idx1, 'to': idx2, 'type': 'estrecha'|'conflictiva'|...}]
    # Si no viene como argumento, buscamos en los datos de los miembros si hay campos específicos
    if interpersonal_relations:
        for rel in interpersonal_relations:
            f = rel.get('from')
            t = rel.get('to')
            rtype = str(rel.get('type', '')).lower()
            
            # Mapeo de estilos según la guía
            attrs = {"arrowhead": "none", "penwidth": "2", "color": EDGE_COLOR}
            if ("estrecha" in rtype or "fusion" in rtype) and "conflict" in rtype:
                attrs["penwidth"] = "6" 
                attrs["color"] = "#C53030"
                attrs["label"] = " ⚡⚡⚡ " # Añadir rayos para denotar conflicto en línea gruesa
                attrs["fontcolor"] = "white"
                attrs["fontsize"] = "10"
            elif "estrecha" in rtype or "fusion" in rtype:
                attrs["penwidth"] = "6" # Muy estrecha / Fusionada (Triple línea conceptual)
                attrs["color"] = "#2F855A" 
            elif "conflict" in rtype:
                attrs["color"] = "#C53030" 
                attrs["penwidth"] = "3"
                attrs["label"] = " ⚡ "
                attrs["fontcolor"] = "#C53030"
            elif "cercan" in rtype:
                attrs["penwidth"] = "4" # Cercana (Doble línea conceptual)
                attrs["color"] = "#2F855A"
            elif "quiebre" in rtype:
                attrs["style"] = "solid"
                attrs["label"] = " || " # Quiebre con barras
                attrs["fontcolor"] = "#C53030"
                attrs["penwidth"] = "2"
            elif "distan" in rtype:
                attrs["style"] = "dotted" # Distante
                
            if f in nodes_info and t in nodes_info:
                # Usar constraint=false para no romper el layout generacional
                dot.edge(f, t, constraint="false", **attrs)

    # ── 10. LEYENDA ────────────────────────────────────────────────────────────
    with dot.subgraph(name="cluster_legend") as leg:
        leg.attr(label="Leyenda Clínica (Norma Técnica)", style="dashed", color="#A0AEC0",
                 fontsize="10", fontcolor="#4A5568", bgcolor="#F7FAFC")
        leg.attr("node", shape="plaintext", style="", fontsize="9",
                 fontcolor="#4A5568", color="white", penwidth="0")
        leg.node("leg_text", label="""<<TABLE BORDER="0" CELLBORDER="0" CELLSPACING="2">
<TR><TD>□</TD><TD> Hombre</TD>
    <TD>○</TD><TD> Mujer</TD>
    <TD>□□</TD><TD> Persona índice</TD></TR>
<TR><TD>✝</TD><TD colspan="2"> Fallecido/a</TD>
    <TD>┄</TD><TD colspan="2"> Hijo Adoptivo</TD></TR>
<TR><TD>△</TD><TD> Gestación</TD>
    <TD>▲</TD><TD> Aborto</TD>
    <TD>○ (Rojo)</TD><TD> Enf. Crónica</TD></TR>
<TR><TD>—</TD><TD> Casados</TD>
    <TD>···</TD><TD> Convivencia</TD>
    <TD>—/—</TD><TD> Sep/Divorc</TD></TR>
<TR><TD>≡</TD><TD> Fusionada</TD>
    <TD>⚡</TD><TD> Conflictiva</TD>
    <TD>||</TD><TD> Quiebre</TD></TR>
</TABLE>>""")

    return dot
