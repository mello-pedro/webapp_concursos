# src/pages/Metas.py
import streamlit as st
import pandas as pd
from datetime import date, timedelta
from db import init_metas_tables, get_connection
from config import ref_df
from utils import current_date

DB_PATH = "db/study_sessions.db"

# ——— Inicialização das tabelas ———
init_metas_tables(DB_PATH)

# Garante que a coluna 'concluded_at' exista (migração simples)
with get_connection(DB_PATH) as conn:
    try:
        conn.execute("ALTER TABLE metas_edital ADD COLUMN concluded_at TEXT")
        conn.commit()
    except Exception:
        pass  # coluna já existe, segue adiante

    conn.execute("""
    CREATE TABLE IF NOT EXISTS study_cycle (
        id           INTEGER PRIMARY KEY AUTOINCREMENT,
        disciplina   TEXT,
        dia_semana   TEXT,
        horas        REAL,
        criado_em    TEXT
    )
    """)
    conn.commit()

st.header("📋 Metas e Checklist")

# Puxa dados atuais
with get_connection(DB_PATH) as conn:
    df_edital = pd.read_sql_query("SELECT * FROM metas_edital", conn)
    df_goals = pd.read_sql_query("SELECT * FROM weekly_goals", conn)

# Cria as três abas
tab1, tab2, tab3 = st.tabs([
    "✔️ Checklist do Edital",
    "🎯 Metas Semanais",
    "🔄 Ciclo de Estudos"
])

# ——— ABA 1: Checklist do Edital ———
with tab1:
    st.subheader("Marcar Item do Edital como Concluído")

    disciplinas = ref_df['disciplina'].unique()
    disciplina_sel = st.selectbox("Disciplina", disciplinas, key="check_disc")
    topicos = ref_df.query("disciplina == @disciplina_sel")['topico'].unique()
    topico_sel = st.selectbox("Tópico", topicos, key="check_top")

    desc = f"{disciplina_sel} • {topico_sel}"
    now = current_date("%Y-%m-%d %H:%M:%S")

    if st.button("✅ Concluído", key="btn_conclud"):
        with get_connection(DB_PATH) as conn:
            cur = conn.execute("SELECT item_id FROM metas_edital WHERE descricao = ?", (desc,)).fetchone()
            if cur:
                conn.execute(
                    "UPDATE metas_edital SET concluido = 1, concluded_at = ? WHERE descricao = ?",
                    (now, desc)
                )
            else:
                conn.execute(
                    "INSERT INTO metas_edital(descricao, concluido, concluded_at) VALUES (?, 1, ?)",
                    (desc, now)
                )
            conn.commit()
        st.success(f"✔️ Marcado como concluído: **{desc}**")

    # Recarrega a lista de concluídos
    with get_connection(DB_PATH) as conn:
        df_done = pd.read_sql_query(
            "SELECT descricao, date(concluded_at) AS quando FROM metas_edital WHERE concluido = 1",
            conn
        )
    st.markdown("---")
    st.write("### Itens já finalizados")
    if df_done.empty:
        st.info("Nenhum item concluído ainda.")
    else:
        st.table(df_done)

