import streamlit as st
from domain.paso_algoritmo import Paso_Algoritmo

def progreso_pasos(pasos, paso_actual):
    """
    Renderiza el progreso de los pasos en la interfaz de usuario.
    
    Args:
        pasos (list): Lista de pasos o mensajes de texto.
        paso_actual (int): Índice del paso activo.
    """
    st.subheader("Paso a paso")
    with st.container(height=600, border=True):
        for i, paso in enumerate(pasos):
            mensaje = paso.mensaje if isinstance(paso, Paso_Algoritmo) else str(paso)
            if i == paso_actual:
                st.info(mensaje)
            else:
                st.write(mensaje)