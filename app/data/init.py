import os
from pathlib import Path
from sqlite3 import Connection, Cursor, connect, IntegrityError

conn: Connection | None = None
cursor: Cursor | None = None


def get_db(name: str | None = None, reset: bool = False):
    global conn, cursor
    if conn:
        if not reset:
            return
        conn = None
    if not name:
        top_dir = Path(__file__).resolve().parents[1]
        db_dir = top_dir / "db"
        db_name = "cryptid.db"
        db_path = str(db_dir / db_name)
        name = os.getenv("CRYPTID_SQLITE_DB", db_path)
    conn = connect(name, check_same_thread=False)
    cursor = conn.cursor()


# Modules are singletons, so this only gets executed once
get_db()
