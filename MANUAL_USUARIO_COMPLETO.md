# 📘 MANUAL DE USUARIO
# Plataforma Integral de Salud Familiar MAIS
### Sistema de Evaluación de Riesgo Biopsicosocial Familiar — CESFAM Cholchol

> **Versión:** 3.0 | **Fecha:** Marzo 2026  
> **Audiencia:** Profesionales, Técnicos y Administrativos de APS (CESFAM, Postas Rurales, EMR)

---

## ÍNDICE

1. [Introducción y Propósito](#1-introducción-y-propósito)
2. [Acceso al Sistema — Inicio de Sesión](#2-acceso-al-sistema--inicio-de-sesión)
3. [Panel de Control (Barra Lateral Izquierda)](#3-panel-de-control-barra-lateral-izquierda)
4. [Catálogo de Evaluaciones — Mis Encuestas Familiares](#4-catálogo-de-evaluaciones--mis-encuestas-familiares)
5. [Creación de una Nueva Ficha Familiar](#5-creación-de-una-nueva-ficha-familiar)
6. [Módulo Grupo Familiar — Editor Inclusivo](#6-módulo-grupo-familiar--editor-inclusivo)
7. [Evaluación de Riesgo Biopsicosocial — Las 5 Tablas](#7-evaluación-de-riesgo-biopsicosocial--las-5-tablas)
8. [Test APGAR Familiar](#8-test-apgar-familiar)
9. [Plan de Intervención y Compromisos](#9-plan-de-intervención-y-compromisos)
10. [Seguimiento del Plan Intervención](#10-seguimiento-del-plan-intervención)
11. [Guardar y Egreso Familiar](#11-guardar-y-egreso-familiar)
12. [Genograma y Ecomapa — Visualización Familiar](#12-genograma-y-ecomapa--visualización-familiar)
13. [Dashboard Analítico — Estadísticas y Reportes](#13-dashboard-analítico--estadísticas-y-reportes)
14. [Descarga de Documentos PDF](#14-descarga-de-documentos-pdf)
15. [Reporte REM-P7 (Jefaturas y Encargados)](#15-reporte-rem-p7-jefaturas-y-encargados)
16. [Uso Offline — Pauta en Blanco para Terreno](#16-uso-offline--pauta-en-blanco-para-terreno)
17. [Digitación desde Pauta en Papel](#17-digitación-desde-pauta-en-papel)
18. [Preguntas Frecuentes (FAQ)](#18-preguntas-frecuentes-faq)
19. [Soporte y Contacto Técnico](#19-soporte-y-contacto-técnico)

---

## 1. Introducción y Propósito

La **Plataforma MAIS** (Modelo de Atención Integral de Salud) es una herramienta digital centralizada diseñada para apoyar a los equipos de Atención Primaria en Salud (APS) en la gestión sistemática del riesgo familiar biopsicosocial. Permite:

- **Registrar y evaluar** el riesgo de familias bajo control en su sector territorial (Sol o Luna).
- **Calcular automáticamente** el nivel de riesgo (Alto, Medio, Bajo) sin necesidad de sumar puntajes a mano.
- **Generar gráficos** familiares (Genograma y Ecomapa) de forma automática.
- **Crear planes de intervención** con objetivos, responsables y fechas de seguimiento.
- **Descargar reportes** en PDF y generar el formulario estadístico REM-P7.
- **Analizar datos** con un dashboard estadístico interactivo en tiempo real.

### ¿Quién puede usar esta plataforma?
La plataforma está diseñada para todos los funcionarios de la red de APS de CESFAM Cholchol y sus Postas/EMR asociadas. El acceso y la visibilidad de los datos varía según el **rol** asignado a cada funcionario (ver Sección 3).

### Sectores
| Sector | Zona | Establecimientos |
|--------|------|-----------------|
| **Sol** | Urbano | CESFAM Cholchol |
| **Luna** | Rural | Postas y EMR rurales |

---

## 2. Acceso al Sistema — Inicio de Sesión

### Pasos para ingresar:

1. **Abra su navegador web** y acceda a la URL de la plataforma.
2. En la pantalla de inicio verá dos campos de texto:
   - **RUT**: Ingrese su RUT sin puntos y con guión (ejemplo: `12345678-9`)
   - **Contraseña**: Ingrese su clave personal
3. Haga clic en el botón verde **"Ingresar al Sistema Clínico"**
4. Si las credenciales son correctas:
   - Se cargará su **Panel Clínico** en la barra lateral izquierda
   - Verá su nombre y cargo en la parte superior
   - Se mostrará el catálogo de evaluaciones según su sector/unidad

### ¿Qué pasa si no puedo ingresar?
- Verifique que su RUT esté escrito correctamente (sin puntos, con guión)
- Si su contraseña no funciona, contacte al administrador del sistema
- Si aparece el mensaje "Usuario no encontrado", es posible que su cuenta no esté registrada aún

> ⚠️ **Importante**: Por seguridad, la plataforma aplica **control de acceso basado en roles (RBAC)**. Usted solo verá las evaluaciones correspondientes a su sector o unidad. Intentar acceder a registros de otro sector arrojará un error de permisos.

---

## 3. Panel de Control (Barra Lateral Izquierda)

La barra lateral es el centro de navegación de la plataforma. Contiene las siguientes secciones:

### 3.1 Información del Usuario
En la parte superior de la barra lateral verá su nombre, cargo y unidad asignada. Esto es solo de lectura.

### 3.2 Botón "Nueva Ficha" ➕
Al presionar este botón grande verde:
- **Limpia todos los campos** del formulario central
- Le entrega un formulario vacío y listo para registrar una nueva familia
- Genera automáticamente un **ID de Evaluación** único en formato `EVA-NNN-FAM-XXX`
  - `NNN`: número correlativo (ej: 001, 002, 003...)
  - `XXX`: primeras 3 letras del apellido de la familia (ej: ORT para Ortiz)

### 3.3 Búsqueda Directa por ID 🔍
Si conoce el ID de una evaluación específica (ej: `EVA-012-FAM-CON`):
1. Escríbalo en el campo de búsqueda de la barra lateral
2. Presione **"Cargar Registro"**
3. La ficha completa se cargará en el formulario central para edición

### 3.4 Descarga de Pauta en Blanco 📄
Para uso offline (terreno, visita domiciliaria sin internet):
- Presione **"📄 Descargar Pauta en Blanco"**
- Se generará un PDF listo para imprimir con todos los campos del formulario
- Incluye espacio cuadriculado para dibujar el genograma y el ecomapa a mano
- Contiene instrucciones y simbología de referencia para uso en terreno

### 3.5 Filtro por Establecimiento (Encargados de Postas)
Si su rol es Encargado/a de Postas, verá un selector adicional para filtrar los datos por establecimiento rural específico.

### 3.6 Botón "Actualizar Dashboard"
Recarga los datos del servidor (Google Sheets). Use este botón si no ve evaluaciones recientes.

### 3.7 Opciones Administrativas (Solo Programadores/Encargados MAIS)
- **Migrar IDs**: Actualiza todos los IDs de evaluación al formato nuevo
- **Limpiar caché**: Fuerza la recarga de datos desde Google Sheets

---

## 4. Catálogo de Evaluaciones — Mis Encuestas Familiares

En el área central de la pantalla, debajo del encabezado de bienvenida, encontrará una tabla con todas las evaluaciones registradas que son visibles para su rol.

### Columnas del catálogo:
| Columna | Descripción |
|---------|-------------|
| **ID Evaluación** | Código único (ej: EVA-005-FAM-GOM) |
| **Familia** | Apellido(s) de la familia |
| **Dirección** | Domicilio |
| **Sector** | Sol (Urbano) o Luna (Rural) |
| **Nivel** | Riesgo Alto 🔴 / Medio 🟡 / Bajo 🟢 |
| **Fecha** | Fecha de la evaluación |
| **Establecimiento** | CESFAM Cholchol o Posta específica |

### Cómo buscar en el catálogo:
1. Use la barra **"🔍 Buscar por Familia, RUT o Dirección"** para filtrar en tiempo real
2. Escriba cualquier parte del nombre, apellido, dirección o RUT
3. Los resultados se filtran instantáneamente a medida que escribe

### Cómo abrir una ficha desde el catálogo:
1. Localice la familia en el catálogo
2. **Copie el texto de la columna "ID Evaluación"** (ej: `EVA-012-FAM-CON`)
3. **Péguelo en la barra de Búsqueda Directa** de la barra lateral
4. Presione "Cargar Registro"

> 💡 **Tip**: También puede ver el ID en la columna de la tabla y buscarlo directamente en el campo de búsqueda lateral sin necesidad de copiarlo.

---

## 5. Creación de una Nueva Ficha Familiar

Para registrar una nueva familia en el sistema:

1. **Presione el botón "➕ Nueva Ficha"** en la barra lateral izquierda
2. Complete los campos del **formulario de datos básicos**:

### 5.1 Datos Básicos de la Evaluación

| Campo | Descripción | Obligatorio |
|-------|-------------|-------------|
| **ID Evaluación** | Se genera automáticamente. No lo modifique | Automático |
| **Nombre y Apellidos** | Apellido(s) principal(es) de la familia | ✅ Sí |
| **Dirección** | Dirección completa del domicilio evaluado | ✅ Sí |
| **RUT del Responsable** | RUT del jefe/a de hogar o apoderado | ✅ Sí |
| **Fecha de Evaluación** | Fecha en que se realizó la visita/entrevista | ✅ Sí |
| **Establecimiento** | CESFAM Cholchol o nombre de la Posta/EMR | ✅ Sí |
| **Sector** | Sol (Urbano) o Luna (Rural) | ✅ Sí |
| **Programa/Unidad** | Programa clínico al que pertenece (ej: MAIS, Salud Mental, Cardiovascular) | ✅ Sí |
| **Evaluador** | Nombre del profesional que realiza la evaluación | ✅ Sí |
| **Parentesco del Evaluador** | Relación del evaluador con la familia | ✅ Sí |
| **Tipo de Unión Familiar** | Casados, Convivencia, Separados, Divorciados | Opcional |
| **Pueblo Originario** | Pertenencia étnica según censo INE 2017 | Opcional |
| **Observaciones** | Notas adicionales relevantes | Opcional |

### 5.2 Validación del RUT
Al ingresar el RUT del responsable, el sistema puede **buscar automáticamente en la base de datos FONASA** (si el establecimiento tiene acceso habilitado) para:
- Confirmar que la persona está inscrita
- Pre-cargar algunos datos demográficos
- Detectar si ya existe una evaluación previa para esa persona

> ⚠️ Si el sistema detecta que el RUT ya fue registrado en otra evaluación existente, le mostrará una advertencia con el ID de la evaluación previa.

---

## 6. Módulo Grupo Familiar — Editor Inclusivo

El módulo de Grupo Familiar permite registrar a cada integrante que compone el núcleo familiar evaluado.

### 6.1 Cómo agregar integrantes

- Presione el botón **"+ Agregar Miembro"** o similar para añadir una nueva fila
- Complete los campos de cada persona en la tabla editable
- Para eliminar un integrante, presione el ícono **🗑** o botón de eliminar de esa fila

### 6.2 Campos del Grupo Familiar

| Campo | Descripción | Opciones |
|-------|-------------|----------|
| **Nombre y Apellidos** | Nombre completo | Texto libre |
| **RUT** | RUT de la persona | Texto |
| **F. Nac** | Fecha de nacimiento | Calendario |
| **Identidad de Género** | Auto-identificación de género | Ver lista abajo |
| **Parentesco** | Relación con el jefe de hogar | Ver lista abajo |
| **E. Civil** | Estado civil o situación reproductiva | Texto |
| **Patología Crónica** | Si tiene enfermedad crónica documentada | ✅ Checkbox |
| **Resp** | Indica si es el caso índice (persona consultante) | ✅ Checkbox |

### 6.3 Opciones de Identidad de Género (Módulo Inclusivo)

| Opción | Descripción | Símbolo en Genograma |
|--------|-------------|----------------------|
| **Masculino** | Hombre biológico o trans-masculino | ☐ Cuadrado |
| **Femenino** | Mujer biológica o trans-femenina | ○ Círculo |
| **No binario** | Identidad no binaria | ◇ Rombo |
| **Transgénero** | Trans sin especificar binario | ◇ Rombo |
| **Prefiero no decir** | Sin especificación de género | ◇ Rombo |
| **Gestación/Aborto** | Embarazo o pérdida gestacional | △ Triángulo |

### 6.4 Opciones de Parentesco

- Jefe/a de Hogar
- Cónyuge/Pareja
- Hijo/a
- Hijo/a (Gemelo Fraterno) / Hijo/a (Gemelo Idéntico)
- Padre/Madre
- Hermano/a
- Abuelo/a
- Nieto/a
- Tío/a / Sobrino/a
- Hijo/a Adoptivo/a
- Otro familiar
- No familiar

### 6.5 Campo E. Civil (Estado Civil y Gestación)

Este campo acepta texto libre pero tiene valores especiales:

| Valor | Efecto en Genograma |
|-------|---------------------|
| Texto normal (Soltero, Casado, etc.) | Sin efecto visual especial |
| **F** o **Fallecido** | Dibuja la figura en gris oscuro con sombra |
| **Espontaneo** | Triángulo con "X" (aborto espontáneo) |
| **Provocado** | Triángulo relleno (aborto inducido) |

### 6.6 Caso Índice (check "Resp")

Marque el campo **"Resp"** en el integrante que es el **caso índice** (la persona cuya situación de salud motivó la evaluación familiar). Este integrante:
- Aparecerá con **doble borde** en el genograma
- Es la persona desde cuya perspectiva se aplica el APGAR Familiar
- **Debe existir al menos 1 caso índice** por evaluación

### 6.7 Patología Crónica

Si un integrante tiene una enfermedad crónica documentada clinicamente, marque el checkbox **"Patología Crónica"**. Este integrante aparecerá con **borde rojo** en el genograma.

---

## 7. Evaluación de Riesgo Biopsicosocial — Las 5 Tablas

La evaluación de riesgo es el corazón de la plataforma. Se organiza en **5 tablas de factores**, agrupados por gravedad. Los checkboxes representan factores presentes en la familia al momento de la evaluación.

### 7.1 ¿Cómo usar las tablas?

1. Revise cada factor en las 5 tablas
2. **Marque el checkbox** de los factores que SÍNELL apliquen a la familia evaluada
3. El **indicador de riesgo se actualiza automáticamente** en tiempo real
4. No necesita calcular nada manualmente

### 7.2 Tabla 1 — Riesgo Máximo (Banderas Rojas Absolutas)

> **Regla**: La presencia de **cualquiera** de estos factores clasifica automáticamente a la familia como **RIESGO ALTO**, sin importar el puntaje acumulado.

| # | Factor de Riesgo |
|---|-----------------|
| 1 | Familia con VIF (violencia intrafamiliar: física, psicológica, sexual, económica) |
| 2 | Consumo problema de drogas o dependencia de algún integrante |
| 3 | Consumo problema de alcohol (AUDIT > 13) |
| 4 | Patología de salud mental descompensada o sin tratamiento |
| 5 | Abuso sexual sufrido por algún integrante de la familia |
| 6 | Adulto mayor y/o niño/a en riesgo biopsicosocial grave |
| 7 | Pauta EPSA (ChCC) con riesgo |
| 8 | Vulnerabilidad socioeconómica extrema (indigencia) |
| 9 | Trabajo infantil en niños menores de 14 años |

### 7.3 Tabla 2 — Riesgo Alto (Doble Condición)

> **Regla**: La presencia de **2 o más** factor de esta tabla clasifica como **RIESGO ALTO**. Solo **1 factor** en T2 eleva el riesgo a **MEDIO** (salvo que el puntaje de T3+T4 ya lo lleve a ALTO).

| # | Factor de Riesgo |
|---|-----------------|
| 1 | Enfermedad grave o terminal en algún integrante |
| 2 | Paciente con alto riesgo de hospitalización |
| 3 | Discapacidad física y/o mental (Barthel ≤ 35 puntos) |
| 4 | Patología de salud mental leve o moderada |
| 5 | Conflictos o problemas con la justicia |
| 6 | Incumplimiento de roles parentales |
| 7 | Sobrecarga del cuidador principal |
| 8 | Conflictos familiares severos o crisis de comunicación |
| 9 | Adultos en riesgo biopsicosocial a cargo de niños |

### 7.4 Tabla 3 — Riesgo Medio (4 puntos por factor)

> **Regla**: Cada factor marcado en esta tabla suma **4 puntos** al puntaje total.

| # | Factor de Riesgo |
|---|-----------------|
| 1 | Patología crónica descompensada sintomática |
| 2 | Miembro con discapacidad leve/moderada (40-55 puntos Barthel) |
| 3 | Rezago o déficit en desarrollo psicomotor |
| 4 | Madre adolescente |
| 5 | Duelo reciente (pérdida de integrante significativo) |
| 6 | Ausencia o escasa red de apoyo social/familiar |
| 7 | Cesantía de más de 1 mes del proveedor principal |
| 8 | Vulnerabilidad socioeconómica no extrema |
| 9 | Precariedad laboral (empleo temporal o por honorarios) |
| 10 | Hacinamiento (2.5 o más personas por dormitorio) |
| 11 | Entorno inseguro (delincuencia) |
| 12 | Adulto mayor que vive solo |
| 13 | Deserción o fracaso escolar |
| 14 | Analfabetismo del padre, madre o cuidador principal |
| 15 | Escolaridad básica incompleta de los padres |
| 16 | Dificultad de acceso a servicios de salud u otras entidades |

### 7.5 Tabla 4 — Riesgo Bajo (3 puntos por factor)

> **Regla**: Cada factor marcado en esta tabla suma **3 puntos** al puntaje total.

| # | Factor de Riesgo |
|---|-----------------|
| 1 | Hogar monoparental |
| 2 | Riesgo cardiovascular (tabaco, obesidad) |
| 3 | Foco de contaminación ambiental cercano al domicilio |
| 4 | Deficiencia en hábitos de higiene |
| 5 | Ausencia de prácticas de recreación |
| 6 | Ausencia de espacios seguros para la recreación |
| 7 | Endeudamiento familiar elevado (> 40% de ingresos) |
| 8 | Servicios básicos incompletos o inadecuados |

### 7.6 Tabla 5 — Factores Protectores (No suman ni restan puntos)

> **Regla**: Estos factores NO modifican el puntaje total. Son recursos y fortalezas de la familia que se documentan para el diseño del plan de intervención. Se usan cualitativamente.

| # | Factor Protector |
|---|-----------------|
| 1 | Lactancia materna exclusiva o complementaria |
| 2 | Hábitos saludables (actividad física, alimentación) |
| 3 | Presencia de redes sociales/comunitarias |
| 4 | Presencia de red de apoyo familiar |
| 5 | Habilidades comunicacionales y de expresión de afecto |
| 6 | Recursos socioeconómicos suficientes |
| 7 | Resiliencia (capacidad de sobreponerse a crisis) |
| 8 | Vivienda adecuada |

### 7.7 Indicador de Riesgo en Tiempo Real

En la parte superior del formulario de evaluación verá un **semáforo de riesgo** que se actualiza automáticamente:

| Resultado | Color | Significado |
|-----------|-------|-------------|
| **RIESGO ALTO** | 🔴 Rojo | Factor T1 presente O ≥2 factores T2 O puntaje ≥ 26 |
| **RIESGO MEDIO** | 🟡 Amarillo | 1 factor T2 O puntaje entre 17 y 25 puntos |
| **RIESGO BAJO** | 🟢 Verde | Puntaje ≤ 16 sin banderas rojas T1 o T2 |

---

## 8. Test APGAR Familiar

El **APGAR Familiar** (Smilkstein) es un instrumento validado que mide la percepción del caso índice sobre el funcionamiento de su entorno familiar.

### 8.1 Cómo aplicar el APGAR

Para cada una de las 5 preguntas:
1. Léala directamente al caso índice (sin sugerir la respuesta)
2. Según la respuesta del paciente, asigne la puntuación:
   - **"Casi nunca"** → 0 puntos
   - **"A veces"** → 1 punto
   - **"Casi siempre"** → 2 puntos

### 8.2 Las 5 Preguntas del APGAR

| Letra | Dimensión | Pregunta orientadora |
|-------|-----------|----------------------|
| **A** | Adaptación | ¿Está satisfecho/a con la ayuda que recibe de su familia cuando tiene un problema? |
| **P** | Participación | ¿Conversen en familia los problemas y comparten las decisiones? |
| **G** | Gradiente de Crecimiento | ¿Las decisiones importantes se toman en conjunto? |
| **A** | Afecto | ¿Expresa su familia el afecto y responde a sus emociones? |
| **R** | Resolución | ¿Está satisfecho/a con el tiempo que su familia dedica a compartir? |

### 8.3 Interpretación del Puntaje APGAR

| Puntaje Total | Clasificación | Interpretación |
|---------------|---------------|----------------|
| **7 a 10** | ✅ Familia Funcional | Funcionamiento familiar saludable |
| **4 a 6** | ⚠️ Disfunción Leve | Tensión moderada, requiere apoyo |
| **0 a 3** | 🚨 Disfunción Severa | Crisis familiar profunda, alta prioridad |

> El sistema calcula automáticamente el total y muestra la clasificación.

---

## 9. Plan de Intervención y Compromisos

Posterior a la evaluación de riesgo y el APGAR, debe registrar el **Plan de Intervención** acordado con la familia.

### 9.1 Edición del Plan de Intervención

La tabla del plan tiene las siguientes columnas:

| Columna | Descripción |
|---------|-------------|
| **Objetivo** | Meta general de la intervención |
| **Actividad** | Tarea específica a realizar |
| **Fecha Prog** | Fecha programada para cumplir la actividad |
| **Responsable** | Nombre del profesional y/o familiar responsable |
| **Fecha Real** | Fecha en que efectivamente se realizó |
| **Evaluación** | Comentario evaluativo sobre el resultado |
| **Estado** | Pendiente / En proceso / Cumplido / No cumplido |
| **F. Seguimiento** | Fecha del próximo control |
| **Obs. Seguimiento** | Observaciones del seguimiento |

### 9.2 Cómo agregar actividades al plan
1. Use el botón **"+ Agregar Actividad"** en la sección de plan de intervención
2. Complete cada campo de la nueva fila
3. Sea específico: "Tramitar pensión de viudez" es mejor que "Gestión previsional"
4. Asigne un responsable claro del equipo de salud Y de la familia
5. Calendarice las fechas para crear compromisos verificables

### 9.3 Firma del Plan — Compromiso Intervencional

Antes de guardar, la sección de firmas documenta el compromiso formal:

| Campo | Quién firma |
|-------|-------------|
| **Firma Evaluador** | El profesional que realizó la evaluación |
| **Firma Funcionario** | Representante del CESFAM |
| **Firma Beneficiario** | Representante/jefe de hogar de la familia |
| **Firma Equipo** | Miembro adicional del equipo interdisciplinario |
| **Firma Jefe/a** | Jefe/a de sector o encargado/a MAIS |

> 📌 En la plataforma digital, el acta digitada tiene rigor clínico bajo su inicio de sesión de funcionario. En papel, debe haber firmas a tinta de puño y letra.

### 9.4 Equipo de Salud

Puede registrar los miembros del equipo de salud presentes en la evaluación. Cada miembro tiene:
- **Nombre y Profesión**: Nombre completo y cargo
- **Firma**: Checkbox que indica si el profesional firmó el acta

---

## 10. Seguimiento del Plan de Intervención

El módulo de seguimiento permite registrar el avance de cada actividad comprometida en el plan.

### 10.1 Tabla de Seguimiento

Para cada actividad del plan:
1. Acceda a la sección de seguimiento (pestaña o sección correspondiente)
2. Actualice el **Estado** de cada actividad:
   - **Pendiente**: La actividad aún no se ha iniciado
   - **En proceso**: La actividad está en ejecución
   - **Cumplido**: La actividad se completó satisfactoriamente
   - **No cumplido**: La actividad no pudo realizarse (documente el motivo en Obs.)
3. Registre la **Fecha Real** de realización
4. Agregue **Observaciones de Seguimiento** con hallazgos relevantes

### 10.2 Análisis Clínico Automatizado

La plataforma genera automáticamente un **Informe de Análisis Familiar Consolidado** basado en los datos ingresados. Este informe incluye:

- **Identificación del caso**: Programa, caso índice, composición familiar
- **Clasificación del riesgo con alerta contextualizada**:
  - Alerta Crítica (T1): Lista los factores críticos específicos detectados
  - Alerta Moderada (T2): Indica presencia de factores moderados
  - Estado equilibrado: Cuando no hay banderas rojas
- **Interpretación del Genograma y Ecomapa**: Análisis de la estructura familiar y redes externas
- **Sugerencias Prospectivas**: Recomendaciones de intervención según el nivel de riesgo detectado

> El análisis clínico es un apoyo para el equipo, NO reemplaza el juicio clínico del profesional.

---

## 11. Guardar y Egreso Familiar

### 11.1 Guardar la Evaluación

Una vez completado el formulario:
1. Presione el botón **"💾 Guardar Evaluación"**
2. El sistema guardará automáticamente en Google Sheets
3. Si la evaluación ya existía (mismo ID), **actualiza** el registro existente
4. Si es nueva, **crea un nuevo registro**
5. Verá un mensaje de confirmación de éxito o error

> 💡 Puede guardar en cualquier momento, incluso si la evaluación está incompleta. El sistema no borra datos previos.

### 11.2 Registro de Egreso

Cuando una familia completa su ciclo de intervención y debe ser dada de baja del programa, registre el tipo de egreso:

| Tipo de Egreso | Descripción |
|----------------|-------------|
| **Alta** | La familia superó el riesgo y累cumplió sus objetivos |
| **Traslado** | La familia se trasladó a otro sector o establecimiento |
| **Derivación** | La familia fue derivada a un nivel de mayor complejidad |
| **Abandono** | La familia abandonó el programa sin completarlo |

1. Seleccione el tipo de egreso correspondiente
2. Registre la **Fecha de Egreso**
3. Guarde la evaluación

---

## 12. Genograma y Ecomapa — Visualización Familiar

La plataforma genera automáticamente representaciones gráficas de la estructura familiar basándose en los datos del Grupo Familiar.

### 12.1 El Genograma

El genograma es el árbol genealógico clínico de la familia. Se genera en tiempo real usando Graphviz.

**Símbolos del genograma:**

| Símbolo | Significado |
|---------|-------------|
| ☐ Cuadrado | Masculino/Hombre |
| ○ Círculo | Femenino/Mujer |
| ◇ Rombo | No binario / Transgénero / Sin especificar |
| △ Triángulo | Gestación en curso |
| ☐ con borde rojo | Enfermedad crónica |
| ☐☐ Doble borde | Caso índice / Persona consultante |
| Figura gris/sombreada | Integrante fallecido |
| △ con X | Aborto espontáneo |
| △ relleno ● | Aborto provocado |

**Líneas de unión:**
| Línea | Significado |
|-------|-------------|
| `===` Doble línea continua | Matrimonio formal |
| `—` Línea simple continua | Convivencia / Pareja de hecho |
| `= / =` Línea cortada | Separación o divorcio |

**Línea vertical desde el centro de la unión hacia abajo** une a los hijos. Los hijos se ordenan de izquierda a derecha, del mayor al menor.

### 12.2 El Ecomapa

El ecomapa visualiza la relación de la familia con su entorno social e institucional. Usa un motor radial (neato) que coloca a la familia en el centro y los nodos institucionales alrededor.

**Tipos de vínculos:**

| Línea | Significado |
|-------|-------------|
| Línea gruesa y continua | Vínculo positivo, fuerte o recíproco |
| Línea punteada | Vínculo débil o prácticamente inexistente |
| Línea quebrada/zigzag roja | Vínculo estresante, conflictivo o roto |

Los nodos del ecomapa representan instituciones o redes: CESFAM, colegio, trabajo, iglesia, familia extensa, servicios sociales, etc.

### 12.3 Descargar los Gráficos

Los gráficos se pueden visualizar directamente en la plataforma. Para incluirlos en el PDF, use la opción de **"Generar Informe PDF"** que los incorpora automáticamente.

---

## 13. Dashboard Analítico — Estadísticas y Reportes

El dashboard muestra estadísticas en tiempo real sobre las evaluaciones registradas.

### 13.1 Acceso
Haga clic en la pestaña **"📊 Dashboard Analítico"** en el área principal.

### 13.2 KPIs Principales (Tarjetas Métricas)

En la parte superior del dashboard verá 4 tarjetas con los indicadores principales:
- **Total Evaluaciones**: Número total de familias evaluadas
- **Riesgo Alto 🔴**: Número y porcentaje de familias en riesgo alto
- **Riesgo Medio 🟡**: Número y porcentaje de familias en riesgo medio
- **Riesgo Bajo 🟢**: Número y porcentaje de familias en riesgo bajo

### 13.3 Gráficos Disponibles

| Gráfico | Descripción |
|---------|-------------|
| **Distribución de Riesgo (Donut)** | Proporción de familias por nivel |
| **Riesgo por Sector** | Comparativa Sol (Urbano) vs Luna (Rural) |
| **Riesgo por Establecimiento** | Comparativa por Posta/EMR (Encargados Postas) |
| **Top 12 Factores de Riesgo** | Factores más frecuentes en la población |
| **Brecha de Intervención** | Familias con vs sin plan de intervención |
| **Histograma de Puntajes** | Distribución de puntajes con zonas de color |
| **Evolución Temporal** | Número de evaluaciones por mes |
| **Puntaje por Programa** | Puntaje promedio según unidad/programa CESFAM |

> 📌 Los datos del dashboard se actualizan con una caché de máximo 5 minutos. Use el botón "Actualizar Dashboard" si necesita datos más recientes.

### 13.4 Filtro por Establecimiento

Los Encargados de Postas pueden filtrar todos los gráficos por un establecimiento específico usando el selector disponible en el sidebar.

---

## 14. Descarga de Documentos PDF

La plataforma genera dos tipos de documentos PDF:

### 14.1 Ficha PDF Completa (Evaluación Llena)

Contiene todos los datos de la evaluación registrada:
- Datos básicos de la familia e identificación
- Composición del grupo familiar
- Factores de riesgo chequeados con el resultado calculado
- APGAR Familiar con puntaje e interpretación
- Genograma (imagen generada automáticamente)
- Ecomapa
- Plan de intervención completo con actividades y responsables
- Firmas del compromiso intervencional
- Análisis clínico narrativo

**Cómo obtenerlo:**
1. Cargue la evaluación deseada
2. Presione el botón **"📄 Descargar Informe PDF"**
3. El archivo se descarga automáticamente

### 14.2 Pauta en Blanco (Para Terreno)

PDF con los campos vacíos para llenar a mano en visitas domiciliarias sin internet:
- Todos los campos del formulario en blanco
- Espacio cuadriculado para dibujar el genograma
- Espacio para el ecomapa
- Leyenda explicativa de los símbolos del genograma
- Tabla de factores de riesgo para marcar con lápiz
- Espacio para el APGAR y plan de intervención

**Cómo obtenerlo:**
1. Presione **"📄 Descargar Pauta en Blanco"** en la barra lateral
2. El PDF se descarga inmediatamente sin necesidad de cargar ninguna evaluación

---

## 15. Reporte REM-P7 (Jefaturas y Encargados)

### 15.1 ¿Qué es el REM-P7?

El **REM-P7** es el Resumen Estadístico Mensual oficial del MINSAL para el componente "Familias en Control Salud Familiar". Reporta el estado de las familias evaluadas según nivel de riesgo, sector e intervención.

### 15.2 ¿Quién puede generar el REM-P7?
Solo tienen acceso los siguientes roles:
- Programador/Desarrollador
- Encargado/a MAIS
- Jefe/a de Sector

### 15.3 Cómo generar el REM-P7

1. Acceda a la sección **"REM-P7"** o busque el botón correspondiente
2. Ingrese el **número de familias inscritas** del Sector Sol y del Sector Luna
3. Presione **"Generar REM-P7"**
4. Descargue el archivo Excel con formato oficial

### 15.4 Contenido del REM-P7 generado

El Excel generado incluye las siguientes secciones:

**Sección A — Familias Urbanas (Sector Sol):**
- N° Familias inscritas
- N° Familias evaluadas
- N° Familias por nivel de riesgo (Bajo / Medio / Alto)

**Sección A.1 — Familias Rurales (Sector Luna):**
- Misma estructura que Sección A pero para el sector rural

**Sección B — Intervención Urbana y Rural:**
- N° Familias con plan de intervención
- N° Familias sin plan por nivel de riesgo
- N° Familias egresadas con tipo de egreso

**Para Encargados de Postas:** El Excel incluye hojas adicionales por cada establecimiento rural (cada Posta/EMR), permitiendo el reporte desagregado.

---

## 16. Uso Offline — Pauta en Blanco para Terreno

Cuando deba visitar domicilios o Postas sin conexión a internet, use la **Pauta en Blanco**.

### 16.1 Antes de salir al terreno

1. Acceda a la plataforma con conexión a internet
2. Descargue la Pauta en Blanco (ver Sección 14.2)
3. Imprima tantas copias como visitas planifique + algunas extra

### 16.2 En el domicilio (llenado en papel)

**Dibujo del Genograma:**

1. **Hombres/Masculinos**: Cuadrado `[ ]`
2. **Mujeres/Femeninas**: Círculo `( )`
3. **Identidades diversas**: Rombo/Diamante `◇`
4. **Matrimonios**: Línea continua por debajo y entre ambos, con línea vertical hacia los hijos
5. **Convivencia**: Misma línea pero simple
6. **Separaciones**: Corte en la línea con `//`
7. **Gestaciones**: Triángulo colgando; con `X` interior si fue aborto espontáneo; pintado si fue inducido
8. **Enfermedades crónicas**: Marque el contorno con lápiz rojo o sombree el borde
9. **Caso índice**: Doble pared `[[ ]]` o `(( ))`
10. **Fallecidos**: Gran "X" sobre toda la figura; fecha de muerte y causa fuera de la figura
11. **Convivientes activos**: Línea punteada `- - -` encerrando solo a quienes viven bajo el mismo techo

**Aplicación del APGAR:**
- Realice las 5 preguntas directamente al caso índice
- Anote la puntuación (0, 1 o 2) para cada pregunta
- Sume y encuadre el total

**Plan de intervención:**
- Pacte directamente con la familia las actividades comprometidas
- Registre actividad, responsable y fecha límite
- Obtenga firmas a tinta al final

---

## 17. Digitación desde Pauta en Papel

Al regresar al CESFAM con la pauta resuelta, siga este proceso para traspasar los datos al sistema:

1. **Presione "➕ Nueva Ficha"** en la barra lateral
2. **Complete Datos Básicos** exactamente como están en el papel
3. **Ingrese el Grupo Familiar**: agregue una fila por cada persona anotada en el papel
   - Use los mismos datos de nombre, RUT, fecha de nacimiento, etc.
   - Seleccione la identidad de género equivalente
   - Para fallecidos: ingrese "F" en E. Civil
4. **Marque los factores de riesgo**: use los mismos checkboxes que marcó en el papel
5. **Ingrese el APGAR**: digiti las puntuaciones de cada pregunta (0, 1 o 2)
6. **Registre el Plan de Intervención**: una fila por cada actividad comprometida
7. **Ingrese las firmas**: escriba los nombres de quienes firmaron en papel
8. **Presione "💾 Guardar Evaluación"**

> ⚠️ **Importante**: Al digitizar, la plataforma asignará un nuevo ID. El ID del papel y el del sistema coincidirán si ya existía un registro previo de esa familia. Si es una familia nueva, el ID se genera automáticamente.

---

## 18. Preguntas Frecuentes (FAQ)

**P: ¿Puedo editar una evaluación ya guardada?**
R: Sí. Cargue la evaluación usando su ID en la búsqueda directa y modifique los campos que necesite. Al guardar, el sistema actualizará el registro existente.

**P: ¿Por qué no veo las evaluaciones de otro sector?**
R: El sistema aplica control de acceso por sector (RBAC). Usted solo puede ver las evaluaciones de su sector o unidad asignada. Esto es intencional para proteger la confidencialidad de la información.

**P: ¿Qué pasa si el internet se cae mientras guardo?**
R: Si la conexión falla durante el guardado, el sistema mostrará un mensaje de error. Los datos en pantalla NO se pierden, permanecen visibles. Reinténtelo cuando se restablezca la conexión.

**P: ¿El genograma se actualiza automáticamente?**
R: Sí. Cada vez que modifica datos en la tabla del Grupo Familiar, el genograma se regenera automáticamente en tiempo real.

**P: ¿Puedo tener múltiples evaluaciones para la misma familia?**
R: Sí, pero cada una tendrá un ID diferente. El sistema detecta si un RUT ya existe y le advierte de evaluaciones previas, pero no impide crear una nueva.

**P: ¿Con qué frecuencia debo actualizar la evaluación?**
R: Se recomienda actualizar la evaluación cada vez que se realice una visita de seguimiento o haya cambios significativos en la situación familiar.

**P: ¿Puedo imprimir el dashboard?**
R: No directamente. Para reportes formales, use el reporte REM-P7 (roles autorizados) o la exportación PDF.

**P: ¿Los datos en la plataforma son confidenciales?**
R: Sí. Los datos se almacenan en Google Sheets con autenticación mediante cuenta de servicio privada. El acceso está restringido por rol y sector. La plataforma registra en un log de auditoría cada acción realizada.

---

## 19. Soporte y Contacto Técnico

Para problemas técnicos, dudas o solicitudes de nuevas funcionalidades:

- **Primer nivel**: Consulte a su Jefe/a de Sector o Encargado/a MAIS
- **Segundo nivel**: Contacte al administrador del sistema (Programador)
- **Registro de acceso nuevo**: Para agregar nuevos usuarios al sistema, contacte al Programador o Encargado MAIS con los datos: nombre completo, RUT, cargo y sector/unidad

> 🔒 **Seguridad**: Nunca comparta su contraseña con otros funcionarios. Cada funcionario debe tener sus propias credenciales.

---

*Manual de Usuario v3.0 — Plataforma MAIS — CESFAM Cholchol*  
*Generado con la asistencia tecnológica del ecosistema Antigravity*
