# 🏥 Manual Metodológico y Guía Técnica - Plataforma MAIS

Este documento detalla exhaustivamente la metodología clínica, los cálculos algorítmicos, la nomenclatura, la simbología y la arquitectura técnica que conforman la **Plataforma de Evaluación de Riesgo Familiar MAIS (Modelo de Atención Integral de Salud)**.

---

## 1. Introducción al Sistema
La plataforma MAIS es una aplicación centralizada diseñada para digitalizar, evaluar y monitorear el riesgo biopsicosocial de las familias bajo control en Atención Primaria de Salud (APS). Integra herramientas psicométricas validadas (Cartolas de Riesgo, APGAR Familiar) e instrumentos de análisis sistémico (Genograma, Ecomapa) para apoyar la toma de decisiones clínicas y generar automáticamente los reportes obligatorios (REM-P7).

---

## 2. Metodología Clínica y Cálculos

El núcleo evaluativo del sistema se basa en dos instrumentos metodológicos principales:

### 2.1 Pauta de Evaluación de Riesgo Biopsicosocial
El sistema clasifica las condiciones de la familia a través de 5 Tablas separadas por gravedad. El cálculo se efectúa sumando factores y aplicando reglas de salto directo ("red flags").

*   **Tabla 1: Riesgo Máximo (No otorgan puntos, clasifican directo a ALTO)**
    *   *Ejemplos:* VIF, consumo de drogas, abuso sexual, vulnerabilidad extrema, trabajo infantil.
    *   *Regla:* Basta la presencia de **1** factor en esta tabla para que el Nivel sea irremediablemente **ALTO**.
*   **Tabla 2: Riesgo Alto (No otorgan puntos)**
    *   *Ejemplos:* Enfermedad grave, paciente con alto riesgo de hospitalizar, conflictos severos.
    *   *Regla:* La presencia de **2 o más** factores determina riesgo **ALTO**. Si solo hay **1**, el riesgo salta a **MEDIO** (a menos que el puntaje total lo eleve a ALTO).
*   **Tabla 3: Riesgo Medio (4 puntos por cada check)**
    *   *Ejemplos:* Patología crónica, cesantía, hacinamiento, analfabetismo.
*   **Tabla 4: Riesgo Bajo (3 puntos por cada check)**
    *   *Ejemplos:* Hogar monoparental, riesgo cardiovascular, endeudamiento elevado.
*   **Tabla 5: Factores Protectores**
    *   *Regla:* Identifican fortalezas (redes de apoyo, lactancia, resiliencia) para el diseño del plan de intervención. No restan ni suman puntos metodológicamente, son de uso en cualitativo.

**Fórmula de Clasificación de Riesgo:**
1. **ALTO:** `Condición en T1 (>=1)` *Ó* `Condiciones en T2 (>=2)` *Ó* `Puntaje Total (T3+T4) >= 26 pts.`
2. **MEDIO:** Ninguna de las anteriores, pero: `Puntaje Total entre 17 y 25 pts.` *Ó* `Condición en T2 == 1`.
3. **BAJO:** `Puntaje Total <= 16 pts.` sin presencia de banderas rojas en T1 o T2.

### 2.2 Test APGAR Familiar (Smilkstein)
Instrumento subjetivo que evalúa mediante 5 preguntas cómo el caso índice percibe el funcionamiento de su entorno.
Cada pregunta otorga de 0 a 2 puntos (0=Casi nunca, 1=A veces, 2=Casi siempre):
*   **A**daptación, **P**articipación, **G**radiente de Crecimiento, **A**fecto, **R**esolución.
*   **Interpretación:**
    *   **7 a 10 puntos:** Familia Funcional.
    *   **4 a 6 puntos:** Disfunción Leve.
    *   **0 a 3 puntos:** Disfunción Severa.

---

## 3. Diccionario de Datos y Nomenclatura del Grupo Familiar

El editor de Grupo Familiar captura las métricas exactas requeridas para dar formato al sistema demográfico. Se ha implementado un sistema inclusivo y clínicamente estandarizado.

### 3.1 Identidad de Género (Módulo Inclusivo)
La aplicación abolió la etiqueta limitante de "Sexo" por `"Identidad de género"`, admitiendo las siguientes variantes:
*   `Masculino`: Mapea como hombre biológico o trans-masculino con representación clínica tradicional.
*   `Femenino`: Mapea como mujer biológica o trans-femenina con representación clínica tradicional.
*   `No binario` / `Transgénero` / `Prefiero no decir`: Identidades diversas e inespecíficas.
*   `Gestación/Aborto`: Bandera sistémica exclusiva para mapeos reproductivos perinatales no nacidos.

### 3.2 Simbología Arquitectónica del Genograma
Construido automáticamente mediante el motor Graphviz basado en las convenciones internacionales, dictadas por sus campos de Género, Enfermedad y Estado Civil.

