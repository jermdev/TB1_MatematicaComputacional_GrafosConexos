import streamlit as st


def render_controles(orquestador=None, paso_atras: callable = None, paso_adelante: callable = None):
    """
    Renderiza los controles de la interfaz de usuario para configurar,
    generar y manipular el grafo, así como navegar por los pasos del algoritmo.
    Retorna un diccionario con todos los valores capturados.
    """
    st.subheader("⚙️ Controles")

    num_vert_default = getattr(orquestador, "num_vertices", 4) if orquestador else 4
    modo_default = getattr(orquestador, "modo", "Automático") if orquestador else "Automático"
    algoritmo_default = getattr(orquestador, "algoritmo_seleccionado", "DFS") if orquestador else "DFS"

    with st.container(border=True):
        st.markdown("**Configuración del grafo**")
        num_vertices = st.number_input(
            "Número de vértices",
            min_value=4,
            max_value=12,
            value=int(num_vert_default),
            step=1,
            key="input_num_vertices",
        )

        modo = st.radio(
            "Modo de generación",
            ["Automático", "Manual"],
            index=0 if modo_default == "Automático" else 1,
            horizontal=True,
            key="radio_modo_generacion",
        )

        densidad = 35
        if modo == "Automático":
            densidad = st.slider(
                "Densidad de aristas (%)",
                min_value=10,
                max_value=90,
                value=35,
                step=5,
                help="Probabilidad de conexión entre pares de vértices",
                key="slider_densidad",
            )
        else:
            st.caption("ℹ️ En **Modo Manual**, genera los vértices y luego añade conexiones interactivamente.")

    with st.container(border=True):
        st.markdown("**Algoritmo de análisis**")
        opciones_alg = ["DFS", "BFS", "Union-Find"]
        idx_alg = opciones_alg.index(algoritmo_default) if algoritmo_default in opciones_alg else 0
        algoritmo = st.selectbox(
            "Seleccionar algoritmo",
            opciones_alg,
            index=idx_alg,
            key="select_algoritmo",
        )

    with st.container(border=True):
        generar = st.button("🚀 Generar grafo", use_container_width=True, type="primary", key="btn_generar_grafo")

    # Panel de conexión manual (si estamos en modo manual y hay vértices disponibles)
    origen_manual = None
    destino_manual = None
    conectar_manual = False
    cancelar_manual = False
    limpiar_manual = False

    if modo == "Manual" and orquestador and orquestador.grafo and len(orquestador.grafo.vertices) >= 2:
        with st.container(border=True):
            st.markdown("**🔗 Agregar conexión manual**")
            vertices = orquestador.grafo.vertices
            opciones = {v.id: f"{v.etiqueta or v.id} (ID: {v.id})" for v in vertices}
            ids = list(opciones.keys())

            c_orig, c_dest = st.columns(2)
            origen_manual = c_orig.selectbox(
                "Origen",
                options=ids,
                format_func=lambda x: opciones[x],
                index=0,
                key="manual_sel_origen",
            )
            def_dest_idx = 1 if len(ids) > 1 else 0
            destino_manual = c_dest.selectbox(
                "Destino",
                options=ids,
                format_func=lambda x: opciones[x],
                index=def_dest_idx,
                key="manual_sel_destino",
            )

            # Validar relación entre los vértices seleccionados
            es_mismo_vertice = (origen_manual == destino_manual)
            conexion_ya_existe = orquestador.existe_conexion(origen_manual, destino_manual)

            etiq_origen = orquestador.obtener_etiqueta_vertice(origen_manual)
            etiq_destino = orquestador.obtener_etiqueta_vertice(destino_manual)

            if es_mismo_vertice:
                st.info("ℹ️ Selecciona dos vértices diferentes para conectar.")
            elif conexion_ya_existe:
                st.warning(f"⚠️ Ya existe una conexión entre **{etiq_origen}** y **{etiq_destino}**.")
            else:
                st.success(f"✨ Listo para conectar **{etiq_origen}** con **{etiq_destino}**.")

            c_btn_conn, c_btn_cancel, c_btn_clear = st.columns([1.2, 1.2, 1])
            conectar_manual = c_btn_conn.button(
                "➕ Conectar",
                use_container_width=True,
                disabled=(es_mismo_vertice or conexion_ya_existe),
                key="btn_conectar_manual",
                type="primary",
            )
            cancelar_manual = c_btn_cancel.button(
                "❌ Cancelar",
                use_container_width=True,
                disabled=(not orquestador.grafo.aristas),
                key="btn_cancelar_manual",
                help="Cancela la conexión entre los vértices seleccionados o la última generada",
            )
            limpiar_manual = c_btn_clear.button(
                "🗑️ Limpiar",
                use_container_width=True,
                disabled=(not orquestador.grafo.aristas),
                key="btn_limpiar_manual",
                help="Elimina todas las conexiones",
            )

            if orquestador.grafo.aristas:
                st.caption(f"Aristas actuales ({len(orquestador.grafo.aristas)}):")
                lista_aristas = [
                    f"{orquestador.obtener_etiqueta_vertice(a.origen)} ↔ {orquestador.obtener_etiqueta_vertice(a.destino)}"
                    for a in orquestador.grafo.aristas
                ]
                st.write(", ".join(lista_aristas))

    with st.container(border=True):
        st.markdown("**Ejecución paso a paso**")
        paso_actual = getattr(orquestador, "paso_actual", 0) if orquestador else 0
        total_pasos = len(getattr(orquestador, "pasos", [])) if orquestador else 1

        c1, c2 = st.columns(2)
        c1.button(
            "⬅ Anterior",
            on_click=paso_atras,
            use_container_width=True,
            disabled=(paso_actual <= 0),
            key="btn_paso_atras",
        )
        c2.button(
            "Siguiente ➡",
            on_click=paso_adelante,
            use_container_width=True,
            disabled=(paso_actual >= total_pasos - 1),
            key="btn_paso_adelante",
        )

    return {
        "num_vertices": int(num_vertices),
        "modo": modo,
        "algoritmo": algoritmo,
        "densidad": float(densidad) / 100.0,
        "generar": generar,
        "origen_manual": origen_manual,
        "destino_manual": destino_manual,
        "conectar_manual": conectar_manual,
        "cancelar_manual": cancelar_manual,
        "limpiar_manual": limpiar_manual,
    }