# ⚙️ MANUAL DE PROCESOS
# Plataforma Integral de Salud Familiar MAIS
### Procedimientos Operativos Estándar — Flujos de Trabajo Clínico-Administrativos

> **Versión:** 3.0 | **Fecha:** Marzo 2026  
> **Audiencia:** Coordinadores, Jefaturas de Sector, Encargados MAIS, Equipo Clínico

---

## ÍNDICE DE PROCESOS

1. [Marco Conceptual y Contexto Institucional](#1-marco-conceptual-y-contexto-institucional)
2. [Proceso 1 — Incorporación de Nueva Familia al Programa](#proceso-1--incorporación-de-nueva-familia-al-programa)
3. [Proceso 2 — Evaluación de Riesgo Biopsicosocial Familiar](#proceso-2--evaluación-de-riesgo-biopsicosocial-familiar)
4. [Proceso 3 — Aplicación del Test APGAR Familiar](#proceso-3--aplicación-del-test-apgar-familiar)
5. [Proceso 4 — Construcción del Genograma Familiar](#proceso-4--construcción-del-genograma-familiar)
6. [Proceso 5 — Construcción del Ecomapa Familiar](#proceso-5--construcción-del-ecomapa-familiar)
7. [Proceso 6 — Diseño del Plan de Intervención](#proceso-6--diseño-del-plan-de-intervención)
8. [Proceso 7 — Seguimiento y Gestión de Casos](#proceso-7--seguimiento-y-gestión-de-casos)
9. [Proceso 8 — Evaluaciones en Terreno (Postas Rurales)](#proceso-8--evaluaciones-en-terreno-postas-rurales)
10. [Proceso 9 — Egreso y Alta Familiar](#proceso-9--egreso-y-alta-familiar)
11. [Proceso 10 — Generación del Reporte Estadístico REM-P7](#proceso-10--generación-del-reporte-estadístico-rem-p7)
12. [Proceso 11 — Gestión de Usuarios y Accesos](#proceso-11--gestión-de-usuarios-y-accesos)
13. [Proceso 12 — Operación del Dashboard Analítico](#proceso-12--operación-del-dashboard-analítico)
14. [Diagrama de Flujo General del Sistema](#diagrama-de-flujo-general-del-sistema)
15. [Indicadores de Proceso y Gestión](#indicadores-de-proceso-y-gestión)
16. [Control de Versiones y Auditoría](#control-de-versiones-y-auditoría)

---

## 1. Marco Conceptual y Contexto Institucional

### 1.1 El Modelo de Atención Integral en Salud (MAIS)

El Modelo de Atención Integral en Salud (MAIS) es el marco conceptual que sustenta el trabajo de la Atención Primaria en Chile. Propone una visión biopsicosocial y familiar de la salud, donde la familia es entendida como la unidad básica de intervención. La **Plataforma MAIS** operacionaliza este modelo digitalmente.

### 1.2 Propósito del Sistema de Evaluación

El sistema de evaluación de riesgo familiar tiene como objetivo:
1. **Estratificar** a las familias según su nivel de vulnerabilidad biopsicosocial
2. **Priorizar** la intervención de los equipos de salud según la complejidad de cada familia
3. **Monitorear** la evolución del riesgo familiar en el tiempo
4. **Generar información estadística** para la toma de decisiones institucionales y el reporte al MINSAL (REM-P7)

### 1.3 Instrumentos Metodológicos del Sistema

| Instrumento | Tipo | Propósito |
|-------------|------|-----------|
| **Pauta de Evaluación de Riesgo** (5 Tablas) | Cuantitativo/Mixto | Clasificar nivel de riesgo familiar |
| **Test APGAR Familiar** (Smilkstein) | Cuantitativo subjetivo | Evaluar percepción del funcionamiento familiar |
| **Genograma** | Cualitativo gráfico | Mapear estructura y dinámica familiar |
| **Ecomapa** | Cualitativo gráfico | Mapear vínculos con sistemas externos |
| **Plan de Intervención** | Gestión | Formalizar compromisos de intervención |

### 1.4 Sectores Territoriales

| Sector | Denominación | Tipo de territorio | Establecimientos |
|--------|-------------|-------------------|-----------------|
| **Sol** | Sector Urbano | Urbano | CESFAM Cholchol |
| **Luna** | Sector Rural | Rural | Postas de salud rurales y EMR de la comuna |

---

## ⬛ PROCESO 1 — Incorporación de Nueva Familia al Programa

**Responsable:** Profesional clínico del equipo de cabecera  
**Disparador:** Detección de familia con factores de vulnerabilidad biopsicosocial  
**Resultado esperado:** Familia registrada en el sistema con ID único asignado

### Flujograma del Proceso 1

```
[INICIO]
    ↓
[Identificación de familia susceptible]
 └─ Por demanda espontánea, derivación interna o pesquisa activa
    ↓
[Verificar si la familia ya está en el sistema]
 ├─ SI → Cargar evaluación existente → [PROCESO 7: Seguimiento]
 └─ NO → Continuar
    ↓
[Hacer clic en "➕ Nueva Ficha"]
    ↓
[Sistema genera ID único: EVA-NNN-FAM-XXX]
    ↓
[Completar datos básicos de la familia]
 - Apellido(s) / Dirección / RUT
 - Sector (Sol/Luna) / Establecimiento
 - Programa/Unidad / Evaluador
    ↓
[Registrar composición del Grupo Familiar]
    ↓
[PROCESO 2: Evaluación de Riesgo]
```

### Pasos detallados del Proceso 1

**Paso 1.1 — Identificación de la familia**
- La familia puede ser identificada por:
  - Demanda espontánea en el CESFAM
  - Derivación desde otro programa de salud (PNAC, Salud Mental, Cardiovascular, etc.)
  - Pesquisa activa durante visitas domiciliarias
  - Derivación desde la red social (FOSIS, OPD, Municipio, etc.)
  - Detección en ChCC (Chile Crece Contigo) mediante pauta EPSA

**Paso 1.2 — Verificación de registro previo**
- Antes de crear una nueva ficha, busque si la familia ya tiene un registro:
  - Use la barra de búsqueda del catálogo (por apellido o dirección)
  - Si ya existe, abra ese registro (no cree uno nuevo)

**Paso 1.3 — Generación del ID único**
- Al presionar "Nueva Ficha", el sistema:
  1. Consulta en Google Sheets el número más alto de ID existente
  2. Genera el siguiente número correlativo (NNN)
  3. Extrae las 3 primeras letras del apellido familiar
  4. Construye el ID: `EVA-{NNN}-FAM-{XXX}`
  
**Paso 1.4 — Datos básicos**
Completar TODOS los campos marcados como obligatorios antes de continuar. El sector y establecimiento son críticos porque determinan la visibilidad del registro para otros funcionarios (RBAC).

**Paso 1.5 — Registro del grupo familiar**
Completar la tabla de Grupo Familiar con todos los miembros del núcleo conviviente, más los no convivientes que sean relevantes para el análisis sistémico.

---

## ⬛ PROCESO 2 — Evaluación de Riesgo Biopsicosocial Familiar

**Responsable:** Profesional clínico con competencias en salud familiar  
**Prerequisito:** Familia registrada con Grupo Familiar completo (Proceso 1)  
**Resultado esperado:** Nivel de riesgo calculado y registrado (Alto/Medio/Bajo)

### Flujograma del Proceso 2

```
[INICIO]
    ↓
[Revisión de los factores de las 5 Tablas]
    ↓
[¿Hay algún factor de Tabla 1 (T1)?]
 ├─ SI → Nivel = RIESGO ALTO (automático) → [FIN Clasificación]
 └─ NO → Continuar
    ↓
[¿Hay 2 o más factores de Tabla 2 (T2)?]
 ├─ SI → Nivel = RIESGO ALTO → [FIN Clasificación]
 └─ NO → Continuar
    ↓
[Calcular Puntaje Total: (N° T3 × 4) + (N° T4 × 3)]
    ↓
[¿Puntaje Total ≥ 26?]
 ├─ SI → Nivel = RIESGO ALTO → [FIN Clasificación]
 └─ NO → Continuar
    ↓
[¿Hay exactamente 1 factor de T2 OR Puntaje Total entre 17 y 25?]
 ├─ SI → Nivel = RIESGO MEDIO → [FIN Clasificación]
 └─ NO → Nivel = RIESGO BAJO → [FIN Clasificación]
    ↓
[Sistema actualiza indicador en tiempo real]
    ↓
[Guardar Evaluación]
```

### Tabla Resumen de Clasificación

| Condición | Nivel Resultante |
|-----------|-----------------|
| 1+ factor en T1 | 🔴 RIESGO ALTO |
| 2+ factores en T2 | 🔴 RIESGO ALTO |
| Puntaje T3+T4 ≥ 26 pts | 🔴 RIESGO ALTO |
| 1 factor en T2 O puntaje 17-25 pts | 🟡 RIESGO MEDIO |
| Puntaje ≤ 16 sin T1 ni 2+ T2 | 🟢 RIESGO BAJO |

### Criterios para marcar cada tabla

**Reglas para T1 (Riesgo Máximo):**

| Factor | Criterio de positividad |
|--------|------------------------|
| VIF | En investigación activa O con denuncia O con indicadores clínicos evidentes |
| Consumo drogas | AUDIT-C positivo O auto-reporte O antecedente documentado |
| Abuso sexual | Declaración directa O sospecha clínica fundamentada |
| Vulnerabilidad extrema | Sin ingresos verificables, indigencia, sinhogar |
| Trabajo infantil | Niño/a < 14 años con actividad laboral regular |

**Reglas para T3 (valoración de 4 puntos):**

| Factor | Criterio |
|--------|----------|
| Hacinamiento | Razón ≥ 2.5 personas por dormitorio |
| Adulto mayor solo | ≥ 60 años viviendo sin otro adulto en el domicilio |
| Cesantía | Proveedor principal sin empleo por más de 30 días corridos |
| Discapacidad leve | Puntuación Barthel entre 40-55 puntos |

### Documentación requerida posterior a la clasificación

Tras clasificar, el equipo debe:
1. **Documentar los factores detectados** con evidencia clínica en la sección "Observaciones"
2. **Activar protocolos específicos** si aplica (VIF, abuso, trabajo infantil)
3. **Continuar con APGAR** → **Genograma** → **Plan de Intervención**

---

## ⬛ PROCESO 3 — Aplicación del Test APGAR Familiar

**Responsable:** Profesional clínico (aplicación directa con el caso índice)  
**Prerequisito:** Caso índice identificado en el Grupo Familiar (campo "Resp" marcado)  
**Resultado esperado:** APGAR Total registrado con interpretación

### Protocolo de Aplicación

**Condiciones recomendadas:**
- Ambiente de privacidad garantizada
- Sin presencia de otros familiares durante la aplicación
- Explicar que no hay respuestas correctas o incorrectas
- Las 5 preguntas son sobre la PERCEPCIÓN del consultante (no la realidad objetiva)

**Proceso de aplicación pregunta por pregunta:**

| Paso | Acción |
|------|--------|
| 1 | Lea la pregunta claramente y despacio |
| 2 | Espere la respuesta espontánea del consultante |
| 3 | Si hay duda, repita la pregunta sin sugerir la respuesta |
| 4 | Asigne: 0 (Casi nunca) / 1 (A veces) / 2 (Casi siempre) |
| 5 | Anote el puntaje en la plataforma o en el papel |
| 6 | Pase a la siguiente pregunta |

**Interpretación y acción por puntaje:**

| Puntaje | Clasificación | Acción recomendada |
|---------|---------------|-------------------|
| **7–10** | ✅ Familia Funcional | Documentar fortalezas. Control habitual según programa |
| **4–6** | ⚠️ Disfunción Leve | Incluir objetivo de comunicación familiar en el plan |
| **0–3** | 🚨 Disfunción Severa | Priorizar intervención. Derivar a salud mental si procede |

---

## ⬛ PROCESO 4 — Construcción del Genograma Familiar

**Responsable:** Profesional clínico que realiza la evaluación  
**Resultado esperado:** Representación gráfica del árbol familiar con 3 generaciones mínimo

### 4.1 Convenciones Internacionales del Genograma

El genograma utiliza las convenciones estándar de McGoldrick, Gerson y Shellenberger (1985, revisadas 2008), adaptadas por el sistema para inclusión de género.

### 4.2 Simbología Completa

**Figuras según identidad de género:**

```
  [ ]         ( )        ◇           △
Masculino   Femenino  No binario  Gestación
                       /Trans.
```

**Indicadores de estados especiales:**

```
[[ ]]     [ ] borde rojo    ( ) gris    △ con X    △ relleno
Caso       Enferm.          Fallecida   Aborto     Aborto
Índice     Crónica                      Espontáneo Provocado
```

**Líneas de vínculo horizontal (parejas):**

```
[  ]════════( )      Matrimonio formal (doble línea continua)
[  ]────────( )      Convivencia (línea simple continua)
[  ]═══//═══( )      Separados/Divorciados (línea cortada)
```

**Descendencia:**

```
        [  ]────────( )
              |
       ┌──────┴──────┐
      [ ]            ( )
    (mayor)        (menor)
```
*(Hijos ordenados de izquierda a derecha, del mayor al menor)*

**Límite de convivencia:**

```
- - - - - - - - - - - - -
:         [ ]            :
:    ( )        ( )      :  ← Burbuja con línea punteada
:       [  ] Conv.       :     encerrando solo a quienes
- - - - - - - - - - - - -     viven bajo el mismo techo
```

### 4.3 Proceso de construcción (en plataforma)

1. Completar datos de Grupo Familiar (el motor interpreta los datos automáticamente)
2. La plataforma detecta relaciones padre-hijo a partir del campo "Parentesco"
3. Graphviz renderiza el gráfico en tiempo real
4. Verificar visual del genograma y corregir datos si hay errores de interpretación

### 4.4 Proceso de construcción (manual en papel)

1. **Determinar el eje horizontal**: La pareja central (jefe/a de hogar + cónyuge/pareja)
2. **Línea de unión**: Trazar la línea entre la pareja
3. **Descendencia**: Desde el centro de la línea de unión, trazar línea vertical hacia abajo y ramificar hacia cada hijo
4. **Generación superior**: Añadir padres/abuelos arriba y a los costados
5. **Anotaciones**: Edades, condiciones médicas, causas de muerte fuera de las figuras
6. **Límite de convivencia**: Trazar la burbuja punteada al final

---

## ⬛ PROCESO 5 — Construcción del Ecomapa Familiar

**Responsable:** Profesional clínico  
**Prerequisito:** Genograma completo del núcleo conviviente  
**Resultado esperado:** Mapa de vínculos con sistemas externos

### 5.1 Concepto del Ecomapa

El ecomapa (Hartman, 1978) representa las relaciones entre el núcleo familiar y los sistemas de su entorno. El objetivo es identificar:
- **Fuentes de apoyo** (vínculos que nutren y sostienen)
- **Fuentes de estrés** (vínculos que agotan o generan conflicto)
- **Aislamiento social** (ausencia de vínculos)

### 5.2 Nodos del Ecomapa (Sistemas Externos)

| Categoría | Nodos típicos |
|-----------|---------------|
| Salud | CESFAM, Hospital, Especialista, Farmacia |
| Educación | Sala cuna, Jardín infantil, Escuela, Liceo |
| Trabajo | Empleador, Sindicato, Capacitación |
| Social | Junta de Vecinos, Posta comunitaria, ONG |
| Espiritual | Iglesia, Comunidad religiosa |
| Legal/Judicial | Juzgado, Policía, Defensor |
| Familia extensa | Abuelos no convivientes, otros parientes |
| Chile Crece Contigo | Programa gubernamental |
| Municipio/FOSIS | Servicios sociales municipales |

### 5.3 Tipos de Vínculo

| Tipo de línea | Código | Significado clínico |
|---------------|--------|---------------------|
| **Gruesa continua** | `━━━━` | Vínculo fuerte, positivo y recíproco |
| **Punteada** | `•  •  •` | Vínculo débil, sporádico o instrumental |
| **Quebrada zigzag (roja)** | `~\/\/~` | Vínculo estresante, conflictivo o ambivalente |

### 5.4 Interpretación clínica del Ecomapa

| Patrón observado | Interpretación | Acción |
|------------------|----------------|--------|
| Predominio vínculos débiles | Aislamiento social | Vincular a red comunitaria (Junta vecinos, CESFAM) |
| Vínculos conflictivos con CESFAM | Desconfianza institucional | Trabajo de alianza terapéutica |
| Sin vínculos laborales | Cesantía estructural | Derivar a Oficina Municipal de Empleo (OMIL) |
| Vínculos fuertes con familia extensa | Factor protector | Documentar en T5, incorporar al plan |

---

## ⬛ PROCESO 6 — Diseño del Plan de Intervención

**Responsable:** Equipo interdisciplinario de salud familiar + familia  
**Prerequisito:** Clasificación de riesgo completa + APGAR + Genograma + Ecomapa  
**Resultado esperado:** Plan escrito, acordado y firmado con objetivos, responsables y fechas

### 6.1 Principios del Plan de Intervención

1. **Participación**: La familia debe co-diseñar el plan. No se impone, se acuerda.
2. **Realismo**: Los objetivos deben ser alcanzables en el contexto de la familia
3. **Especificidad**: Cada actividad debe ser concreta y medible
4. **Temporalidad**: Todas las actividades deben tener fecha comprometida
5. **Responsabilidad compartida**: Cada actividad debe tener un responsable del equipo Y de la familia

### 6.2 Estructura de una Actividad del Plan

| Campo | Descripción | Ejemplo |
|-------|-------------|---------|
| **Objetivo** | Meta estratégica | "Reducir el consumo de alcohol del padre" |
| **Actividad** | Tarea concreta | "Derivar a programa de alcohol y drogas COSAM" |
| **Fecha Programada** | Plazo comprometido | 2026-04-15 |
| **Responsable** | Quien ejecuta la acción | "A.S. González y Sr. Rojas (padre)" |
| **Fecha Real** | Cuando se cumplió | 2026-04-10 |
| **Evaluación** | Resultado observado | "Inscrito en COSAM, asistió 3 sesiones" |
| **Estado** | Avance | Cumplido / En proceso / No cumplido |

### 6.3 Priorización de Actividades según Riesgo

| Nivel de Riesgo | Plazo máximo primera intervención | Tipo de Intervención |
|-----------------|----------------------------------|---------------------|
| 🔴 ALTO | 15 días | VDI obligatoria + Reunión de equipo |
| 🟡 MEDIO | 30 días | Contacto telefónico + Consulta programada |
| 🟢 BAJO | 60 días | Control en programa habitual |

### 6.4 Firmas del Plan

La firma del plan tiene valor de compromiso formal. Debe obtenerse de:

1. **Evaluador/Profesional**: El profesional que realizó la evaluación
2. **Representante familiar**: El jefe/a de hogar o quien tenga la autoridad familiar
3. **Jefe de sector / Encargado MAIS**: Validación institucional del plan

**En papel**: Firmas a tinta, puño y letra, en el formulario físico.  
**En plataforma**: El login de funcionario tiene rigor clínico equivalente. Los nombres de los firmantes se registran en los campos correspondientes.

---

## ⬛ PROCESO 7 — Seguimiento y Gestión de Casos

**Responsable:** Profesional de cabecera asignado a la familia  
**Frecuencia:** Variable según nivel de riesgo (ver tabla)  
**Resultado esperado:** Actividades del plan actualizadas y familia con situación monitoreada

### 7.1 Periodicidad de Seguimiento Recomendada

| Nivel de Riesgo | Frecuencia contacto | Frecuencia visita domiciliaria |
|-----------------|--------------------|---------------------------------|
| 🔴 ALTO | Quincenal | Mensual mínimo |
| 🟡 MEDIO | Mensual | Bimestral |
| 🟢 BAJO | Trimestral | Semestral o según criterio clínico |

### 7.2 Proceso de Actualización del Seguimiento

1. Cargar la evaluación desde el catálogo usando el ID correspondiente
2. Acceder a la sección de Seguimiento del Plan
3. Para cada actividad comprometida:
   - Actualizar el **Estado** (Pendiente / En proceso / Cumplido / No cumplido)
   - Registrar la **Fecha Real** si se cumplió
   - Agregar **Observaciones de seguimiento** con hallazgos
   - Programar la **Fecha de próximo seguimiento**
4. Si hay cambios significativos en la situación familiar:
   - Revisar y actualizar los factores de riesgo chequeados
   - El sistema recalculará el nivel de riesgo automáticamente
5. Guardar la evaluación actualizada

### 7.3 Alertas de Seguimiento

Los siguientes cambios deben gatillar una actualización inmediata del registro:
- Hospitalización de algún integrante
- Ingreso a programa de salud mental
- Detección de nuevo factor de riesgo T1
- Cambio de domicilio
- Nacimiento o fallecimiento de integrante
- Inicio o término de proceso judicial

### 7.4 Gestión de Casos Complejos (Riesgo ALTO)

Para familias con riesgo ALTO, el protocolo ampliado es:

1. **Presentación en reunión de equipo**: Dentro de los 15 días de clasificación
2. **Asignación de profesional de cabecera**: Un profesional es el punto de contacto primario
3. **Visita domiciliaria integral (VDI)**: Obligatoria dentro del mes
4. **Articulación intersectorial**: Contactar según los factores:
   - VIF → Comisaría, OPD
   - Vulnerabilidad extrema → FOSIS, Municipio
   - Salud mental → COSAM, Psiquiatría Hospital
   - Trabajo infantil → SENAME, OPD

---

## ⬛ PROCESO 8 — Evaluaciones en Terreno (Postas Rurales)

**Responsable:** Profesional o TENS de la Posta / Técnico de Salud Rural  
**Contexto:** Zonas rurales sin conexión a internet confiable  
**Resultado esperado:** Datos recogidos en papel y digitalizados al regreso

### 8.1 Preparación Previa (CESFAM, antes de salir)

| Acción | Herramienta | Dónde |
|--------|-------------|-------|
| Descarga de pauta en blanco | Botón "📄 Descargar Pauta en Blanco" | Sidebar de la plataforma |
| Impresión de pautas | Impresora del CESFAM | En papel |
| Revisión de familias pendientes | Catálogo de evaluaciones | Dashboard plataforma |
| Cargar materiales adicionales | Lapiceros de tinta (azul y rojo) | Terreno |

### 8.2 En el Domicilio Rural

**Orden de trabajo recomendado:**

1. Dibujar el genograma (árboles) en el espacio cuadriculado
2. Completar los datos básicos de la familia
3. Registrar el grupo familiar (tabla de integrantes)
4. Marcar los factores de riesgo presentes (checkboxes físicos)
5. Aplicar el APGAR Familiar (5 preguntas, anotar puntaje por pregunta)
6. Completar el ecomapa (vínculos con la red social)
7. Acordar el plan de intervención y anotar actividades
8. **Obtener firmas a tinta** de la familia y del profesional evaluador
9. Verificar que todos los campos obligatorios estén completos

### 8.3 Al Regreso al CESFAM (Digitalización)

**Plazo máximo**: 48 horas después del trabajo en terreno.

1. Crear nueva evaluación en el sistema (o cargar la existente si hay seguimiento)
2. Traspasar los datos del papel a la plataforma campo por campo
3. Verificar que el grupo familiar digital coincide con el del papel
4. Marcar los mismos factores de riesgo que en el papel
5. Ingresar el puntaje APGAR por cada pregunta
6. Ingresar el plan de intervención
7. Guardar la evaluación

> 📌 Conservar las pautas físicas firmadas como respaldo. Se recomienda archivarlas por establecimiento/año.

### 8.4 Filtro por Establecimiento (Encargados de Postas)

El Encargado/a de Postas puede:
- Ver solo las evaluaciones del Sector Luna en el catálogo
- Filtrar por establecimiento específico en el sidebar
- Generar el REM-P7 con hojas desagregadas por cada posta

---

## ⬛ PROCESO 9 — Egreso y Alta Familiar

**Responsable:** Jefe/a de Sector o Profesional de cabecera  
**Disparador:** Cumplimiento de objetivos del plan O cambio de situación  
**Resultado esperado:** Familia egresada del programa con tipo de egreso documentado

### 9.1 Criterios de Egreso por Tipo

| Tipo de Egreso | Criterio | Acciones previas |
|----------------|----------|-----------------|
| **Alta** | Familia superó los factores de riesgo que motivaron su ingreso Y cumplió objetivos del plan | Evaluación final del plan + confirmación de mejoría |
| **Traslado** | Familia se mudó a otro sector o comuna | Enviar ficha al nuevo establecimiento |
| **Derivación** | Caso requiere mayor complejidad (hospital, programa especializado) | Completar formulario de derivación + contrareferencia |
| **Abandono** | Familia no responde a 3 contactos consecutivos sin justificación | Documentar intentos de contacto en observaciones |

### 9.2 Proceso de Egreso en la Plataforma

1. Cargar la evaluación de la familia
2. Confirmar que el plan de intervención está completo (todas las actividades evaluadas)
3. En la sección de Egreso, marcar el tipo correspondiente:
   - `egreso_alta`
   - `egreso_traslado`
   - `egreso_derivacion`
   - `egreso_abandono`
4. Registrar la **Fecha de Egreso**
5. Agregar observaciones explicando el motivo detallado del egreso
6. Guardar la evaluación

> ⚠️ El egreso NO elimina el registro de la base de datos. La evaluación queda como historia clínica archivada, con el indicador de egreso activado.

---

## ⬛ PROCESO 10 — Generación del Reporte Estadístico REM-P7

**Responsable:** Encargado/a MAIS o Jefe/a de Sector  
**Periodicidad:** Mensual (al cierre de cada mes)  
**Resultado esperado:** Archivo Excel con formato oficial MINSAL para envío a DESAM

### 10.1 Prerrequisitos

- Rol con permiso de descarga REM-P7 (Programador, Encargado MAIS, Jefe de Sector)
- Conocer el **número de familias inscritas** por sector:
  - N° familias inscritas Sector Sol
  - N° familias inscritas Sector Luna

### 10.2 Proceso de Generación

1. Acceder a la sección de Reportes o REM-P7
2. Ingresar el número de familias inscritas para:
   - Sector Sol (Urbano)
   - Sector Luna (Rural)
3. Presionar el botón **"Generar REM-P7"**
4. El sistema calculará automáticamente:
   - Familias evaluadas por sector y nivel de riesgo
   - Familias con y sin plan de intervención
   - Familias egresadas por tipo de egreso
5. Descargar el archivo Excel generado

### 10.3 Validación del REM-P7

Antes de enviar el REM-P7, verificar:
- [ ] Los totales de familias evaluadas coinciden con el registro manual
- [ ] Los egresos están correctamente tipificados
- [ ] El número de familias inscritas fue ingresado correctamente
- [ ] La fecha de generación es del período correcto

### 10.4 Estructura del REM-P7 generado

El Excel contiene:

**Hoja "CONSOLIDADO"**:
- Sección A: Clasificación Urbano (Sector Sol): inscritas, evaluadas, por nivel
- Sección A.1: Clasificación Rural (Sector Luna): mismos indicadores
- Sección B: Intervención Urbana y Rural: familias con/sin plan, egresos

**Hojas por Posta** (solo para Encargados de Postas):
- Una hoja adicional por cada establecimiento rural con sus datos desagregados

---

## ⬛ PROCESO 11 — Gestión de Usuarios y Accesos

**Responsable:** Programador o Administrador del Sistema  
**Disparador:** Alta de nuevo funcionario / Cambio de cargo / Baja de funcionario

### 11.1 Estructura de Roles RBAC

| Rol | Cargo típico | Visibilidad | Permisos especiales |
|-----|-------------|-------------|---------------------|
| `programador` | Desarrollador/TI | Global (todo) | Migrar IDs, Limpiar caché |
| `encargado_mais` | Encargado/a MAIS | Global (todo) | REM-P7, Auditoría |
| `jefe_sector` | Jefe/a de Sector | Solo su sector | REM-P7 |
| `equipo_sector` | Profesionales | Solo su sector | Sin permisos extra |
| `usuario` | Técnicos/Auxiliares | Solo su unidad | Sin permisos extra |

**Restricción de Sector:**
- Usuarios con "Sol" en cargo o unidad → Solo ven evaluaciones Sector Sol
- Usuarios con "Luna" o "Postas" → Solo ven evaluaciones Sector Luna
- Encargados MAIS y Programadores → Ven todo

### 11.2 Alta de Nuevo Usuario

Para agregar un nuevo usuario al sistema:
1. Acceder a la hoja "usuarios" del Google Sheets vinculado
2. Agregar una nueva fila con los campos:
   - `usuario`: RUT del funcionario (sin puntos, con guión)
   - `contraseña`: Contraseña inicial (debe ser cambiada en el primer ingreso)
   - `nombre`: Nombre completo
   - `cargo`: Cargo institucional exacto (determina el RBAC)
   - `rol`: Rol del sistema (ver tabla arriba)
   - `Programa/Unidad`: Unidad o programa al que pertenece
3. Notificar al usuario sus credenciales

### 11.3 Baja o Modificación de Usuario

1. Localizar la fila del usuario en la hoja "usuarios" del Google Sheets
2. Modificar los campos necesarios (cargo, rol, unidad)
3. Para dar de baja: cambiar la contraseña por una no comunicada al usuario

---

## ⬛ PROCESO 12 — Operación del Dashboard Analítico

**Responsable:** Jefe/a de Sector, Encargado/a MAIS  
**Periodicidad:** Mensual mínimo; puede ser en tiempo real según necesidad  
**Resultado esperado:** Análisis actualizado de la situación de riesgo del sector

### 12.1 Acceso y Actualización

El dashboard se actualiza automáticamente con un caché de 5 minutos. Para forzar la actualización:
1. Presionar el botón **"Actualizar Dashboard"** en el sidebar

### 12.2 Lectura e Interpretación de Gráficos

**Donut de Distribución de Riesgo:**
- Muestra la proporción de familias en cada nivel
- El número central es el total de evaluaciones visibles para el usuario

**Barras por Sector (Sol/Luna):**
- Permite comparar la carga de riesgo entre zonas urbana y rural
- Barras apiladas: ALTO en rojo, MEDIO en amarillo, BAJO en verde

**Top 12 Factores de Riesgo:**
- Los 3 factores con barras oscuras son los más frecuentes
- Estos representan las urgencias de intervención epidemiológica del sector

**Brecha de Intervención:**
- Familias con plan (azul) vs sin plan (celeste claro)
- Idealmente debe haber 0 familias en riesgo ALTO sin plan

**Histograma de Puntajes:**
- Zonas de fondo coloridas indican los rangos: verde=bajo, amarillo=medio, rojo=alto
- Permite ver si hay familias cercanas al umbral de subir de nivel

**Evolución Temporal:**
- Muestra el ritmo de evaluaciones mes a mes
- Picos pueden indicar campañas o visitas masivas

### 12.3 Acciones derivadas del Dashboard

| Hallazgo en Dashboard | Acción recomendada |
|-----------------------|-------------------|
| Alto % familias ALTO sin plan | Revisar cartera y asignar VDI urgentes |
| Aumento sostenido de VIF en T1 | Activar protocolo VIF, articular con Comisaría y OPD |
| Brecha de intervención > 30% | Revisar carga de casos por profesional |
| Disminución de evaluaciones por mes | Revisar adherencia del equipo al registro |

---

## 📊 Diagrama de Flujo General del Sistema

```
[IDENTIFICACIÓN DE FAMILIA]
         ↓
[¿Ya está en el sistema?]
 ├─ SI → [CARGAR EVALUACIÓN] → [SEGUIMIENTO]
 └─ NO ↓
[NUEVA FICHA (ID auto-generado)]
         ↓
[DATOS BÁSICOS + GRUPO FAMILIAR]
         ↓
[EVALUACIÓN RIESGO — 5 TABLAS]
         ↓ (Sistema calcula automáticamente)
[RESULTADO: ALTO 🔴 / MEDIO 🟡 / BAJO 🟢]
         ↓
[APGAR FAMILIAR (5 preguntas)]
         ↓
[GENOGRAMA + ECOMAPA]
         ↓
[PLAN DE INTERVENCIÓN + FIRMAS]
         ↓
[GUARDAR EN GOOGLE SHEETS]
         ↓
[CICLO DE SEGUIMIENTO (periódico)]
         ↓
[¿Objetivos cumplidos?]
 ├─ NO → [ACTUALIZAR SEGUIMIENTO] → [CICLO]
 └─ SI ↓
[EGRESO: Alta / Traslado / Derivación / Abandono]
         ↓
[REGISTRO CERRADO EN BD (no se elimina)]
         ↓
[DATOS PARA DASHBOARD + REM-P7]
```

---

## 📈 Indicadores de Proceso y Gestión

### Indicadores Operativos del Sistema

| Indicador | Fórmula | Meta sugerida |
|-----------|---------|---------------|
| **Cobertura de evaluación** | N° familias evaluadas / N° familias inscritas × 100 | ≥ 80% anual |
| **% Familias con plan** | N° familias con plan / N° familias evaluadas × 100 | 100% ALTO y MEDIO |
| **% Brecha de intervención** | N° familias sin plan / N° familias evaluadas × 100 | <20% |
| **Tiempo de 1ra intervención** | Días entre evaluación y primera actividad del plan | ≤15 días (ALTO) |
| **Tasa de egreso** | N° egresos / N° familias en programa × 100 | Variable según programa |
| **% RIESGO ALTO** | N° familias ALTO / N° evaluadas × 100 | Benchmark territorial |

### Indicadores de Calidad del Registro

| Indicador | Descripción | Meta |
|-----------|-------------|------|
| **Completitud del registro** | % de evaluaciones con grupo familiar completo | ≥ 95% |
| **Adherencia al protocolo** | % evaluaciones con plan de intervención firmado | 100% ALTO |
| **Oportunidad de registro** | Días entre evaluación en papel y digitalización | ≤ 48 horas |

---

## 🔐 Control de Versiones y Auditoría

### Registro Automático de Auditoría

Cada acción registrada en la plataforma genera un **evento de auditoría** automático que se guarda en la hoja "Auditoría" de Google Sheets con:

| Campo | Descripción |
|-------|-------------|
| **Timestamp** | Fecha y hora exacta de la acción |
| **Usuario** | RUT del usuario que realizó la acción |
| **Cargo** | Cargo del usuario |
| **Acción** | Tipo de acción (Guardar, Editar, Ver, Generar PDF) |
| **Detalles** | Descripción específica de la acción |
| **ID Evaluación** | ID del registro afectado |

### Acceso al Log de Auditoría

Solo el rol `programador` y `encargado_mais` pueden acceder al log de auditoría en Google Sheets directamente.

### Ciclo de Caché y Consistencia de Datos

| Mecanismo | Tiempo | Propósito |
|-----------|--------|-----------|
| **Caché de datos crudos** | 5 minutos | Reducir llamadas a Google Sheets |
| **Invalidación de caché al guardar** | Inmediata | Al guardar, el dashboard ve datos frescos |
| **TTL de mapa de RUTs** | 5 minutos | Cache global de validación de duplicados |

---

*Manual de Procesos v3.0 — Plataforma MAIS — CESFAM Cholchol*  
*Generado con la asistencia tecnológica del ecosistema Antigravity*
