import sqlite3
from pathlib import Path
import datetime

DB_FILE_NAME = "snipcli.db"
APP_CONFIG_DIR_NAME = ".snipcli" # Typically a hidden directory in user's home

def get_db_path() -> Path:
    """
    Returns the absolute path to the SQLite database file.
    Creates the necessary application configuration directory if it doesn't exist.
    """
    home_dir = Path.home()
    app_config_dir = home_dir / APP_CONFIG_DIR_NAME
    db_path = app_config_dir / DB_FILE_NAME

    # Ensure the application configuration directory exists
    app_config_dir.mkdir(parents=True, exist_ok=True)
    
    return db_path

def init_db(conn: sqlite3.Connection) -> None:
    """
    Initializes the database schema by creating necessary tables and indexes.
    """
    with conn: # This ensures transactions are handled automatically (commit on success, rollback on error)
        cursor = conn.cursor()
        
        # Table for storing code snippets
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS snippets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,       -- Unique name for the snippet
                content TEXT NOT NULL,           -- The actual code snippet content
                language TEXT,                   -- Optional: programming language (e.g., 'python', 'javascript')
                tags TEXT,                       -- Optional: comma-separated tags (e.g., 'web,frontend')
                created_at TEXT NOT NULL,        -- ISO 8601 formatted datetime string
                updated_at TEXT NOT NULL         -- ISO 8601 formatted datetime string
            )
        """)
        
        # Create an index on the 'name' column for faster lookups and uniqueness enforcement
        cursor.execute("CREATE UNIQUE INDEX IF NOT EXISTS idx_snippet_name ON snippets (name)")

def get_db_connection() -> sqlite3.Connection:
    """
    Returns a connection to the SQLite database.
    Initializes the database schema if it doesn't exist.
    """
    db_path = get_db_path()
    
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row # Allows accessing columns by name (e.g., row['name'])

    # Initialize the database schema if tables do not exist
    init_db(conn)
        
    return conn