*   **Identidades:**
    *   `[ ]` **Cuadrado**: Hombre / Masculino.
    *   `( )` **Círculo**: Mujer / Femenino.
    *   `◇` **Rombo / Diamante**: No binario, Transgénero o Sin Especificar (Inclusivo).
    *   `△` **Triángulo**: Gestación en curso.
*   **Indicadores de Estado:**
    *   **DOBLE Borde**: Paciente/Persona Caso Índice (Señalado activando el check *Resp*).
    *   **Borde ROJO**: Presencia de Enfermedad Crónica (detectando la palabra *Cronico=True*).
    *   **Sombra Interior GRIS/Oscura**: Fallecido (detectando `Fallecido/F` en *E. Civil*).
*   **Variantes Reproductivas:**
    *   Triángulo marcado con `X`: Aborto Espontáneo (E. Civil = Espontáneo).
    *   Triángulo relleno o marcado con `●`: Aborto Provocado (E. Civil = Provocado).
*   **Líneas de Vinculación y Conviviencia (Horizontal):**
    *   `===` Línea Continua de doble rail: Matrimonio.
    *   `---` Línea Simple continua: Pareja de hecho / Convivencia.
    *   `= / =` Línea con interrupciones cortadas: Separación o Divorcio.

### 3.3 Ecomapa (Lazos Sistémicos)
Analiza la conexión con nodos de la sociedad.
*   Línea **Fuerte y Continua (Gruesa)**: Vínculo Positivo o Recíproco.
*   Línea **Punteada**: Vínculo Débil o Inexistente.
*   Línea **Quebrada/Zigzag (Roja)**: Vínculo Estresante, Conflictivo o Roto.

---

## 4. Estructura y Flujo de la Plataforma

La aplicación posee un ciclo de vida diseñado para mantener integridades técnicas (backend en Google Sheets) garantizando fluidez en la herramienta Web (frontend en Streamlit).

*   **1. Generación del ID único:** Se autocompleta incrementalmente (`EVA-NNN-FAM-XXX`). Evita duplicidades al identificar el sector y los miembros.
*   **2. Tabla Dinámica del Grupo Familiar:** Serializa y empaqueta en formato JSON transparente a la Base de Datos para mantener en un solo registro matriz (fila) todo el detalle familiar en la hoja maestra.
*   **3. Firma y Compromiso Intervencional:** Captura los planes pactados bajo una firma explícita entre equipo de cabecera y familia.
*   **4. Motor Generador de PDFs (`pdf_gen.py`):** Agrupa todo en reportes listos para impresión.
    *   **Ficha Pauta Plena:** Recoge todo el JSON, extrae la lógica, escribe el resultado del riesgo y acomoda leyendas genéricas.
    *   **Pauta en Blanco:** Dibuja plantillas físicas para uso offline en zonas rurales (Postas), respetando nomenclaturas de los símbolos (Ej. ◇ Rombo) en sus pie de páginas.

---

## 5. Guía Técnica - Arquitectura de Código (Developers)

El proyecto está diseñado de forma modular.

### 5.1 Componentes Principales
1.  **`app.py`:** El script orquestador. Define la interfaz renderizada de Streamlit (`UI`), controles de acceso (`RBAC`), estado de los componentes (`st.session_state`) y persistencia.
2.  **`pdf_gen.py`:** Manipulador de documentos generados vía clase FPDF. Se encarga de mapear fuentes (ASCII Latin-1 para esquivar limitantes de caracteres natos), tablas y la exportación de bitstreams a la UI.
3.  **`genogram.py`:** Analiza relaciones padre-hijo generacionales (3 niveles de profundidad sugeridos) y los traduce al lenguaje `.dot` utilizado por Graphviz para diagramación en tiempo real de nodos y vértices.
4.  **`ecomap.py`:** Construye un gráfico similar basado en flujos de energía radial (`neato` engine) desde el epicentro familiar.
5.  **`analytics.py` & `seed_postas_data.py`:** Módulos en cargados de Data Science. Analytics envuelve las importaciones desde Google Sheets inyectando memoria caché (Dataframes Pandas) y Seed genera datos controlados para pruebas.

### 5.2 Roles y Seguridad (RBAC)
Dependiendo del token del perfil guardado en Google Sheets ("usuarios"), la plataforma limita vistas:
*   **Supervisores / Programador:** Acceso total y libre alucinación cruzada sectorial. Pueden resetear migraciones.
*   **Jefaturas y Equipo Sol/Luna:** Limitados restrictamente a la importación y visualización del Sector asignado para prevención de fugas PHI (Personal Health Information).
*   **Encargado/a Postas:** Acceso garantizado de visualización al mundo primario rural (Luna).
*   **Seguridad Mutex de Caché:**  La lectura de Google Sheets está protegida con un timelock por sesión de **5 minutos** en dashboard (`raw_analytics_df` en `analytics.py`), el cual es invalidado artificialmente en caliente por `app.py` dentro de la función `save_evaluacion()` para reaccionar asíncronamente a los inputs.

---
*Documento generado con la asistencia tecnológica del ecosistema Antigravity.*
