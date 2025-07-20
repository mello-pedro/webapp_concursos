import streamlit as st
from db import save_exercise_session
from config import db_conn, ref_df
from utils import generate_uuid, current_date

st.header("Registro de Exercícios")

# Inicializa flag na sessão
if "confirmar_sessao" not in st.session_state:
    st.session_state.confirmar_sessao = False

# Seleções dinâmicas
discipline = st.selectbox(
    "Disciplina",
    options=ref_df['disciplina'].unique()
)

topic = st.selectbox(
    "Tópico",
    options=ref_df.query("disciplina == @discipline")['topico'].unique()
)

# Inputs numéricos
qtd_feitas = st.number_input("Total de questões feitas", min_value=0, step=1)
qtd_certas = st.number_input("Acertos", min_value=0, step=1)
qtd_erradas = st.number_input("Erros", min_value=0, step=1)
qtd_branco = st.number_input("Em branco", min_value=0, step=1)

# Botão de salvar que ativa a confirmação
if st.button("Salvar Sessão de Exercícios"):
    st.session_state.confirmar_sessao = True

# Se clicou no botão acima, exibe confirmação
if st.session_state.confirmar_sessao:
    with st.expander("⚠️ Confirmação", expanded=True):
        st.warning(
            f"Você está prestes a salvar a sessão com os seguintes dados:\n\n"
            f"- 📅 Data: **{current_date()}**\n"
            f"- 📚 Disciplina: **{discipline}**\n"
            f"- 🧩 Tópico: **{topic}**\n"
            f"- 📝 Questões feitas: **{qtd_feitas}**\n"
            f"- ✅ Acertos: **{qtd_certas}**\n"
            f"- ❌ Erros: **{qtd_erradas}**\n"
            f"- ❔ Em branco: **{qtd_branco}**\n"
        )

        col1, col2 = st.columns(2)
        with col1:
            if st.button("Confirmar e Salvar", key="confirmar"):
                total_resps = qtd_certas + qtd_erradas + qtd_branco
                if total_resps != qtd_feitas:
                    st.error(f"A soma de acertos ({qtd_certas}), erros ({qtd_erradas}) e em branco ({qtd_branco}) não pode ser diferente do total de questões feitas ({qtd_feitas}).")
                else:
                    session = {
                        'session_id': generate_uuid(),
                        'date': current_date(),
                        'discipline': discipline,
                        'topic': topic,
                        'qtd_feitas': qtd_feitas,
                        'qtd_certas': qtd_certas,
                        'qtd_erradas': qtd_erradas,
                        'qtd_branco': qtd_branco
                    }
                    save_exercise_session(db_conn, session)
                    st.success("Sessão de exercícios salva com sucesso!")
                    st.session_state.confirmar_sessao = False  # reseta

        with col2:
            if st.button("Cancelar", key="cancelar"):
                st.info("Operação cancelada.")
                st.session_state.confirmar_sessao = False  # reseta

