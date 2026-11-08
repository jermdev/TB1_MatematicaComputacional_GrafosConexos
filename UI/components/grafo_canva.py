import json
import pandas as pd
import pyvis as pv
import streamlit as st
from domain.Entidades.grafo import Grafo


def grafo_canva(
    grafo, 
    vista: str = "grafo", 
    modo_manual: bool = False, 
    paso_actual=0, 
    pasos_algoritmo=None, 
    componentes_conexas=None, 
    grafo_id="default", 
    fuertemente=True,
    orquestador=None
):
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
            mostrar_grafo(
                grafo,
                modo_manual=modo_manual,
                paso_actual=paso_actual,
                pasos_algoritmo=pasos_algoritmo or [],
                componentes_conexas=componentes_conexas or [],
                grafo_id=grafo_id,
                fuertemente=fuertemente,
            )
        elif vista == "ambos":
            c1, c2 = st.columns(2)
            with c1:
                st.markdown("**Representación visual**")
                mostrar_grafo(
                    grafo,
                    modo_manual=modo_manual,
                    paso_actual=paso_actual,
                    pasos_algoritmo=pasos_algoritmo or [],
                    componentes_conexas=componentes_conexas or [],
                    grafo_id=grafo_id,
                    fuertemente=fuertemente,
                )
            with c2:
                st.markdown("**Matriz de adyacencia**")
                mostrar_matriz(grafo)


def mostrar_matriz(grafo: Grafo, orquestador=None):
    """
    Renderiza la matriz del grafo. Si el algoritmo seleccionado es Harary,
    muestra la matriz correspondiente al paso actual (caminos, permutaciones, etc.).
    """
    matriz = []
    etiquetas_filas = []
    etiquetas_columnas = []
    
    # 1. Verificar si estamos usando Harary y si hay un orquestador activo
    if orquestador and orquestador.algoritmo_seleccionado == "Harary":
        harary_srv = orquestador.obtener_harary_service()
        paso = harary_srv.obtener_paso(orquestador.paso_actual)
        
        if paso and hasattr(paso, 'matriz') and paso.matriz:
            matriz = paso.matriz
            etiquetas_filas = paso.etiquetas_filas
            etiquetas_columnas = paso.etiquetas_columnas
            st.markdown(f"##### 🔢 {paso.titulo}")
            st.caption(paso.descripcion)

    # 2. Si no es Harary (o falló), usar la matriz de adyacencia clásica
    if not matriz:
        matriz = grafo.get_matriz()
        vertices = grafo.vertices
        etiquetas = [f"{v.etiqueta or v.id} ({v.id})" for v in vertices]
        etiquetas_filas = etiquetas
        etiquetas_columnas = etiquetas
        st.markdown("##### 🔢 Matriz de Adyacencia")

    # Mapear métricas generales
    num_v = len(grafo.vertices)
    num_e = len(grafo.aristas)
    tipo_str = "Dirigido" if grafo.dirigido else "No dirigido"

    m1, m2, m3 = st.columns(3)
    m1.metric("Vértices (|V|)", num_v)
    m2.metric("Aristas (|E|)", num_e)
    m3.metric("Tipo", tipo_str)

    # Renderizar el DataFrame
    df = pd.DataFrame(matriz, index=etiquetas_filas, columns=etiquetas_columnas)
    st.dataframe(df, use_container_width=True, height=400)


def _definir_color_nodo(
    vertice_id: str,
    paso_actual: int | None,
    pasos_algoritmo: list,
    componentes_conexas: list[list[str]],
) -> dict:
    default_color = {
        "background": "#dbeafe",
        "border": "#2563eb",
        "highlight": {"background": "#fbbf24", "border": "#d97706"},
        "hover": {"background": "#bfdbfe", "border": "#1d4ed8"},
    }

    if not pasos_algoritmo or paso_actual is None:
        return default_color

    ultimo_paso = len(pasos_algoritmo) - 1
    if paso_actual >= 0 and paso_actual == ultimo_paso and componentes_conexas:
        palette = [
            ("#a7f3d0", "#166534"),
            ("#bfdbfe", "#1d4ed8"),
            ("#fde68a", "#92400e"),
            ("#fbcfe8", "#9d174d"),
            ("#c7d2fe", "#3730a3"),
            ("#fed7aa", "#9a4d00"),
            ("#99f6e4", "#115e59"),
            ("#fecdd3", "#9f1239"),
            ("#d9f99d", "#3f6212"),
            ("#ddd6fe", "#5b21b6"),
            ("#fed7aa", "#c2410c"),
            ("#f5d0fe", "#86198f"),
        ]

        for idx, componente in enumerate(componentes_conexas):
            if str(vertice_id) in [str(c) for c in componente]:
                bg, border = palette[idx % len(palette)]
                return {
                    "background": bg,
                    "border": border,
                    "highlight": {"background": "#f59e0b", "border": "#b45309"},
                    "hover": {"background": bg, "border": border},
                }

    if not (0 <= paso_actual < len(pasos_algoritmo)):
        return default_color

    paso = pasos_algoritmo[paso_actual]
    visitados = set(str(v) for v in getattr(paso, "visitados", set()))
    if getattr(paso, "nodo_actual", None) is not None:
        visitados.add(str(paso.nodo_actual))

    if str(vertice_id) in visitados:
        return {
            "background": "#fbbf24",
            "border": "#d97706",
            "highlight": {"background": "#f59e0b", "border": "#b45309"},
            "hover": {"background": "#fcd34d", "border": "#d97706"},
        }

    return default_color


