# src/config.py
from loader import load_reference
from db import init_db, get_connection, init_metas_tables
from timer import Timer

DB_PATH = 'db/study_sessions.db'
REF_PATH = 'data/reference.xlsx'

# apenas inicializa o banco (cria tabelas se não existir)
init_db(DB_PATH)
init_metas_tables(DB_PATH)

ref_df = load_reference(REF_PATH)
timer = Timer()
