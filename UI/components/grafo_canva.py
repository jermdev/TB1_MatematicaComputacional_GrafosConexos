import streamlit as st
import pyvis as pv
import pandas as pd
from domain.grafo import Grafo

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

def grafo_canva(grafo: Grafo, vista="matriz"):
    st.subheader("Visualizacion del grafo")

    with st.container(height=600, border=True):
        if vista == "matriz":
            mostrar_matriz(grafo)

        elif vista == "grafo":
            mostrar_grafo(grafo)

        elif vista == "ambos":
            mostrar_matriz(grafo)
            mostrar_grafo(grafo)


def mostrar_matriz(grafo: Grafo):
    matriz = grafo.get_matriz()

def mostrar_grafo(grafo: Grafo):
    net = pv.network.Network(directed=grafo.dirigido)

    for vertice in grafo.vertices:
        etiqueta = vertice.etiqueta or vertice.id

        net.add_node(vertice.id, label=etiqueta)

    for arista in grafo.aristas:
        es_dirigida = arista.dirigida or grafo.dirigido

        net.add_edge(
            arista.origen, 
            arista.destino,
            label=str(arista.peso)
            if arista.peso != 1
            else "",
            arros = "to"
            if es_dirigida
            else ""
            )

    net.repulsion(node_distance=200, spring_length=200)
    st.components.v1.html(net.generate_html(), height=600, scrolling=True)