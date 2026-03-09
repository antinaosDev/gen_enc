# 🔧 MANUAL TÉCNICO
# Plataforma Integral de Salud Familiar MAIS
### Documentación de Arquitectura, Módulos de Código y Despliegue

> **Versión:** 3.0 | **Fecha:** Marzo 2026  
> **Audiencia:** Desarrolladores, Administradores de Sistemas, TI del CESFAM

---

## ÍNDICE

1. [Arquitectura General del Sistema](#1-arquitectura-general-del-sistema)
2. [Stack Tecnológico y Dependencias](#2-stack-tecnológico-y-dependencias)
3. [Estructura del Proyecto](#3-estructura-del-proyecto)
4. [Módulo Principal — app.py](#4-módulo-principal--apppy)
5. [Módulo de Visualización Familiar — genogram.py](#5-módulo-de-visualización-familiar--genogramapy)
6. [Módulo Ecomapa — ecomap.py](#6-módulo-ecomapa--ecomappy)
7. [Módulo de Generación PDF — pdf_gen.py](#7-módulo-de-generación-pdf--pdf_genpy)
8. [Módulo de Analítica — analytics.py](#8-módulo-de-analítica--analyticspy)
9. [Módulo de Semilla de Datos — seed_postas_data.py](#9-módulo-de-semilla-de-datos--seed_postas_datapy)
10. [Arquitectura de Base de Datos (Google Sheets)](#10-arquitectura-de-base-de-datos-google-sheets)
11. [Sistema RBAC — Control de Acceso](#11-sistema-rbac--control-de-acceso)
12. [Sistema de Caché y Rendimiento](#12-sistema-de-caché-y-rendimiento)
13. [Generación de IDs — Algoritmo Incremental](#13-generación-de-ids--algoritmo-incremental)
14. [Algoritmo de Clasificación de Riesgo](#14-algoritmo-de-clasificación-de-riesgo)
15. [Migración de Datos](#15-migración-de-datos)
16. [Despliegue y Configuración](#16-despliegue-y-configuración)
17. [Configuración de Secrets (Streamlit)](#17-configuración-de-secrets-streamlit)
18. [Log de Auditoría](#18-log-de-auditoría)
19. [Extensión y Mantenimiento](#19-extensión-y-mantenimiento)

---

## 1. Arquitectura General del Sistema

La plataforma MAIS sigue una arquitectura **cliente-servidor simplificada** basada en:

```
┌─────────────────────────────────────────────────────────────┐
│                   FRONTEND (Streamlit)                       │
│                      app.py (UI)                            │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  │
│  │genogram  │  │ ecomap   │  │ pdf_gen  │  │analytics │  │
│  │   .py    │  │   .py    │  │   .py    │  │   .py    │  │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘  │
└─────────────────────────┬───────────────────────────────────┘
                          │ gspread + oauth2client
                          ▼
┌─────────────────────────────────────────────────────────────┐
│              BACKEND — Google Sheets (BD)                   │
│  ┌─────────────┐  ┌──────────────────────┐  ┌──────────┐  │
│  │ Evaluaciones│  │ Planes de            │  │ usuarios │  │
│  │   (Hoja 1) │  │  Intervención (Hoja2)│  │ (Hoja)   │  │
│  └─────────────┘  └──────────────────────┘  └──────────┘  │
│  ┌─────────────┐  ┌──────────────────────┐               │
│  │  Ecomapas   │  │      Auditoría       │               │
│  └─────────────┘  └──────────────────────┘               │
└─────────────────────────────────────────────────────────────┘
```

**Flujo de datos principal:**
1. Usuario autenticado interactúa con la UI (Streamlit)
2. App.py lee/escribe directamente en Google Sheets vía `gspread`
3. Los módulos especializados (genogram, ecomap, pdf_gen) procesan datos bajo demanda
4. Analytics.py consume el mismo Google Sheet con caché de 5 minutos

---

## 2. Stack Tecnológico y Dependencias

### 2.1 Dependencias Python (`requirements.txt`)

| Paquete | Versión | Uso principal |
|---------|---------|---------------|
| `streamlit` | Latest | Framework UI web |
| `gspread` | Latest | Cliente Google Sheets API |
| `oauth2client` | Latest | Autenticación Google Service Account |
| `pandas` | Latest | Manipulación de DataFrames |
| `openpyxl` | Latest | Generación de archivos Excel (REM-P7) |
| `fpdf2` | Latest | Generación de PDFs |
| `plotly` | Latest | Gráficos interactivos del dashboard |
| `graphviz` | Latest | Motor de dibujo de genogramas |
| `toml` | Latest | Lectura de configuración |

### 2.2 Dependencias del Sistema

```
packages.txt:
  graphviz   ← Motor de renderizado de grafos (instalación del SO)
```

En Linux/Debian (Streamlit Cloud): el archivo `packages.txt` instala `graphviz` como paquete del sistema operativo mediante `apt-get`. En Windows local, debe instalarse manualmente y agregar al PATH.

### 2.3 Variables de Entorno y Secrets

La plataforma usa `st.secrets` de Streamlit para acceder a las credenciales de Google. Ver Sección 17.

---

## 3. Estructura del Proyecto

```
encuesta_riesgo/
│
├── app.py                    # Orquestador principal (2944 líneas)
├── analytics.py              # Dashboard estadístico (647 líneas)
├── genogram.py               # Motor de genogramas Graphviz (20KB)
├── ecomap.py                 # Motor de ecomapas (4KB)
├── pdf_gen.py                # Generador PDF con FPDF2 (40KB)
├── seed_postas_data.py       # Script de datos de prueba (15KB)
├── migrate_ids.py            # Utilidad de migración de IDs
├── requirements.txt          # Dependencias Python
├── packages.txt              # Dependencias del SO (graphviz)
│
├── .streamlit/
│   └── secrets.toml          # Credenciales GCP (NO subir a git)
│
├── MANUAL_MAIS.md            # Manual metodológico original
├── MANUAL_USUARIO.md         # Manual de usuario original
├── MANUAL_USUARIO_COMPLETO.md # Manual de usuario completo (v3.0)
├── MANUAL_PROCESOS.md        # Manual de procesos (v3.0)
├── MANUAL_TECNICO.md         # Este documento (v3.0)
│
└── presentacion/             # Aplicación React de presentación
```

---

## 4. Módulo Principal — app.py

**Tamaño:** ~2944 líneas | **Framework:** Streamlit

### 4.1 Constantes Globales

```python
SHEET_URL = "https://docs.google.com/spreadsheets/d/1JjYw2W6c-..."
```

Las constantes definen los datos maestros usados en toda la aplicación:

| Constante | Tipo | Descripción |
|-----------|------|-------------|
| `SHEET_URL` | str | URL del Google Sheets de producción |
| `PARENTESCO_OPTIONS` | list | Opciones de parentesco para el evaluador |
| `PARENTESCO_FAMILIA_OPTIONS` | list | Opciones de parentesco para el grupo familiar |
| `TIPO_UNION_OPTIONS` | list | Tipos de unión familiar |
| `PUEBLO_ORIGINARIO_OPTIONS` | list | Pueblos originarios (INE Chile, Censo 2017) |
| `PROGRAMA_OPTIONS` | list | Programas/cargos del CESFAM (>40 opciones) |
| `RISK_LABELS` | dict | Diccionario `{clave_riesgo: descripción_humana}` |

### 4.2 Claves de Riesgo (RISK_LABELS)

Las claves de riesgo siguen la nomenclatura `{tabla}_{nombre}`:

```python
# Tabla 1 (Riesgo Máximo – no puntúan):
't1_vif', 't1_drogas', 't1_alcohol', 't1_saludMentalDescomp',
't1_abusoSexual', 't1_riesgoBiopsicoGrave', 't1_epsaRiesgo',
't1_vulnerabilidadExtrema', 't1_trabajoInfantil'

# Tabla 2 (Riesgo Alto – no puntúan):
't2_enfermedadGrave', 't2_altoRiesgoHosp', 't2_discapacidad',
't2_saludMentalLeve', 't2_judicial', 't2_rolesParentales',
't2_sobrecargaCuidador', 't2_conflictosSeveros', 't2_adultosRiesgo'

# Tabla 3 (4 puntos cada una):
't3_patologiaCronica', 't3_discapacidadLeve', 't3_rezago',
't3_madreAdolescente', 't3_duelo', 't3_sinRedApoyo', 't3_cesantia',
't3_vulneNoExtrema', 't3_precariedadLaboral', 't3_hacinamiento',
't3_entornoInseguro', 't3_adultoSolo', 't3_desercionEscolar',
't3_analfabetismo', 't3_escolaridadIncompleta', 't3_dificultadAcceso'

# Tabla 4 (3 puntos cada una):
't4_monoparental', 't4_riesgoCardio', 't4_contaminacion',
't4_higiene', 't4_sinRecreacion', 't4_sinEspaciosSeguros',
't4_endeudamiento', 't4_serviciosIncompletos'

# Tabla 5 (Factores protectores – no puntúan):
't5_lactancia', 't5_habitos', 't5_redesSociales', 't5_redFamiliar',
't5_comunicacion', 't5_recursosSuficientes', 't5_resiliencia',
't5_viviendaAdecuada'
```

### 4.3 Funciones Principales de app.py

| Función | Propósito |
|---------|-----------|
| `get_google_sheet_client()` | Crea cliente gspread autenticado con service account |
| `load_users()` | Carga usuarios desde hoja "usuarios" de Sheets |
| `check_access(row_data, user_info)` | Verifica RBAC por sector/unidad |
| `can_download_rem(user_info)` | Verifica permiso de descarga REM-P7 |
| `generate_incremental_eval_id(apellido)` | Genera ID EVA-NNN-FAM-XXX |
| `generate_family_id()` | Genera FAM-AAAAMMDD-XXXX (legacy) |
| `search_record(id_eval)` | Busca evaluación por ID en Sheets |
| `load_record_into_state(record)` | Carga registro en `st.session_state` |
| `save_evaluacion_to_sheet(data, headers)` | Guarda/actualiza evaluación en Sheet |
| `save_intervention_rows(...)` | Guarda plan de intervención (Hoja 2) |
| `export_rem_p7_excel(...)` | Genera Excel REM-P7 con openpyxl |
| `get_all_ruts_mapping()` | Retorna dict {RUT: (familia, id_eval)} para validación |
| `log_audit_event(...)` | Registra evento en hoja "Auditoría" |
| `get_or_create_worksheet(...)` | Obtiene o crea hoja de Sheets |
| `migrate_eval_ids_to_new_format()` | Migra IDs al formato EVA-NNN-FAM-XXX |
| `generate_clinical_narrative(...)` | Genera informe clínico narrativo automático |

### 4.4 Estado de Sesión (st.session_state)

La aplicación usa extensivamente `st.session_state` para mantener los datos del formulario entre interacciones:

| Clave | Tipo | Descripción |
|-------|------|-------------|
| `authenticated` | bool | Si el usuario está autenticado |
| `user_info` | dict | Datos del usuario actual |
| `family_members` | DataFrame | Tabla del grupo familiar |
| `intervention_plan` | DataFrame | Tabla del plan de intervención |
| `seguimiento_plan` | DataFrame | Tabla de seguimiento del plan |
| `interpersonal_relations` | list | Relaciones interpersonales del genograma |
| `team_members` | DataFrame | Equipo de salud firmante |
| `apgar_total` | int | Puntaje total APGAR |
| `apgar_a1`…`apgar_a5` | int | Puntajes individuales APGAR |
| `fechaEvaluacion` | date | Fecha de evaluación |
| `fechaEgreso` | date | Fecha de egreso |
| `sector` | str | Sector (Sol/Luna) |
| `programa_unidad` | str | Programa/Unidad del evaluador |
| `evaluadorName` | str | Nombre del evaluador |
| `observaciones` | str | Observaciones libres |
| `t1_vif` … `t5_viviendaAdecuada` | bool | Estado de cada factor de riesgo |
| `egreso_alta` … `egreso_abandono` | bool | Tipo de egreso |
| `raw_analytics_df` | DataFrame | Caché de datos para analytics |
| `raw_df_ts` | datetime | Timestamp del caché de analytics |
| `filter_est_main` | str | Filtro global por establecimiento |

### 4.5 Flujo de Guardado de Evaluación (`save_evaluacion_to_sheet`)

```python
# 1. Conecta al Google Sheets client
client = get_google_sheet_client()

# 2. Obtiene o crea la hoja "Evaluaciones" con headers
worksheet = get_or_create_worksheet(spreadsheet, "Evaluaciones", headers)

# 3. Lee todos los valores actuales
all_values = worksheet.get_all_values()

# 4. Busca si el ID ya existe
for row in all_values[1:]:
    if row[id_col_idx] == new_id:
        row_to_update = i + 1  # fila de Google Sheets (1-indexed)
        break

# 5a. Si existe → actualiza la fila completa
worksheet.update(range_name=f"A{row_to_update}", values=[data])

# 5b. Si no existe → agrega nueva fila
worksheet.append_row(data)

# 6. Invalida el caché de analytics
if 'raw_analytics_df' in st.session_state:
    del st.session_state['raw_analytics_df']
```

### 4.6 Headers de la Hoja "Evaluaciones"

La hoja "Evaluaciones" contiene estas columnas (en orden):

```
ID Evaluación | Familia | Dirección | RUT | Fecha | Establecimiento |
Sector | Programa/Unidad | Evaluador | Parentesco | Tipo Unión |
Pueblo Originario | Nivel | Puntaje | APGAR Total | A1 | A2 | A3 | A4 | A5 |
t1_vif | t1_drogas | ... (todos los factores de riesgo T1-T5) |
Grupo Familiar JSON | Plan Intervención JSON | Relaciones JSON |
Equipo Salud JSON | Seguimiento Plan JSON |
Rep Sector | Familia Comp | Dir Comp | Rep Familia | RUT Rep | Fecha Comp |
Firma Funcionario | Firma Beneficiario | Firma Equipo | Firma Jefe |
Firma Evaluador | Observaciones | egreso_alta | egreso_traslado |
egreso_derivacion | egreso_abandono | Fecha Egreso
```

---

## 5. Módulo de Visualización Familiar — genogram.py

**Tamaño:** ~20KB | **Dependencia:** `graphviz` (Python + sistema)

### 5.1 Función Principal

```python
def generate_genogram_dot(members: list, relations: list) -> str:
    """
    Recibe la lista de miembros del grupo familiar y las relaciones interpersonales.
    Retorna el código DOT (lenguaje de Graphviz) como string.
    Se renderiza con graphviz.Source(dot_code).render() o graphviz.Source.wrap().
    """
```

### 5.2 Lógica de Representación

**Mapeo de Identidad de Género → Forma del nodo:**

| Valor `Identidad de género` | Forma Graphviz | Descripción Visual |
|------------------------------|----------------|-------------------|
| `Masculino` | `box` | Cuadrado |
| `Femenino` | `ellipse` | Círculo/Elipse |
| `No binario`, `Transgénero`, `Prefiero no decir` | `diamond` | Rombo |
| `Gestación/Aborto` | `triangle` | Triángulo |

**Modificadores visuales aplicados como atributos DOT:**

```dot
# Caso Índice → doble borde (peripheries=2)
node [peripheries=2]

# Patología crónica → borde rojo
node [color="red", penwidth=2]

# Fallecido (E. Civil = "F" o "Fallecido") → relleno gris
node [style="filled", fillcolor="gray50"]

# Aborto espontáneo (E. Civil = "Espontaneo") → triángulo con X label
node [label="×"]

# Aborto provocado (E. Civil = "Provocado") → triángulo relleno negro
node [style="filled", fillcolor="black"]
```

**Relaciones de pareja (aristas horizontales):**

| Tipo Unión | Estilo de arista DOT |
|------------|---------------------|
| `Casados` | `style=bold, dir=none` (doble línea) |
| `Convivencia` | `style=solid, dir=none` |
| `Separados`, `Divorciados` | `style=dashed, dir=none` |

**Relaciones padre-hijo (aristas verticales):**
- `dir=none, arrowhead=none` (sin punta de flecha)
- Ordenadas de mayor a menor (usando `rank=same` en el subgrafo)

### 5.3 Motor de Renderizado

El módulo usa el motor `dot` de Graphviz para disposición jerárquica (grafos de árbol). Genera un archivo PNG que se embebe en la UI con `st.image()`.

```python
import graphviz
src = graphviz.Source(dot_string)
png_data = src.pipe(format='png')
st.image(png_data)
```

---

## 6. Módulo Ecomapa — ecomap.py

**Tamaño:** ~4KB | **Dependencia:** `graphviz` (motor `neato`)

### 6.1 Función Principal

```python
def generate_ecomap_dot(family_name: str, ecomap_data: list) -> str:
    """
    Genera un gráfico radial con la familia en el centro
    y nodos institucionales alrededor.
    Usa el motor 'neato' de Graphviz para disposición circular forzada.
    """
```

### 6.2 Tipos de Aristas según Vínculo

```python
EDGE_STYLES = {
    "fuerte":    {"style": "bold",   "color": "black",  "penwidth": "2.5"},
    "debil":     {"style": "dashed", "color": "gray",   "penwidth": "1.0"},
    "estresante":{"style": "dotted", "color": "red",    "penwidth": "2.0"},
}
```

### 6.3 Motor Neato vs Dot

A diferencia del genograma (motor `dot`, jerárquico), el ecomapa usa el motor `neato` (spring model), que distribuye los nodos en disposición radial natural, ideal para representar sistemas concéntricos.

---

## 7. Módulo de Generación PDF — pdf_gen.py

**Tamaño:** ~40KB | **Dependencia:** `fpdf2`

### 7.1 Funciones Exportadas

```python
def generate_pdf_report(eval_data: dict, members: list, ...) -> bytes:
    """
    Genera el PDF completo con todos los datos de la evaluación.
    Retorna bytes del PDF para st.download_button().
    """

def generate_blank_pdf() -> bytes:
    """
    Genera el PDF de la pauta en blanco para terreno.
    Retorna bytes del PDF para st.download_button().
    """
```

### 7.2 Arquitectura del PDF — Ficha Completa

El PDF generado incluye las siguientes secciones en orden:

| Sección | Contenido |
|---------|-----------|
| **Portada / Encabezado** | Logo CESFAM + Título + ID Evaluación + Fecha |
| **Datos Básicos** | Familia, dirección, sector, programa, evaluador |
| **Grupo Familiar** | Tabla con todos los integrantes y sus datos |
| **Riesgo Biopsicosocial** | Factores chequeados por tabla + resultado total con color |
| **APGAR Familiar** | 5 preguntas con puntaje individual y total + interpretación |
| **Genograma** | Imagen PNG embebida (generada por genogram.py) |
| **Ecomapa** | Imagen PNG embebida (generada por ecomap.py) |
| **Plan de Intervención** | Tabla de actividades con objetivos, responsables y fechas |
| **Firmas y Compromiso** | Sección de firmas con nombres de los firmantes |
| **Análisis Clínico** | Narrativa auto-generada por `generate_clinical_narrative()` |

### 7.3 Manejo de Caracteres Especiales

FPDF2 trabaja nativamente en Latin-1. Para el soporte completo del español (tildes, ñ), el módulo:
1. Aplica `unicodedata.normalize('NFD', ...)` a los textos
2. Elimina diacríticos problemáticos cuando es necesario
3. Usa la fuente built-in `helvetica` que soporta Latin-1

### 7.4 Estructura del PDF en Blanco

El PDF en blanco incluye:
- Formulario con campos vacíos (sin datos de ninguna evaluación)
- Instrucciones de uso del formulario en terreno
- Espacio cuadriculado (grilla) para dibujar genograma y ecomapa a mano
- Leyenda completa de simbología del genograma (cuadrado=hombre, círculo=mujer, etc.)
- Tablas de factores de riesgo con checkboxes vacíos para marcar con lápiz
- Sección APGAR con espacio para puntajes
- Sección Plan de Intervención con filas en blanco

---

## 8. Módulo de Analítica — analytics.py

**Tamaño:** ~647 líneas | **Dependencias:** `streamlit`, `pandas`, `plotly`

### 8.1 Función Principal UI

```python
def render_analytics():
    """
    Punto de entrada para renderizar el dashboard completo.
    Llamado desde app.py cuando el usuario accede a la pestaña de analytics.
    """
```

### 8.2 Función de Carga de Datos

```python
def load_evaluaciones_df(est_filter=None) -> pd.DataFrame:
    """
    Carga el DataFrame con caché inteligente de 5 minutos.
    Aplica RBAC dinámicamente según el usuario en sesión.
    Aplica filtro de establecimiento si se especifica.
    """
```

**Flujo de la función:**
1. Verificar si existe `raw_analytics_df` en session_state y si tiene < 5 min
2. Si no hay caché válido → cargar desde Google Sheets
3. Guardar resultado en `raw_analytics_df` + timestamp `raw_df_ts`
4. Aplicar filtro RBAC (sector Sol/Luna según rol del usuario)
5. Aplicar filtro de establecimiento si viene `est_filter`
6. Retornar DataFrame filtrado

### 8.3 Gráficos del Dashboard

| Función | Tipo | Descripción |
|---------|------|-------------|
| `chart_risk_distribution(df)` | Donut (Pie) | Distribución por nivel de riesgo |
| `chart_risk_by_sector(df)` | Bar apilado | Riesgo por Sector Sol/Luna |
| `chart_risk_by_establishment(df)` | Bar H apilado | Riesgo por Posta/EMR |
| `chart_top_risk_factors(df, n=12)` | Bar H | Top N factores más frecuentes |
| `chart_intervention_gap(df)` | Bar apilado | Con plan vs sin plan por nivel |
| `chart_score_distribution(df)` | Histograma | Distribución de puntajes totales |
| `chart_evaluations_over_time(df)` | Línea | Evaluaciones por mes |
| `chart_by_program(df)` | Bar H | Puntaje promedio por programa |

### 8.4 Paleta de Colores Institucional

```python
AZUL_OSCURO = "#1F3864"   # Color corporativo CESFAM
AZUL_MED    = "#2E75B6"   # Azul medio
CELESTE     = "#BDD7EE"   # Celeste claro
AMARILLO    = "#FFD966"   # Riesgo Medio
ROJO        = "#C00000"   # Riesgo Alto
VERDE_OK    = "#375623"   # Riesgo Bajo
```

---

## 9. Módulo de Semilla de Datos — seed_postas_data.py

**Tamaño:** ~15KB | **Propósito:** Pruebas y desarrollo

Este script genera datos de prueba controlados para poblar el Google Sheets con 30 familias ficticias que cubran diversas combinaciones de:
- Niveles de riesgo (Alto/Medio/Bajo)
- Sectores (Sol/Luna)
- Establecimientos (CESFAM + distintas Postas)
- Factores de riesgo variados por tabla
- Composiciones familiares diversas

**Uso:**
```bash
python seed_postas_data.py
```

> ⚠️ **Solo para uso en ambiente de desarrollo o testing.** Nunca ejecutar en producción sin limpiar previamente los datos generados.

---

## 10. Arquitectura de Base de Datos (Google Sheets)

La base de datos es un Google Spreadsheet con las siguientes hojas:

### Hoja 1: "Evaluaciones"

**Función:** Registro maestro de todas las evaluaciones familiares.  
**Estructura:** Una fila por familia evaluada.  
**Clave primaria:** Columna `ID Evaluación` (formato `EVA-NNN-FAM-XXX`)

**Columnas clave:**

| Columna | Tipo | Descripción |
|---------|------|-------------|
| `ID Evaluación` | str | Clave primaria `EVA-NNN-FAM-XXX` |
| `Familia` | str | Apellido(s) de la familia |
| `Dirección` | str | Dirección del domicilio |
| `RUT` | str | RUT del responsable |
| `Fecha` | date str | Fecha evaluación (YYYY-MM-DD) |
| `Establecimiento` | str | CESFAM o nombre de la Posta |
| `Sector` | str | "Sol" o "Luna" |
| `Programa/Unidad` | str | Programa del evaluador |
| `Nivel` | str | "RIESGO ALTO", "RIESGO MEDIO", "RIESGO BAJO" |
| `Puntaje` | int | Puntaje total calculado (T3×4 + T4×3) |
| `APGAR Total` | int | Suma del APGAR (0-10) |
| `A1`…`A5` | int | Puntajes individuales APGAR |
| `t1_vif`…`t5_viviendaAdecuada` | bool str | Factores de riesgo ("True"/"False") |
| `Grupo Familiar JSON` | JSON str | Array de objetos con datos de cada integrante |
| `Plan Intervención JSON` | JSON str | Array de actividades del plan |
| `Relaciones JSON` | JSON str | Array de relaciones interpersonales |
| `Equipo Salud JSON` | JSON str | Array de miembros del equipo firmante |
| `Seguimiento Plan JSON` | JSON str | Array de actualizaciones de seguimiento |
| `egreso_alta`…`egreso_abandono` | bool str | Tipo de egreso |
| `Fecha Egreso` | date str | Fecha de egreso del programa |

**Estructura del Grupo Familiar JSON:**
```json
[
  {
    "Nombre y Apellidos": "Juan Pérez",
    "RUT": "12345678-9",
    "F. Nac": "1980-03-15",
    "Identidad de género": "Masculino",
    "Parentesco": "Jefe/a de Hogar",
    "E. Civil": "Casado",
    "Patología Crónica": false,
    "Resp": true
  }
]
```

**Estructura del Plan Intervención JSON:**
```json
[
  {
    "Objetivo": "Reducir consumo de alcohol",
    "Actividad": "Derivar a COSAM",
    "Fecha Prog": "2026-04-15",
    "Responsable": "A.S. García",
    "Fecha Real": null,
    "Evaluación": "",
    "Estado": "Pendiente",
    "F. Seguimiento": null,
    "Obs. Seguimiento": ""
  }
]
```

### Hoja 2: "Planes de Intervención"

**Función:** Registro desnormalizado de actividades del plan (una fila por actividad).  
**Propósito:** Facilita el cálculo del REM-P7 (familias con/sin plan) sin parsear JSON.

**Columnas:**
```
ID Evaluación | Familia | Fecha Evaluación | Nivel Riesgo |
Programa/Unidad | Parentesco | Objetivo | Actividad | Fecha Prog |
Responsable | Fecha Real | Evaluación | Estado | F. Seguimiento |
Obs. Seguimiento
```

**Nota:** Esta hoja se actualiza completamente al guardar (se eliminan las filas previas del mismo ID y se reinsertan), garantizando consistencia.

### Hoja 3: "Ecomapas"

**Función:** Registro de ecomapas (relaciones con sistemas externos) por ID de evaluación.

### Hoja 4: "usuarios"

**Función:** Directorio de usuarios autorizados para acceder al sistema.

**Columnas:**
```
usuario (RUT) | contraseña | nombre | cargo | rol | Programa/Unidad
```

**Roles posibles:**
- `programador`: Acceso global
- `encargado_mais`: Acceso global + REM-P7
- `jefe_sector`: Solo su sector + REM-P7
- `equipo_sector`: Solo su sector
- `usuario`: Solo su unidad

### Hoja 5: "Auditoría"

**Función:** Log inmutable de todas las acciones del sistema.

**Columnas:**
```
Timestamp | Usuario | Cargo | Acción | Detalles | ID Evaluación
```

---

## 11. Sistema RBAC — Control de Acceso

### 11.1 Función `check_access(row_data, user_info)`

```python
def check_access(row_data: dict, user_info: dict) -> bool:
    """
    Retorna True si el usuario puede ver el registro row_data.
    Lógica de prioridad:
    1. Rol programador/encargado_mais → siempre True
    2. Cargo contiene "sol" → solo sector Sol
    3. Cargo contiene "luna" o "postas" → solo sector Luna
    4. Programa/Unidad del usuario contenido en el registro → True
    5. Default → False
    """
    role = user_info.get('rol', '').lower()
    cargo = user_info.get('cargo', '').lower()
    
    # Superadmin
    if role in ['programador', 'encargado_mais'] or 'mais' in cargo:
        return True
    
    full_context = f"{user_info.get('Programa/Unidad', '')} {cargo}".lower()
    reg_sector = row_data.get('Sector', '').strip().lower()
    
    if re.search(r'\bsol\b', full_context):
        return reg_sector == 'sol'
    if re.search(r'\bluna\b', full_context) or 'postas' in full_context:
        return reg_sector == 'luna'
    
    # Filtro por programa/unidad
    user_unit = user_info.get('Programa/Unidad', '').lower()
    if user_unit and user_unit in row_data.get('Programa/Unidad', '').lower():
        return True
    
    return False
```

### 11.2 Función `can_download_rem(user_info)`

```python
def can_download_rem(user_info: dict) -> bool:
    role = user_info.get('rol', '').lower()
    cargo = user_info.get('cargo', '').lower()
    return role in ['programador', 'encargado_mais'] \
        or 'jefe' in cargo \
        or 'mais' in cargo \
        or 'encargado' in cargo
```

---

## 12. Sistema de Caché y Rendimiento

### 12.1 Caché de Google Sheets

Las llamadas a Google Sheets son costosas en tiempo (~1-3 segundos). Se implementa un sistema de caché en dos niveles:

**Nivel 1 — Caché de sesión `st.session_state`:**
```python
# En load_evaluaciones_df():
if 'raw_analytics_df' in st.session_state and 'raw_df_ts' in st.session_state:
    age_min = (datetime.now() - st.session_state['raw_df_ts']).seconds / 60
    if age_min < 5:  # TTL = 5 minutos
        return st.session_state['raw_analytics_df']
```

**Nivel 2 — Invalidación al guardar:**
```python
# En save_evaluacion_to_sheet():
if 'raw_analytics_df' in st.session_state:
    del st.session_state['raw_analytics_df']
# → La próxima consulta al dashboard forzará recarga desde Sheets
```

**Caché de validación de RUTs:**
```python
@st.cache_data(ttl=300)  # 5 minutos via decorator de Streamlit
def get_all_ruts_mapping():
    # Retorna dict {rut: (familia, id_eval)} para detectar duplicados
```

---

## 13. Generación de IDs — Algoritmo Incremental

```python
def generate_incremental_eval_id(familia_apellido: str) -> str:
    """
    Formato: EVA-{NNN}-FAM-{XXX}
    NNN: número correlativo con padding ceros a 3 dígitos
    XXX: primeras 3 letras del apellido (sin tildes, mayúsculas)
    
    Algoritmo:
    1. Conectar a Google Sheets
    2. Leer columna "ID Evaluación" de la hoja "Evaluaciones"
    3. Extraer todos los números NNN con regex: r'^EVA-(\d+)'
    4. Encontrar el máximo número usado
    5. Retornar max+1 con formato EVA-{max+1:03d}-FAM-{prefix}
    """
```

**Función `clean_prefix(apellido)`:**
```python
def clean_prefix(apellido: str) -> str:
    """Extrae 3 letras del apellido, eliminando tildes y caracteres especiales."""
    s = unicodedata.normalize('NFD', apellido.strip())
    s = ''.join(c for c in s if unicodedata.category(c) != 'Mn')  # quita tildes
    s = ''.join(c for c in s if c.isalpha())  # solo letras
    return s[:3].upper() if len(s) >= 3 else s.upper().ljust(3, 'X')
# Ejemplo: "Ñáñez" → normalize → "Nanez" → "NAN"
```

---

## 14. Algoritmo de Clasificación de Riesgo

El algoritmo es determinista y se ejecuta en tiempo real al marcar/desmarcar factores.

```python
def calcular_nivel_riesgo(active_risks: dict) -> tuple[str, int]:
    """
    Retorna: (nivel_str, puntaje_total)
    nivel_str: "RIESGO ALTO" | "RIESGO MEDIO" | "RIESGO BAJO"
    """
    # Contadores
    t1_count = sum(1 for k, v in active_risks.items() if k.startswith('t1_') and v)
    t2_count = sum(1 for k, v in active_risks.items() if k.startswith('t2_') and v)
    t3_count = sum(1 for k, v in active_risks.items() if k.startswith('t3_') and v)
    t4_count = sum(1 for k, v in active_risks.items() if k.startswith('t4_') and v)
    
    puntaje = (t3_count * 4) + (t4_count * 3)
    
    # Clasificación por prioridad
    if t1_count >= 1 or t2_count >= 2 or puntaje >= 26:
        return "RIESGO ALTO", puntaje
    elif t2_count == 1 or (17 <= puntaje <= 25):
        return "RIESGO MEDIO", puntaje
    else:
        return "RIESGO BAJO", puntaje
```

---

## 15. Migración de Datos

### 15.1 Función `migrate_eval_ids_to_new_format()`

Esta función fue introducida para migrar IDs en formato legado (UUID o FAM-AAAAMMDD-XXXX) al nuevo formato secuencial `EVA-NNN-FAM-XXX`.

**Proceso:**
1. Lee todos los registros de la hoja "Evaluaciones"
2. Genera un un mapa `{id_viejo: id_nuevo}` para todos los registros
3. Actualiza la columna ID en "Evaluaciones" fila por fila
4. Actualiza referencias en "Planes de Intervención"
5. Actualiza referencias en "Ecomapas"
6. Retorna `(True, mensaje, n_registros_actualizados)`

**Precaución:** Esta operación es destructiva sobre los IDs existentes. Debe ejecutarse solo una vez al migrar de sistema legacy.

---

## 16. Despliegue y Configuración

### 16.1 Despliegue en Streamlit Cloud (Producción)

1. Push del código a GitHub (repositorio privado)
2. Conectar el repositorio en [share.streamlit.io](https://share.streamlit.io)
3. Configurar los secrets de la aplicación (ver Sección 17)
4. Verificar que `packages.txt` (con `graphviz`) esté en la raíz del proyecto
5. El deployment es automático en cada push al branch principal

**Flujo de build en Streamlit Cloud:**
```
Instala requirements.txt (pip)
Instala packages.txt (apt-get, sistema operativo)
Ejecuta: streamlit run app.py --server.port=8501
```

### 16.2 Ejecución Local (Desarrollo)

```bash
# 1. Crear entorno virtual
python -m venv venv
.\venv\Scripts\activate    # Windows
source venv/bin/activate   # Linux/Mac

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Instalar graphviz en el sistema
# Windows: descargar instalador de https://graphviz.org/download/
# Agregar bin/ al PATH del sistema

# 4. Configurar secrets locales
mkdir .streamlit
# Crear .streamlit/secrets.toml (ver Sección 17)

# 5. Ejecutar
streamlit run app.py
```

---

## 17. Configuración de Secrets (Streamlit)

El archivo `.streamlit/secrets.toml` debe contener las credenciales de la cuenta de servicio de Google Cloud:

```toml
[gcp_service_account]
type = "service_account"
project_id = "tu-proyecto-gcp"
private_key_id = "abc123..."
private_key = "-----BEGIN RSA PRIVATE KEY-----\n...\n-----END RSA PRIVATE KEY-----\n"
client_email = "mais-service@tu-proyecto.iam.gserviceaccount.com"
client_id = "123456789"
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"
auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
client_x509_cert_url = "https://www.googleapis.com/robot/v1/metadata/x509/..."
universe_domain = "googleapis.com"
```

> 🔒 **Seguridad crítica:** Este archivo NUNCA debe subirse al repositorio Git. Verificar que `.gitignore` incluya `.streamlit/secrets.toml`.

### Permisos requeridos para la cuenta de servicio:
1. Compartir el Google Spreadsheet con el email `client_email` como **Editor**
2. Roles de IAM en GCP: `roles/drive.readonly` (mínimo) o `roles/drive.file`

### Scopes utilizados:
```python
scope = [
    'https://spreadsheets.google.com/feeds',
    'https://www.googleapis.com/auth/drive'
]
```

---

## 18. Log de Auditoría

### 18.1 Función `log_audit_event`

```python
def log_audit_event(
    user_info: dict,
    action: str,
    details: str = "",
    eval_id: str = None
) -> None:
    """
    Registra un evento en la hoja 'Auditoría' de Google Sheets.
    Fallo silencioso (no bloquea la UX si falla).
    """
```

**Acciones registradas:**
- `"GUARDAR_EVALUACION"` — Al guardar una ficha
- `"CARGAR_REGISTRO"` — Al abrir una evaluación
- `"GENERAR_PDF"` — Al descargar un PDF
- `"GENERAR_REM_P7"` — Al generar el reporte
- `"MIGRAR_IDS"` — Al ejecutar migración de IDs
- `"LOGIN"` — Al autenticarse

---

## 19. Extensión y Mantenimiento

### 19.1 Agregar un Nuevo Factor de Riesgo

1. Agregar la clave y descripción en `RISK_LABELS` (app.py)
2. Agregar la clave en `FACTOR_LABELS` (analytics.py)
3. Agregar el checkbox correspondiente en la UI del formulario
4. Agregar el campo como columna en la hoja "Evaluaciones" de Google Sheets
5. Actualizar el algoritmo de clasificación si el factor puntúa diferente
6. Actualizar la función `export_rem_p7_excel` si afecta al REM-P7

### 19.2 Agregar Nuevo Programa/Cargo

Agregar la opción a la lista `PROGRAMA_OPTIONS` en app.py (línea ~353). No requiere cambios en la base de datos.

### 19.3 Agregar Nuevo Usuario

Editar la hoja "usuarios" del Google Sheets directamente, agregando la fila con los campos requeridos. No requiere cambios en el código.

### 19.4 Agregar Nueva Posta/Establecimiento

El sistema detecta establecimientos dinámicamente desde los datos. Solo agregar la Posta como opción en el formulario de datos básicos y/o usar el nombre en los registros. El dashboard y el REM-P7 la detectarán automáticamente.

### 19.5 Punto de Entrada para Nuevos Módulos

Para agregar un nuevo módulo de visualización o análisis:

```python
# En app.py, patrón de carga lazy (para no bloquear inicio):
try:
    from nuevo_modulo import nueva_funcion
except ImportError:
    nueva_funcion = None

# Uso seguro en la UI:
if nueva_funcion:
    nueva_funcion(datos)
else:
    st.warning("Módulo no disponible.")
```

### 19.6 Actualización de Structure de Hoja en Sheets

Si se agregan nuevas columnas a la hoja "Evaluaciones":
1. Actualizar la lista `headers` en la función de guardado
2. Actualizar la función `load_record_into_state()` con el nuevo mapeo
3. Actualizar el PDF si debe mostrarse el nuevo campo
4. Ejecutar la migración de estructura si los registros existentes necesitan la nueva columna vacía

---

## Diagrama de Dependencias entre Módulos

```
app.py (Orquestador)
├── pdf_gen.py     (generate_pdf_report, generate_blank_pdf)
├── genogram.py    (generate_genogram_dot)
├── ecomap.py      (generate_ecomap_dot)
└── analytics.py   (render_analytics, load_evaluaciones_df)
         │
         ▼ (todos leen/escriben)
    Google Sheets API
    (gspread + oauth2client)
```

---

*Manual Técnico v3.0 — Plataforma MAIS — CESFAM Cholchol*  
*Generado con la asistencia tecnológica del ecosistema Antigravity*
