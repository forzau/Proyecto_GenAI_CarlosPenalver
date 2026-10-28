"""Primera web local: el mismo agente del notebook, una memoria por sesión."""

from base64 import b64encode
from html import escape
from pathlib import Path
from uuid import uuid4

import streamlit as st

from agent import ERROR_CUOTA, ERROR_SERVICIO_OCUPADO
from web_runtime import MODELOS, cargar_agente, modelo_inicial, preparar_datos


ROOT = Path(__file__).resolve().parent
SIMULADORES = {"lmu": "Le Mans Ultimate", "iracing": "iRacing", "acc": "ACC"}
ERROR_RESPUESTA = "No he podido completar la respuesta. Puedes volver a intentarlo o continuar con otra consulta."



def iniciar_sesion():
    if "conversacion" not in st.session_state:
        st.session_state.conversacion = {"configurable": {"thread_id": uuid4().hex}}
        st.session_state.mensajes = []
        st.session_state.trazas = []
        st.session_state.contexto = None
        st.session_state.pendiente = None
        st.session_state.consulta_pendiente = None


def nueva_conversacion(agente):
    """Retira también los checkpoints anteriores de esta sesión."""
    agente.checkpointer.delete_thread(st.session_state.conversacion["configurable"]["thread_id"])
    del st.session_state["conversacion"]
    iniciar_sesion()


def atender_consulta(agente, pregunta):
    st.session_state.mensajes.append({"role": "user", "content": pregunta})
    try:
        resultado = agente.invoke({"pregunta": pregunta}, config=st.session_state.conversacion)
        # Se conserva la evidencia en la sesión, pero no se envía a los componentes de la página.
        st.session_state.trazas.append({**resultado, "modelo": st.session_state.modelo})
        st.session_state.contexto = resultado.get("contexto")
        st.session_state.pendiente = resultado.get("contexto_pendiente")
        respuesta = resultado["respuesta_piloto"]
        if not respuesta.strip():
            raise ValueError("Respuesta vacía.")
        mensaje = {"role": "assistant", "content": respuesta, "error": bool(resultado.get("error"))}
    except Exception as error:
        mensaje = {"role": "assistant", "content": {503: ERROR_SERVICIO_OCUPADO, 429: ERROR_CUOTA}.get(
            getattr(error, "code", None), ERROR_RESPUESTA), "error": True}
    st.session_state.mensajes.append(mensaje)


def mostrar_mensaje(mensaje):
    avatar = ":material/person:" if mensaje["role"] == "user" else ":material/sports_motorsports:"
    with st.chat_message(mensaje["role"], avatar=avatar):
        if mensaje.get("error"):
            st.error(mensaje["content"])
        else:
            st.markdown(mensaje["content"])


def mostrar_sidebar(agente, logo):
    with st.sidebar:
        st.markdown(f'''<svg class="sidebar-logo" viewBox="90 895 1200 225" role="img" aria-label="BOX">
        <image width="1375" height="1144" href="data:image/png;base64,{logo}" /></svg>''', unsafe_allow_html=True)
        st.caption("TU INGENIERO DE PISTA")
        st.button("Nueva conversación", icon=":material/add:", on_click=nueva_conversacion,
                  args=(agente,), width="stretch", disabled=bool(st.session_state.get("consulta_pendiente")))
        st.divider()
        st.markdown("##### Sesión de pista")
        contexto = st.session_state.contexto or {}
        sim = contexto.get("simulador")
        nombre = SIMULADORES.get(sim, sim) if sim else "Por identificar"
        coche = contexto.get("coche") or "Por identificar"
        st.markdown('<div class="context-label">SIMULADOR</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="context-value">{escape(nombre)}</div>', unsafe_allow_html=True)
        st.markdown('<div class="context-label">COCHE</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="context-value">{escape(coche)}</div>', unsafe_allow_html=True)
        if st.session_state.pendiente:
            pendiente = st.session_state.pendiente
            destino = SIMULADORES.get(pendiente["simulador"], pendiente["simulador"])
            if pendiente.get("coche"):
                destino += " · " + pendiente["coche"]
            st.info(f"Cambio pendiente: {destino}. Confírmalo o cancélalo en el chat.")
        st.divider()
        st.caption("Cuéntame el contexto al conversar. No hace falta rellenar formularios.")


def main():
    st.set_page_config(page_title="BOX · Ingeniero de pista", page_icon="🏁", layout="centered")
    st.markdown("<style>" + (ROOT / "ui/style.css").read_text(encoding="utf-8") + "</style>", unsafe_allow_html=True)
    preparar_datos()
    iniciar_sesion()
    try:
        if "modelo" not in st.session_state:
            st.session_state.modelo = modelo_inicial()
        agente = cargar_agente(st.session_state.modelo)
    except Exception:
        st.title("BOX · Ingeniero de pista")
        st.error("No se ha podido iniciar el ingeniero. Revisa la configuración local del proyecto y vuelve a abrir la página.")
        st.stop()
    logo = b64encode((ROOT / "ui/box-logo.png").read_bytes()).decode("ascii")
    mostrar_sidebar(agente, logo)
    ocupado = bool(st.session_state.get("consulta_pendiente"))
    if not st.session_state.mensajes and not ocupado:
        st.markdown(f'''<div class="welcome">
        <h1 class="welcome-logo"><img src="data:image/png;base64,{logo}" alt="BOX · Tu ingeniero de pista"></h1>
        <p>En boxes y listo para escucharte</p></div>''', unsafe_allow_html=True)
    for mensaje in st.session_state.mensajes:
        mostrar_mensaje(mensaje)
    with st.bottom.container(key="composer", gap=None):
        pregunta = st.chat_input("¿En qué simulador estás y qué notas al conducir?",
                                key="borrador", max_chars=4000, disabled=ocupado)
        with st.container(key="modelo_control"):
            st.selectbox("Modelo Gemini", MODELOS, format_func=MODELOS.get, key="modelo",
                         label_visibility="collapsed", disabled=ocupado)
    if pregunta and pregunta.strip():
        st.session_state.consulta_pendiente = pregunta.strip()
        # Primero se dibujan los controles desactivados; después se llama al agente.
        st.rerun()
    if ocupado:
        consulta = st.session_state.consulta_pendiente
        with st.chat_message("user", avatar=":material/person:"):
            st.markdown(consulta)
        with st.spinner("Estoy revisando tu caso…"):
            atender_consulta(agente, consulta)
        st.session_state.consulta_pendiente = None
        # El rerun solo presenta lo guardado: no vuelve a invocar al agente.
        st.rerun()


if __name__ == "__main__":
    main()