def mostrar_grafo(
    grafo: Grafo,
    modo_manual: bool = False,
    paso_actual: int | None = None,
    pasos_algoritmo: list | None = None,
    componentes_conexas: list[list[str]] | None = None,
    grafo_id: str = "default",
    fuertemente: bool = True,
):
    """
    Renderiza el grafo interactivo con Pyvis.
    En modo manual, activa la barra de herramientas de manipulación táctil/interactiva de vis.js.
    """
    if modo_manual:
        st.caption(
            "💡 **Interacción activa:** Agrega conexiones desde el panel lateral derecho "
            "o usa las herramientas interactivas del lienzo."
        )
    elif (
        grafo.dirigido
        and paso_actual is not None
        and pasos_algoritmo
        and paso_actual == len(pasos_algoritmo) - 1
        and componentes_conexas
    ):
        tipo_coloreado = (
            "Componentes Fuertemente Conexas"
            if fuertemente
            else "Componentes Débilmente Conexas"
        )
        st.caption(f"🎨 **Coloreado final (Grafo Dirigido):** {tipo_coloreado}")

    net = pv.network.Network(
        height="500px",
        width="100%",
        directed=grafo.dirigido,
        notebook=False,
        cdn_resources="remote",
    )

    smooth_edges = (
        {"enabled": True, "type": "curvedCW", "roundness": 0.16}
        if grafo.dirigido
        else {"type": "continuous"}
    )

    opciones = {
        "nodes": {
            "font": {"size": 15, "color": "#0f172a", "face": "sans-serif"},
            "color": {
                "background": "#dbeafe",
                "border": "#2563eb",
                "highlight": {"background": "#fbbf24", "border": "#d97706"},
                "hover": {"background": "#bfdbfe", "border": "#1d4ed8"},
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
            "smooth": smooth_edges,
            "width": 2.5,
        },
        "physics": {
            "enabled": True,
            "solver": "forceAtlas2Based",
            "forceAtlas2Based": {
                "gravitationalConstant": -150,
                "centralGravity": 0.01,
                "springLength": 250,
                "springConstant": 0.05,
                "damping": 0.4,
            },
            "stabilization": {"iterations": 200},
        },
        "interaction": {
            "hover": True,
            "navigationButtons": True,
            "keyboard": False,
            "zoomView": True,
            "dragView": True,
            "dragNodes": True,
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

    net.options = opciones

    for vertice in grafo.vertices:
        etiqueta = vertice.etiqueta or vertice.id
        tooltip = f"Vértice: {etiqueta} | ID: {vertice.id}"
        if (
            paso_actual is not None
            and pasos_algoritmo
            and paso_actual == len(pasos_algoritmo) - 1
            and componentes_conexas
        ):
            for idx, comp in enumerate(componentes_conexas, start=1):
                if str(vertice.id) in [str(c) for c in comp]:
                    if grafo.dirigido:
                        pref = "Comp. Fuerte" if fuertemente else "Comp. Débil"
                        tooltip += f" | {pref} {idx}"
                    else:
                        tooltip += f" | Componente {idx}"
                    break

        estilo_nodo = _definir_color_nodo(
            vertice.id,
            paso_actual=paso_actual,
            pasos_algoritmo=pasos_algoritmo or [],
            componentes_conexas=componentes_conexas or [],
        )
        net.add_node(
            vertice.id,
            label=etiqueta,
            title=tooltip,
            color=estilo_nodo,
            font={"color": "#0f172a", "size": 15},
            size=26,
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

    target_init = "network = new vis.Network(container, data, options);"
    if target_init in html_content:
        js_persistencia = f"""
        // --- CONTROL DE PERSISTENCIA DE POSICIONES DE VÉRTICES ---
        var GRAFO_ID = "{grafo_id}";
        var STORAGE_KEY = "grafo_posiciones_" + GRAFO_ID;

        function guardarEstado(posiciones, viewPos, scale) {{
            try {{
                var payload = JSON.stringify({{
                    positions: posiciones,
                    viewPosition: viewPos,
                    scale: scale
                }});
                try {{ if (window.parent && window.parent.sessionStorage) window.parent.sessionStorage.setItem(STORAGE_KEY, payload); }} catch(e){{}}
                try {{ if (window.parent && window.parent.localStorage) window.parent.localStorage.setItem(STORAGE_KEY, payload); }} catch(e){{}}
                try {{ sessionStorage.setItem(STORAGE_KEY, payload); }} catch(e){{}}
                try {{ localStorage.setItem(STORAGE_KEY, payload); }} catch(e){{}}
            }} catch(err) {{
                console.warn("Error guardando posiciones:", err);
            }}
        }}

        function cargarEstado() {{
            var raw = null;
            try {{ if (window.parent && window.parent.sessionStorage) raw = window.parent.sessionStorage.getItem(STORAGE_KEY); }} catch(e){{}}
            if (!raw) {{ try {{ if (window.parent && window.parent.localStorage) raw = window.parent.localStorage.getItem(STORAGE_KEY); }} catch(e){{}} }}
            if (!raw) {{ try {{ raw = sessionStorage.getItem(STORAGE_KEY); }} catch(e){{}} }}
            if (!raw) {{ try {{ raw = localStorage.getItem(STORAGE_KEY); }} catch(e){{}} }}
            if (raw) {{
                try {{
                    return JSON.parse(raw);
                }} catch(e) {{
                    return null;
                }}
            }}
            return null;
        }}

        // Limpieza de claves viejas de otros grafos
        try {{
            var storageList = [];
            try {{ if (window.parent && window.parent.localStorage) storageList.push(window.parent.localStorage); }} catch(e){{}}
            try {{ if (window.parent && window.parent.sessionStorage) storageList.push(window.parent.sessionStorage); }} catch(e){{}}
            try {{ storageList.push(localStorage); }} catch(e){{}}
            try {{ storageList.push(sessionStorage); }} catch(e){{}}

            storageList.forEach(function(store) {{
                for (var i = store.length - 1; i >= 0; i--) {{
                    var k = store.key(i);
                    if (k && k.indexOf("grafo_posiciones_") === 0 && k !== STORAGE_KEY) {{
                        store.removeItem(k);
                    }}
                }}
            }});
        }} catch(e) {{}}

        var savedState = cargarEstado();

        if (savedState && savedState.positions) {{
            // Aplicar las posiciones guardadas a los vértices antes de renderizar
            var updates = [];
            nodes.forEach(function(item) {{
                if (savedState.positions[item.id]) {{
                    updates.push({{
                        id: item.id,
                        x: savedState.positions[item.id].x,
                        y: savedState.positions[item.id].y
                    }});
                }}
            }});
            if (updates.length > 0) {{
                nodes.update(updates);
            }}
            // Desactivar física para congelar la posición de los vértices al avanzar o retroceder paso
            options.physics = {{ enabled: false }};
        }}

        network = new vis.Network(container, data, options);

        if (!savedState || !savedState.positions) {{
            // Grafo recién generado: registrar posiciones tras estabilización física
            function registrarPosicionesIniciales() {{
                try {{
                    var pos = network.getPositions();
                    var viewPos = network.getViewPosition();
                    var scale = network.getScale();
                    if (pos && Object.keys(pos).length > 0) {{
                        guardarEstado(pos, viewPos, scale);
                        network.setOptions({{ physics: {{ enabled: false }} }});
                    }}
                }} catch(e) {{}}
            }}

            setTimeout(registrarPosicionesIniciales, 150);

            network.once("stabilizationIterationsDone", function() {{
                registrarPosicionesIniciales();
            }});
            network.once("stabilized", function() {{
                registrarPosicionesIniciales();
            }});
        }} else {{
            // Restaurar cámara / zoom si existe
            if (savedState.viewPosition && typeof savedState.scale === "number") {{
                network.moveTo({{
                    position: savedState.viewPosition,
                    scale: savedState.scale,
                    animation: false
                }});
            }}
        }}

        // Guardar posiciones tras terminar de arrastrar vértices en pantalla
        network.on("dragEnd", function(params) {{
            try {{
                var pos = network.getPositions();
                var viewPos = network.getViewPosition();
                var scale = network.getScale();
                guardarEstado(pos, viewPos, scale);
            }} catch(e) {{}}
        }});

        // Guardar también si el usuario hizo zoom o paneo
        network.on("zoom", function() {{
            try {{
                var pos = network.getPositions();
                var viewPos = network.getViewPosition();
                var scale = network.getScale();
                guardarEstado(pos, viewPos, scale);
            }} catch(e) {{}}
        }});
        """
        html_content = html_content.replace(target_init, js_persistencia, 1)

    st.components.v1.html(html_content, height=520, scrolling=False)