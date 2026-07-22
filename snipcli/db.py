import sqlite3
from pathlib import Path
import datetime
from typing import Optional, List

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

def add_snippet(name: str, content: str, language: Optional[str] = None, tags: Optional[str] = None) -> int:
    """
    Inserts a new code snippet into the database.

    Args:
        name (str): Unique name for the snippet.
        content (str): The actual code snippet content.
        language (Optional[str]): Programming language (e.g., 'python'). Defaults to None.
        tags (Optional[str]): Comma-separated tags (e.g., 'web,frontend'). Defaults to None.

    Returns:
        int: The ID of the newly inserted snippet.
    """
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        now = datetime.datetime.now().isoformat()
        
        cursor.execute("""
            INSERT INTO snippets (name, content, language, tags, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (name, content, language, tags, now, now))
        
        conn.commit()
        return cursor.lastrowid
    finally:
        conn.close()

def get_snippet_by_id(snippet_id: int) -> Optional[sqlite3.Row]:
    """
    Retrieves a single code snippet by its ID.

    Args:
        snippet_id (int): The ID of the snippet to retrieve.

    Returns:
        Optional[sqlite3.Row]: The snippet as a sqlite3.Row object if found, otherwise None.
    """
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, name, content, language, tags, created_at, updated_at
            FROM snippets
            WHERE id = ?
        """, (snippet_id,))
        
        snippet = cursor.fetchone()
        return snippet
    finally:
        conn.close()

def get_all_snippets() -> List[sqlite3.Row]:
    """
    Retrieves all code snippets from the database.

    Returns:
        List[sqlite3.Row]: A list of all snippets, where each snippet is a sqlite3.Row object.
    """
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, content, language, tags, created_at, updated_at FROM snippets ORDER BY name")
        snippets = cursor.fetchall()
        return snippets
    finally:
        conn.close()

def search_snippets(keyword: str) -> List[sqlite3.Row]:
    """
    Searches for code snippets by matching keywords in their content or tags.
    The search is case-insensitive.

    Args:
        keyword (str): The keyword to search for.

    Returns:
        List[sqlite3.Row]: A list of matching snippets, where each snippet is a sqlite3.Row object.
    """
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        search_pattern = f"%{keyword}%"
        
        cursor.execute("""
            SELECT id, name, content, language, tags, created_at, updated_at 
            FROM snippets 
            WHERE 
                content LIKE ? COLLATE NOCASE OR 
                tags LIKE ? COLLATE NOCASE
            ORDER BY name
        """, (search_pattern, search_pattern))
        
        snippets = cursor.fetchall()
        return snippets
    finally:
        conn.close()