import streamlit as st
from domain.Entidades.paso_algoritmo import Paso_Algoritmo


def _formatear_lista_componentes(
    componentes: list[list[str]],
    obtener_etiqueta: callable | None = None,
    prefijo_item: str = "Componente",
):
    for idx, comp in enumerate(componentes, start=1):
        etiquetas = [
            obtener_etiqueta(vid) if obtener_etiqueta else str(vid)
            for vid in comp
        ]
        st.markdown(f"- **{prefijo_item} {idx}:** `{'{' + ', '.join(etiquetas) + '}'}`")


def progreso_pasos(
    pasos: list,
    paso_actual: int,
    componentes_conexas: list[list[str]] | None = None,
    obtener_etiqueta: callable | None = None,
    dirigido: bool = False,
    fuertemente: bool = True,
    componentes_fuertemente_conexas: list[list[str]] | None = None,
    componentes_debilmente_conexas: list[list[str]] | None = None,
):
    """
    Renderiza el progreso de los pasos en la interfaz de usuario y el desglose de componentes conexas
    (incluyendo conectividad fuerte con Kosaraju y conectividad débil para grafos dirigidos).
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

        if not dirigido:
            if componentes_conexas:
                st.divider()
                total_comp = len(componentes_conexas)
                if total_comp == 1:
                    st.success("🟢 **Grafo Conexo** (1 componente)")
                else:
                    st.warning(f"🟡 **Grafo Disconexo** ({total_comp} componentes conexas)")

                st.markdown("**Componentes Conexas:**")
                _formatear_lista_componentes(componentes_conexas, obtener_etiqueta, "Componente")
        else:
            st.divider()
            st.markdown("#### 🧭 Análisis de Grafo Dirigido")

            if componentes_fuertemente_conexas:
                total_fuertes = len(componentes_fuertemente_conexas)
                total_debiles = len(componentes_debilmente_conexas or [])

                if total_fuertes == 1:
                    st.success("🟢 **Fuertemente Conexo** (1 componente fuerte)")
                elif total_debiles == 1:
                    st.info(
                        f"🔵 **Débilmente Conexo** (1 componente débil | {total_fuertes} componentes fuertes)"
                    )
                else:
                    st.warning(
                        f"🟡 **Grafo Disconexo** ({total_debiles} componentes débiles | {total_fuertes} fuertes)"
                    )

                badge_fuerte = " *(resaltadas en grafo)*" if fuertemente else ""
                st.markdown(f"**Componentes Fuertemente Conexas:**{badge_fuerte}")
                _formatear_lista_componentes(
                    componentes_fuertemente_conexas,
                    obtener_etiqueta,
                    "C. Fuerte",
                )

                if componentes_debilmente_conexas:
                    badge_debil = " *(resaltadas en grafo)*" if not fuertemente else ""
                    st.markdown(f"**Componentes Débilmente Conexas:**{badge_debil}")
                    _formatear_lista_componentes(
                        componentes_debilmente_conexas,
                        obtener_etiqueta,
                        "C. Débil",
                    )
            elif componentes_conexas:
                st.info(
                    "ℹ️ Mostrando recorrido en anchura (BFS). "
                    "Selecciona **DFS** para calcular **Componentes Fuertemente Conexas** y **Débilmente Conexas**."
                )
                st.markdown("** Subgrafos alcanzados (BFS):**")
                _formatear_lista_componentes(componentes_conexas, obtener_etiqueta, "Grupo")
