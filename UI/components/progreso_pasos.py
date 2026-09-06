import streamlit as st

def progreso_pasos(pasos, paso_actual):
    """
    Renderiza el progreso de los pasos en la interfaz de usuario.
    
    Args:
        pasos (list): Lista de strings que representan los pasos.
        paso_actual (int): Índice del paso actual.
    """
    st.subheader("Paso a paso")
    with st.container(height=600, border=True):
        for i, texto in enumerate(pasos):
            if i == paso_actual:
                st.info(texto)  # resalta el paso activo
            else:
                st.write(texto)