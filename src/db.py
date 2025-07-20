import sqlite3
from uuid import uuid4

def init_db(db_path: str):
    conn = sqlite3.connect(db_path)
    conn.execute("""
    CREATE TABLE IF NOT EXISTS sessions(
        session_id TEXT PRIMARY KEY,
        date TEXT,
        discipline TEXT,
        topic TEXT,
        duration_seconds INTEGER
    )""")
    conn.commit()
    return conn


def save_session(conn, session: dict):
    conn.execute(
        "INSERT INTO sessions(session_id, date, discipline, topic, duration_seconds) VALUES (?,?,?,?,?)",
        (
            session['session_id'], session['date'],
            session['discipline'], session['topic'],
            session['duration_seconds']
        )
    )
    conn.commit()


def save_exercise_session(conn, session):
    query = """
    INSERT INTO exercicio_sessoes (
        session_id,
        date,
        discipline,
        topic,
        qtd_feitas,
        qtd_certas,
        qtd_erradas,
        qtd_branco
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """
    values = (
        session['session_id'],
        session['date'],
        session['discipline'],
        session['topic'],
        session['qtd_feitas'],
        session['qtd_certas'],
        session['qtd_erradas'],
        session['qtd_branco']
    )
    conn.execute(query, values)
    conn.commit()

def init_metas_tables(conn):
    conn.execute("""
    CREATE TABLE IF NOT EXISTS metas_edital (
        item_id      INTEGER PRIMARY KEY AUTOINCREMENT,
        descricao    TEXT UNIQUE,
        concluido    INTEGER DEFAULT 0
    )""")
    conn.execute("""
    CREATE TABLE IF NOT EXISTS weekly_goals (
        week_start        TEXT PRIMARY KEY,  -- ex: '2025-07-14'
        study_goal_hours  REAL,
        exercise_goal_cnt INTEGER
    )""")
    conn.commit()
