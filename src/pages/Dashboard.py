import streamlit as st
import pandas as pd
from db import init_db
from config import db_conn, ref_df, timer as t
import matplotlib.pyplot as plt

conn = init_db('db/study_sessions.db')
df = pd.read_sql_query("SELECT * FROM sessions", conn)

st.header("Desempenho de Estudos")

# Tempo total por disciplina
total_disc = df.groupby('discipline')['duration_seconds'].sum().reset_index()
fig1, ax1 = plt.subplots()
ax1.bar(total_disc['discipline'], total_disc['duration_seconds'])
ax1.set_ylabel('Total de segundos')
st.pyplot(fig1)

# Tempo total por tópico
total_top = df.groupby('topic')['duration_seconds'].sum().reset_index()
fig2, ax2 = plt.subplots()
ax2.bar(total_top['topic'], total_top['duration_seconds'])
ax2.set_ylabel('Total de segundos')
st.pyplot(fig2)