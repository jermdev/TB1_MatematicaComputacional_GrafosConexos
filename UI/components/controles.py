import streamlit as st

#implementar los metodos para el control de interface de usuario

def render_controles(paso_atras: callable, paso_adelante: callable):
    st.subheader("Controles")

    with st.container(border=True):
        st.markdown("**Configuración del grafo**")
        num_vertices = st.number_input("Número de vértices", min_value=1, max_value=50, value=4, step=1)
        dirigido = st.checkbox("Grafo dirigido", value=False)
        vista = st.selectbox("Vista", ["ambos", "grafo", "matriz"], index=0)

        st.markdown("**Modo de generación**")
        modo = st.radio("Modo", ["Manual", "Automático"], horizontal=True, label_visibility="collapsed")

        conexiones_texto = ""
        if modo == "Manual":
            st.caption("Ingresa las conexiones (origen destino, una por línea):")
            conexiones_texto = st.text_area(
                "Conexiones",
                value="1 2\n2 3\n3 4\n4 1",
                height=110,
                help="Ejemplo: '1 2' o '1-2' para unir el vértice 1 con el vértice 2"
            )

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
        "modo": modo,
        "num_vertices": int(num_vertices),
        "dirigido": dirigido,
        "vista": vista,
        "algoritmo": algoritmo,
        "generar": generar,
        "conexiones_texto": conexiones_texto
    }