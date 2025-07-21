
# src/pages/Dashboard.py

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from config import db_conn

st.set_page_config(page_title="📈 Dashboard de Estudos", layout="wide")


# --- Carrega dados ---
df_sessions   = pd.read_sql_query("SELECT * FROM sessions", db_conn)
df_exercises  = pd.read_sql_query("SELECT * FROM exercicio_sessoes", db_conn)

# converte datas e calcula horas
df_sessions['date'] = pd.to_datetime(df_sessions['date'])
df_sessions['hours'] = df_sessions['duration_seconds'] / 3600

# converte datas de exercícios
df_exercises['date'] = pd.to_datetime(df_exercises['date'])

# --- Métricas principais ---
total_hours      = df_sessions['hours'].sum()
total_questions  = df_exercises['qtd_feitas'].sum()
total_correct    = df_exercises['qtd_certas'].sum()
percent_correct  = (total_correct / total_questions * 100) if total_questions else 0

col1, col2, col3 = st.columns(3, gap="large")
col1.metric("⏱️ Horas Estudadas (total)", f"{total_hours:.1f} h")
col2.metric("✏️ Questões Respondidas", f"{int(total_questions)}")
col3.metric("✅ % de Acertos", f"{percent_correct:.0f}%")

st.markdown("---")

# --- Evolução Diária ---
st.subheader("Evolução ao Longo dos Dias")

# preparação dos dados diários
daily_hours = df_sessions.groupby(df_sessions['date'].dt.date)['hours'].sum().rename("Horas")
daily_qs    = df_exercises.groupby(df_exercises['date'].dt.date)['qtd_feitas'].sum().rename("Questões")

# linha de horas
st.line_chart(daily_hours, color="#d62728")

# linha de questões
st.line_chart(daily_qs, color="#bcbd22")

st.markdown("---")

# --- Gráficos de barras ---
st.subheader("Distribuição por Disciplina")

# horas por disciplina
hours_by_disc = (
    df_sessions
    .groupby('discipline')['hours']
    .sum()
    .sort_values(ascending=False)
)
st.bar_chart(hours_by_disc, color="#2ca02c")

st.markdown("---")

st.subheader("Questões Resolvidas Por Disciplina")

# questões por disciplina
qs_by_disc = (
    df_exercises
    .groupby('discipline')['qtd_feitas']
    .sum()
    .sort_values(ascending=False)
)
st.bar_chart(qs_by_disc, color="#e377c2")

st.markdown("---")

st.subheader("Percentual de Acertos por Disciplina")

# calcula % acertos disciplina a disciplina
disc_stats = (
    df_exercises
    .groupby('discipline')
    .agg({
        'qtd_certas': 'sum',
        'qtd_feitas': 'sum'
    })
)
disc_stats['pct_acertos'] = (disc_stats['qtd_certas'] / disc_stats['qtd_feitas']) * 100
pct_by_disc = disc_stats['pct_acertos'].sort_values(ascending=False)

st.bar_chart(pct_by_disc, color="#17becf")

st.markdown("---")
