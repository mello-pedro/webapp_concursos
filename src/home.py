# src/main.py

import streamlit as st
import pandas as pd
import datetime
import random

from loader import load_reference
from db import init_db, init_metas_tables

# ——— Configurações iniciais ———
DB_PATH   = 'db/study_sessions.db'
REF_PATH  = 'data/reference.xlsx'

db_conn = init_db(DB_PATH)
ref_df   = load_reference(REF_PATH)

# Carrega todas as sessões para métricas
df = pd.read_sql_query("SELECT * FROM sessions", db_conn)
df['date'] = pd.to_datetime(df['date']).dt.date

# Datas auxiliares
today          = datetime.date.today()
first_of_month = today.replace(day=1)
monday         = today - datetime.timedelta(days=today.weekday())
# ————————————————————————

# ——— Layout da página ———
st.set_page_config(page_title="🎯 Study Tracker", layout="wide")

# 1) Banner de boas‑vindas
# Se quiser usar logo, coloque 'logo.png' na raiz do projeto:
# st.image("logo.png", width=100)
st.title("🎯 Monitoramento de Estudos")
st.markdown(
    """
    Bem‑vindo ao painel de monitoramento de estudos!  
    Registre suas sessões, acompanhe seu progresso e mantenha o foco nos seus objetivos.
    """
)

# 2) Métricas principais
total_hours   = df['duration_seconds'].sum() / 3600
daily_avg_h   = df.groupby('date')['duration_seconds'].sum().mean() / 3600
max_session_h = df['duration_seconds'].max() / 3600 if not df.empty else 0.0
sessions_month = df.query("date >= @first_of_month").shape[0]

col1, col2, col3, col4 = st.columns(4)
col1.metric("⏱️ Total de Horas", f"{total_hours:.1f} h")
col2.metric("📅 Média Diária", f"{daily_avg_h:.1f} h")
col3.metric("🔥 Maior Sessão", f"{max_session_h:.1f} h")
col4.metric("📋 Sessões (mês)", sessions_month)

st.markdown("---")

# 4) Progresso Semanal
weekly_goal = 10  # meta em horas
hours_week  = df.query("date >= @monday")['duration_seconds'].sum() / 3600
progress_pct = min(hours_week / weekly_goal, 1.0)
st.write(f"🗓️ **Esta semana:** {hours_week:.1f}h de {weekly_goal}h ({progress_pct * 100:.0f}%)")
st.progress(progress_pct)

st.markdown("---")

init_metas_tables(db_conn)



# import streamlit as st
# from loader import load_reference
# from db import init_db, save_session
# from timer import Timer
# from utils import generate_uuid, current_date

# # Configurações iniciais
# db_conn = init_db('db/study_sessions.db')
# ref_df = load_reference('data/reference.xlsx')
# t = Timer()

# st.set_page_config(page_title="Study Tracker", layout="centered")

# # Multipage via folder "pages/"
# st.write("Use o menu lateral para navegar entre Home e Dashboard.")