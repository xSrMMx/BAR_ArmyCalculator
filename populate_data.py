import sqlite3

def create_connection(db_file="game_data.db"):
    """Create a database connection to the SQLite database"""
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except sqlite3.Error as e:
        print(e)
    
    return conn

def create_table(conn):
    """Create the table if it doesn't exist"""
    sql_create_table = """
    CREATE TABLE IF NOT EXISTS units (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        metal INTEGER NOT NULL
    );
    """
    
    try:
        cursor = conn.cursor()
        cursor.execute(sql_create_table)
    except sqlite3.Error as e:
        print(e)

def insert_unit(conn, unit):
    """Insert a new unit into the units table"""
    sql = """
    INSERT INTO units(name, metal) VALUES(?, ?)
    """
    
    try:
        cursor = conn.cursor()
        cursor.execute(sql, unit)
        conn.commit()
        return cursor.lastrowid
    except sqlite3.Error as e:
        print(e)
        
    return None

def populate_data(conn):
    """Populate the database with the provided data"""
    units = [
        ("CBot", 110),
        ("Pawn", 52),
        ("Lazarus", 130),
        ("Rocketeer", 130),
        ("Mace", 130),
        ("Crossbow", 125),
        ("Centurion", 270),
        ("Tick", 21)
    ]
    
    for unit in units:
        unit_id = insert_unit(conn, unit)
        print(f"Added {unit[0]} with metal {unit[1]}, ID: {unit_id}")

def display_all_units(conn):
    """Display all units in the database"""
    sql = "SELECT * FROM units"
    
    try:
        cursor = conn.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        
        print("\nAll units in database:")
        print("ID | Name | metal")
        print("-" * 30)
        for row in rows:
            print(f"{row[0]} | {row[1]} | {row[2]}")
    except sqlite3.Error as e:
        print(e)

def main():
    """Main function to run the script"""
    conn = create_connection()
    
    if conn is not None:
        create_table(conn)
        populate_data(conn)
        display_all_units(conn)
        conn.close()
    else:
        print("Error! Cannot create the database connection.")

if __name__ == "__main__":
    main()