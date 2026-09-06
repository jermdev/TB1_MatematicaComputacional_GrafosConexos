import streamlit as st


def render_controles(paso_atras: callable, paso_adelante: callable):
    st.subheader("Controles")

    with st.container(border=True):
            st.markdown("**Datos del grafo**")
            num_vertices = st.number_input("Número de vértices", min_value=1, step=1)
    
            st.markdown("**Modo de generación**")
            modo = st.radio("Modo", ["Manual", "Automático"], horizontal=True, label_visibility="collapsed")

    with st.container(border=True):
        st.markdown("**Algoritmo**")
        algoritmo = st.selectbox("Seleccionar algoritmo", ["DFS", "BFS", "Union-Find"])

    with st.container(border=True):
        generar = st.button("Generar grafo", use_container_width=True)

    with st.container(border=True):
            st.markdown("**Ejecución paso a paso**")
            c1, c2 = st.columns(2)
            c1.button("⬅ Anterior", on_click=paso_atras, use_container_width=True)
            c2.button("Siguiente ➡", on_click=paso_adelante, use_container_width=True)

    return {
          "modo" : modo,
          "num_vertices" : num_vertices,
          "algoritmo" : algoritmo
    }