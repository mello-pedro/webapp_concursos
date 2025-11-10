# src/db.py
import sqlite3
import threading

_db_lock = threading.Lock()

def get_connection(db_path: str = "db/study_sessions.db"):
    """Cria uma conexão nova, segura para threads."""
    return sqlite3.connect(db_path, check_same_thread=False)

def init_db(db_path: str):
    """Inicializa a base de dados (se não existir)."""
    with _db_lock:
        conn = get_connection(db_path)
        conn.execute("""
        CREATE TABLE IF NOT EXISTS sessions(
            session_id TEXT PRIMARY KEY,
            date TEXT,
            discipline TEXT,
            topic TEXT,
            duration_seconds INTEGER
        )""")
        conn.commit()
        conn.close()

def save_session(session: dict, db_path: str = "db/study_sessions.db"):
    with _db_lock:
        conn = get_connection(db_path)
        conn.execute(
            "INSERT INTO sessions(session_id, date, discipline, topic, duration_seconds) VALUES (?,?,?,?,?)",
            (
                session['session_id'], session['date'],
                session['discipline'], session['topic'],
                session['duration_seconds']
            )
        )
        conn.commit()
        conn.close()

def save_exercise_session(session, db_path: str = "db/study_sessions.db"):
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
    with _db_lock:
        conn = get_connection(db_path)
        conn.execute(query, (
            session['session_id'],
            session['date'],
            session['discipline'],
            session['topic'],
            session['qtd_feitas'],
            session['qtd_certas'],
            session['qtd_erradas'],
            session['qtd_branco']
        ))
        conn.commit()
        conn.close()

def init_metas_tables(db_path: str = "db/study_sessions.db"):
    with _db_lock:
        conn = get_connection(db_path)
        conn.execute("""
        CREATE TABLE IF NOT EXISTS metas_edital (
            item_id      INTEGER PRIMARY KEY AUTOINCREMENT,
            descricao    TEXT UNIQUE,
            concluido    INTEGER DEFAULT 0
        )""")
        conn.execute("""
        CREATE TABLE IF NOT EXISTS weekly_goals (
            week_start        TEXT PRIMARY KEY,
            study_goal_hours  REAL,
            exercise_goal_cnt INTEGER
        )""")
        conn.commit()
        conn.close()




# import sqlite3
# from uuid import uuid4

# def init_db(db_path: str):
#     conn = sqlite3.connect(db_path)
#     conn.execute("""
#     CREATE TABLE IF NOT EXISTS sessions(
#         session_id TEXT PRIMARY KEY,
#         date TEXT,
#         discipline TEXT,
#         topic TEXT,
#         duration_seconds INTEGER
#     )""")
#     conn.commit()
#     return conn


# def save_session(conn, session: dict):
#     conn.execute(
#         "INSERT INTO sessions(session_id, date, discipline, topic, duration_seconds) VALUES (?,?,?,?,?)",
#         (
#             session['session_id'], session['date'],
#             session['discipline'], session['topic'],
#             session['duration_seconds']
#         )
#     )
#     conn.commit()


# def save_exercise_session(conn, session):
#     query = """
#     INSERT INTO exercicio_sessoes (
#         session_id,
#         date,
#         discipline,
#         topic,
#         qtd_feitas,
#         qtd_certas,
#         qtd_erradas,
#         qtd_branco
#     ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
#     """
#     values = (
#         session['session_id'],
#         session['date'],
#         session['discipline'],
#         session['topic'],
#         session['qtd_feitas'],
#         session['qtd_certas'],
#         session['qtd_erradas'],
#         session['qtd_branco']
#     )
#     conn.execute(query, values)
#     conn.commit()

# def init_metas_tables(conn):
#     conn.execute("""
#     CREATE TABLE IF NOT EXISTS metas_edital (
#         item_id      INTEGER PRIMARY KEY AUTOINCREMENT,
#         descricao    TEXT UNIQUE,
#         concluido    INTEGER DEFAULT 0
#     )""")
#     conn.execute("""
#     CREATE TABLE IF NOT EXISTS weekly_goals (
#         week_start        TEXT PRIMARY KEY,  -- ex: '2025-07-14'
#         study_goal_hours  REAL,
#         exercise_goal_cnt INTEGER
#     )""")
#     conn.commit()