# ——— ABA 2: Metas Semanais ———
with tab2:
    hoje = date.today()
    monday = hoje - timedelta(days=hoje.weekday())
    sunday = monday + timedelta(days=6)
    monday_str = monday.isoformat()
    m_str, s_str = monday.strftime("%d/%m"), sunday.strftime("%d/%m")

    st.subheader(f"Defina sua meta para esta semana ({m_str} – {s_str})")

    with get_connection(DB_PATH) as conn:
        df_goals = pd.read_sql_query("SELECT * FROM weekly_goals", conn)
    row = df_goals.query("week_start == @monday_str")
    atual_study = float(row['study_goal_hours'].iloc[0]) if not row.empty else 0.0
    atual_exercise = int(row['exercise_goal_cnt'].iloc[0]) if not row.empty else 0

    with st.form("form_goals"):
        new_study = st.number_input(
            "Horas de estudo total na semana",
            min_value=0.0, value=atual_study or 5.0, step=0.5, key="new_study"
        )
        new_exercise = st.number_input(
            "Qtd. total de questões resolvidas na semana",
            min_value=0, value=atual_exercise or 20, step=1, key="new_exercise"
        )
        submitted = st.form_submit_button("Salvar Meta")

    if "confirm_edit" not in st.session_state:
        st.session_state.confirm_edit = False

    if submitted:
        if (not row.empty) and new_study == atual_study and new_exercise == atual_exercise:
            st.error(f"Essa já é a meta vigente para esta semana ({m_str} – {s_str}).")
        else:
            with get_connection(DB_PATH) as conn:
                if row.empty:
                    conn.execute("""
                        INSERT INTO weekly_goals(week_start, study_goal_hours, exercise_goal_cnt)
                        VALUES (?, ?, ?)
                    """, (monday_str, new_study, new_exercise))
                    conn.commit()
                    st.success("Meta semanal cadastrada com sucesso!")
                else:
                    st.session_state.confirm_edit = True

    if st.session_state.confirm_edit:
        with st.expander("⚠️ Confirmar Alteração de Meta", expanded=True):
            st.warning(
                f"- Meta ATUAL: {atual_study:.1f}h e {atual_exercise} exercícios\n"
                f"- Nova meta: {new_study:.1f}h e {new_exercise} exercícios"
            )
            c1, c2 = st.columns(2)
            with c1:
                if st.button("Confirmar Alteração", key="confirm_meta"):
                    with get_connection(DB_PATH) as conn:
                        conn.execute("""
                            UPDATE weekly_goals
                            SET study_goal_hours = ?, exercise_goal_cnt = ?
                            WHERE week_start = ?
                        """, (new_study, new_exercise, monday_str))
                        conn.commit()
                    st.success("Meta semanal alterada com sucesso!")
                    st.session_state.confirm_edit = False
            with c2:
                if st.button("Cancelar Alteração", key="cancel_meta"):
                    st.info("Alteração de meta cancelada.")
                    st.session_state.confirm_edit = False

    # KPIs semanais
    with get_connection(DB_PATH) as conn:
        df_sessions = pd.read_sql_query("SELECT * FROM sessions", conn)
        df_exercicios = pd.read_sql_query("SELECT * FROM exercicio_sessoes", conn)
    df_sessions['date'] = pd.to_datetime(df_sessions['date']).dt.date
    df_exercicios['date'] = pd.to_datetime(df_exercicios['date']).dt.date

    horas_sem = df_sessions.query("date >= @monday & date <= @hoje")['duration_seconds'].sum() / 3600
    qtde_sem = df_exercicios.query("date >= @monday & date <= @hoje")['qtd_feitas'].sum()

    st.markdown("---")
    st.markdown(f"#### Progresso desta semana ({m_str} – {s_str})")

    c1, c2 = st.columns(2, gap="large")
    with c1:
        pct_study = int(horas_sem / atual_study * 100) if atual_study else 0
        st.metric("⏱️ Estudo (h)", f"{horas_sem:.1f} / {atual_study:.1f}", delta=f"{pct_study}%")
    with c2:
        pct_ex = int(qtde_sem / atual_exercise * 100) if atual_exercise else 0
        st.metric("📊 Exercícios (qtd)", f"{qtde_sem} / {atual_exercise}", delta=f"{pct_ex}%")

# ——— ABA 3: Ciclo de Estudos ———
with tab3:
    st.subheader("🔄 Agende seu Ciclo de Estudos")

    disciplina = st.selectbox("Disciplina", ref_df['disciplina'].unique(), key="cycle_disc")
    dias = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"]
    dia_semana = st.selectbox("Dia da Semana", dias, key="cycle_day")
    horas = st.number_input("Horas de estudo neste dia", min_value=0.0, step=0.5, format="%.1f", key="cycle_hours")

    if st.button("➕ Adicionar ao Ciclo", key="add_cycle"):
        agora = current_date("%Y-%m-%d %H:%M:%S")
        with get_connection(DB_PATH) as conn:
            conn.execute(
                "INSERT INTO study_cycle (disciplina, dia_semana, horas, criado_em) VALUES (?,?,?,?)",
                (disciplina, dia_semana, horas, agora)
            )
            conn.commit()
        st.success(f"✅ {disciplina} — {horas:.1f}h na {dia_semana} adicionado ao ciclo.")

    if "confirm_clear_cycle" not in st.session_state:
        st.session_state.confirm_clear_cycle = False

    if st.button("🗑️ Limpar Ciclo (apagar tudo)", key="btn_clear_cycle"):
        st.session_state.confirm_clear_cycle = True

    if st.session_state.confirm_clear_cycle:
        with st.expander("⚠️ Confirmar Limpeza do Ciclo", expanded=True):
            st.warning("Isto apagará TODO o cronograma de estudos salvo.")
            c1, c2 = st.columns(2)
            with c1:
                if st.button("Confirmar Limpeza", key="confirm_clear"):
                    with get_connection(DB_PATH) as conn:
                        conn.execute("DELETE FROM study_cycle")
                        conn.commit()
                    st.success("Cronograma limpo.")
                    st.session_state.confirm_clear_cycle = False
            with c2:
                if st.button("Cancelar", key="cancel_clear"):
                    st.info("Operação cancelada.")
                    st.session_state.confirm_clear_cycle = False

    with get_connection(DB_PATH) as conn:
        df_cycle = pd.read_sql_query("""
            SELECT * FROM study_cycle
            ORDER BY CASE dia_semana
                WHEN 'Segunda' THEN 1 WHEN 'Terça' THEN 2 WHEN 'Quarta' THEN 3
                WHEN 'Quinta' THEN 4 WHEN 'Sexta' THEN 5 WHEN 'Sábado' THEN 6
                WHEN 'Domingo' THEN 7 END
        """, conn)

    st.markdown("---")
    st.write("### Cronograma de Estudos Salvo")
    if df_cycle.empty:
        st.info("Nenhum agendamento no ciclo ainda.")
    else:
        st.dataframe(df_cycle[["disciplina", "dia_semana", "horas", "criado_em"]], hide_index=True)
