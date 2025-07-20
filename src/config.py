from loader import load_reference
from db import init_db
from timer import Timer

DB_PATH   = 'db/study_sessions.db'
REF_PATH  = 'data/reference.xlsx'

db_conn = init_db(DB_PATH)
ref_df   = load_reference(REF_PATH)
timer    = Timer()
