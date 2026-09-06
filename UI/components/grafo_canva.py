import streamlit as st

def grafo_canva():
    st.subheader("Grafo")
    with st.container(height=600, border=True):
        # Aqui va tu render del grafo. Opciones:
        # - streamlit_agraph.agraph(nodes=..., edges=..., config=...)
        # - pyvis -> generar html y mostrarlo con components.html
        # - networkx + matplotlib -> st.pyplot(fig)
        # - plotly -> st.plotly_chart(fig, use_container_width=True)
        st.write("Aquí se dibuja el grafo (placeholder)")