import streamlit as st
import pyvis as pv

#utilizar la clase generada de grafo  para renderizar el grafo en el canvas

def grafo_canva():
    st.subheader("Grafo")
    with st.container(height=600, border=True):
        # Aqui va tu render del grafo. Opciones:
        # - streamlit_agraph.agraph(nodes=..., edges=..., config=...)
        # - pyvis -> generar html y mostrarlo con components.html
        # - networkx + matplotlib -> st.pyplot(fig)
        # - plotly -> st.plotly_chart(fig, use_container_width=True)
        net = pv.network.Network()
        net.add_node(1, label="A")
        net.add_node(2, label="B")
        net.add_node(3, label="C")
        net.add_node(4, label="D")
        net.add_edge(1, 2)
        net.add_edge(2, 3)
        net.add_edge(3, 4)
        net.add_edge(4, 1)
        net.repulsion(node_distance=200, spring_length=200)

        st.components.v1.html(net.generate_html(), height=600, scrolling=True)