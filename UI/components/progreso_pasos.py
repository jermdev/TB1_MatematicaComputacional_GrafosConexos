import streamlit as st
from domain.Entidades.paso_algoritmo import Paso_Algoritmo


def progreso_pasos(
    pasos: list,
    paso_actual: int,
    componentes_conexas: list[list[str]] | None = None,
    obtener_etiqueta: callable | None = None,
):
    """
    Renderiza el progreso de los pasos en la interfaz de usuario y el desglose de componentes conexas.

    Args:
        pasos (list): Lista de pasos o mensajes de texto.
        paso_actual (int): Índice del paso activo.
        componentes_conexas (list[list[str]], optional): Lista de componentes conexas del grafo.
        obtener_etiqueta (callable, optional): Función para convertir ID de vértice en su etiqueta.
    """
    st.subheader("Paso a paso")
    with st.container(height=600, border=True):
        if not pasos:
            st.info("No hay pasos registrados para el grafo actual.")
        else:
            for i, paso in enumerate(pasos):
                mensaje = paso.mensaje if isinstance(paso, Paso_Algoritmo) else str(paso)
                prefijo = f"**Paso {i + 1}:** "
                if i == paso_actual:
                    st.info(f"{prefijo}{mensaje}")
                else:
                    st.write(f"{prefijo}{mensaje}")

        if componentes_conexas:
            st.divider()
            total_comp = len(componentes_conexas)
            if total_comp == 1:
                st.success("🟢 **Grafo Conexo** (1 componente)")
            else:
                st.warning(f"🟡 **Grafo Disconexo** ({total_comp} componentes conexas)")

            st.markdown("**Componentes Conexas:**")
            for idx, comp in enumerate(componentes_conexas, start=1):
                etiquetas = [
                    obtener_etiqueta(vid) if obtener_etiqueta else str(vid)
                    for vid in comp
                ]
                st.markdown(f"- **Componente {idx}:** `{'{' + ', '.join(etiquetas) + '}'}`")
