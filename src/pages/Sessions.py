import streamlit as st
import pandas as pd
from config import db_conn, ref_df, timer as t
from db import init_db

# Conecta ao banco e carrega todas as sessões
conn = init_db('db/study_sessions.db')
df_estudo = pd.read_sql_query("SELECT * FROM sessions", conn)

df_exercicios = pd.read_sql_query("SELECT * FROM exercicio_sessoes", conn)

# Expander para sessões de estudo
with st.expander("📚 Sessões de Estudo", expanded=False):
    st.dataframe(df_estudo, hide_index=True)

# Expander para exercícios resolvidos
with st.expander("✅ Exercícios Resolvidos", expanded=False):
    st.dataframe(df_exercicios, hide_index=True)