
import sys
try:
    import pypdf
    reader = pypdf.PdfReader("d:/PROYECTOS PROGRAMACIÓN/ANTIGRAVITY_PROJECTS/encuesta_riesgo/PROTOCOLO INTERVENCION Y  VDI SJ.pdf")
    text = ""
    for i, page in enumerate(reader.pages):
        text += f"--- PAGE {i+1} ---\n"
        text += page.extract_text() + "\n"
    
    # Save to a text file for easier searching
    with open("d:/PROYECTOS PROGRAMACIÓN/ANTIGRAVITY_PROJECTS/encuesta_riesgo/protocolo_text.txt", "w", encoding="utf-8") as f:
        f.write(text)
    
    print(f"Extracted {len(text)} characters. First 2000 chars:\n")
    print(text[:2000])
except Exception as e:
    print(f"Error: {e}")
