import streamlit as st
import pandas as pd
from config import ref_df, timer as t
from db import get_connection, init_db

DB_PATH = "db/study_sessions.db"

# Inicializa o banco (garante que o arquivo existe e tabelas básicas também)
init_db(DB_PATH)

# Carrega os dados dentro de um bloco seguro
with get_connection(DB_PATH) as conn:
    df_estudo = pd.read_sql_query("SELECT * FROM sessions", conn)
    df_exercicios = pd.read_sql_query("SELECT * FROM exercicio_sessoes", conn)

# Expander para sessões de estudo
with st.expander("📚 Sessões de Estudo", expanded=False):
    st.dataframe(df_estudo, hide_index=True)

# Expander para exercícios resolvidos
with st.expander("✅ Exercícios Resolvidos", expanded=False):
    st.dataframe(df_exercicios, hide_index=True)
