import os

def cargar_archivo(ruta_relativa):
    directorio_base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    ruta_absoluta = os.path.join(directorio_base, ruta_relativa)

    with open(ruta_absoluta, "r", encoding="utf-8") as f:
        return f.read()