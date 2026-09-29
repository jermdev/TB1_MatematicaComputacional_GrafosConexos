import json
import pandas as pd
import pyvis as pv
import streamlit as st
from domain.grafo import Grafo


def grafo_canva(grafo: Grafo, vista: str = "grafo", modo_manual: bool = False):
    """
    Renderiza la visualización del grafo o su matriz de adyacencia según la vista elegida.
    """
    with st.container(height=620, border=True):
        if not grafo or len(grafo.vertices) == 0:
            st.info("ℹ️ No hay vértices en el grafo. Configura el número de vértices y haz clic en 'Generar grafo'.")
            return

        if vista == "matriz":
            mostrar_matriz(grafo)
        elif vista == "grafo":
            mostrar_grafo(grafo, modo_manual=modo_manual)
        elif vista == "ambos":
            c1, c2 = st.columns(2)
            with c1:
                st.markdown("**Representación visual**")
                mostrar_grafo(grafo, modo_manual=modo_manual)
            with c2:
                st.markdown("**Matriz de adyacencia**")
                mostrar_matriz(grafo)


def mostrar_matriz(grafo: Grafo):
    """
    Renderiza la matriz de adyacencia con información y métricas del grafo.
    """
    matriz = grafo.get_matriz()
    vertices = grafo.vertices
    etiquetas = [f"{v.etiqueta or v.id} ({v.id})" for v in vertices]

    num_v = len(vertices)
    num_e = len(grafo.aristas)
    tipo_str = "Dirigido" if grafo.dirigido else "No dirigido"

    m1, m2, m3 = st.columns(3)
    m1.metric("Vértices (|V|)", num_v)
    m2.metric("Aristas (|E|)", num_e)
    m3.metric("Tipo", tipo_str)

    st.markdown("##### 🔢 Matriz de Adyacencia")
    df = pd.DataFrame(matriz, index=etiquetas, columns=etiquetas)
    st.dataframe(df, use_container_width=True, height=400)


def mostrar_grafo(grafo: Grafo, modo_manual: bool = False):
    """
    Renderiza el grafo interactivo con Pyvis.
    En modo manual, activa la barra de herramientas de manipulación táctil/interactiva de vis.js.
    """
    if modo_manual:
        st.caption(
            "💡 **Interacción táctil / manual activa:** Pulsa **'Add Edge'** en la barra superior del lienzo "
            "y toca/arrastra entre dos vértices para conectarlos en pantalla."
        )

    net = pv.network.Network(
        height="500px",
        width="100%",
        directed=grafo.dirigido,
        notebook=False,
    )

    opciones = {
        "nodes": {
            "font": {"size": 15, "color": "#ffffff", "face": "sans-serif"},
            "color": {
                "background": "#2563eb",
                "border": "#1d4ed8",
                "highlight": {"background": "#f59e0b", "border": "#d97706"},
                "hover": {"background": "#3b82f6", "border": "#1e40af"},
            },
            "shape": "circle",
            "size": 26,
            "borderWidth": 2,
        },
        "edges": {
            "color": {
                "color": "#64748b",
                "highlight": "#f59e0b",
                "hover": "#0284c7",
            },
            "smooth": {"type": "continuous"},
            "width": 2.5,
        },
        "physics": {
            "enabled": True,
            "solver": "forceAtlas2Based",
            "forceAtlas2Based": {
                "gravitationalConstant": -45,
                "centralGravity": 0.01,
                "springLength": 120,
                "springConstant": 0.07,
                "damping": 0.4,
            },
            "stabilization": {"iterations": 100},
        },
        "interaction": {
            "hover": True,
            "navigationButtons": True,
            "keyboard": False,
            "zoomView": True,
            "dragView": True,
        },
    }

    if modo_manual:
        opciones["manipulation"] = {
            "enabled": True,
            "initiallyActive": True,
            "addNode": False,
            "addEdge": True,
            "editEdge": False,
            "deleteNode": False,
            "deleteEdge": True,
        }

    net.set_options(json.dumps(opciones))

    for vertice in grafo.vertices:
        etiqueta = vertice.etiqueta or vertice.id
        tooltip = f"Vértice: {etiqueta} | ID: {vertice.id}"
        net.add_node(
            vertice.id,
            label=etiqueta,
            title=tooltip,
        )

    for arista in grafo.aristas:
        es_dirigida = arista.dirigida or grafo.dirigido
        net.add_edge(
            arista.origen,
            arista.destino,
            label=str(arista.peso) if arista.peso != 1.0 else "",
            arrows="to" if es_dirigida else "",
        )

    html_content = net.generate_html()
    st.components.v1.html(html_content, height=520, scrolling=False)