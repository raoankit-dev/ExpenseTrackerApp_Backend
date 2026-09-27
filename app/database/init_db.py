from app.database.connection import get_connection


def create_tables():

    connection = get_connection()

    try:
        connection.executescript("""
                             
            CREATE TABLE IF NOT EXISTS users(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL,
                role TEXT NOT NULL DEFAULT "user",
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP           
            );
                                
            CREATE TABLE IF NOT EXISTS expenses(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                title TEXT NOT NULL,
                amount REAL NOT NULL,
                category TEXT NOT NULL,
                expense_date TEXT NOT NULL,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,

                FOREIGN KEY (user_id)
                REFERENCES users(id)        
            );
        """)
        
        connection.commit()
    
    finally:
        connection.close()
