import streamlit as st
import time
from db import save_session
from config import db_conn, ref_df, timer as t
from utils import generate_uuid, current_date, seconds_to_hms
from streamlit_autorefresh import st_autorefresh

# ——— Garantir state keys ———
if 'start_time' not in st.session_state:
    st.session_state.start_time = None
if 'accumulated' not in st.session_state:
    st.session_state.accumulated = 0
# ——————————————————————

st_autorefresh(interval=1_000, key="home_autorefresh")

st.header("Iniciar Sessão de Estudo")

# Seleções dinâmicas
discipline = st.selectbox(
    "Disciplina",
    options=ref_df['disciplina'].unique()
)
topic = st.selectbox(
    "Tópico",
    options=ref_df.query("disciplina == @discipline")['topico'].unique()
)

# Placeholder para mostrar o cronômetro
timer_placeholder = st.empty()

# Botões do cronômetro
col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 1])
with col1:
    if st.button("Start"):
        t.start()
with col2:
    if st.button("Pause"):
        t.pause()
with col3:
    if st.button("Resume"):
        t.resume()
with col4:
    if st.button("Stop"):
        duration = t.stop()
        session = {
            'session_id': generate_uuid(),
            'date': current_date(),
            'discipline': discipline,
            'topic': topic,
            'duration_seconds': duration
        }
        save_session(db_conn, session)
        st.session_state['last_message'] = f"Sessão salva: {seconds_to_hms(duration)}."
        #st.success(f"Sessão salva: {seconds_to_hms(duration)}.")
with col5:
    if st.button("Desconsiderar", key="discard", help="Zera esta sessão sem salvar"):
        st.session_state.start_time = None
        st.session_state.accumulated = 0
        st.info("Sessão desconsiderada.")

if 'last_message' in st.session_state:
    st.success(st.session_state['last_message'])
    
# # Botões do cronômetro
# col1, col2, col3, col4 = st.columns([1,1,1,1])
# with col1:
#     if st.button("Start"):
#         t.start()
# with col2:
#     if st.button("Pause"):
#         t.pause()
# with col3:
#     if st.button("Stop"):
#         duration = t.stop()
#         session = {
#             'session_id': generate_uuid(),
#             'date': current_date(),
#             'discipline': discipline,
#             'topic': topic,
#             'duration_seconds': duration
#         }
#         save_session(db_conn, session)
#         st.success(f"Sessão salva: {seconds_to_hms(duration)}.")
# with col4:
#     if st.button("Desconsiderar", key="discard", help="Zera esta sessão sem salvar"):
#         # Zera o cronômetro sem salvar
#         st.session_state.start_time = None
#         st.session_state.accumulated = 0
#         st.info("Sessão desconsiderada.")



# Exibe o tempo decorrido (ao vivo ou acumulado)
if st.session_state.start_time:
    elapsed = st.session_state.accumulated + (time.time() - st.session_state.start_time)
    timer_placeholder.markdown(f"**Tempo decorrido:** `{seconds_to_hms(int(elapsed))}`")
else:
    if st.session_state.accumulated > 0:
        timer_placeholder.markdown(
            f"**Tempo decorrido:** `{seconds_to_hms(int(st.session_state.accumulated))}`"
        )

