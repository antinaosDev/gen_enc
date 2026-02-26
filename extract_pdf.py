
import sys
try:
    import pypdf
    reader = pypdf.PdfReader("d:/PROYECTOS PROGRAMACIÓN/ANTIGRAVITY_PROJECTS/encuesta_riesgo/Gu_a_Taller_Instrumentos_de_Familia.pdf")
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    print(text[:5000]) # Print first 5000 chars
except Exception as e:
    print(f"Error: {e}")
