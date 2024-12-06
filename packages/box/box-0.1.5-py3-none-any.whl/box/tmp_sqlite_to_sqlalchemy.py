from box.timer import Timer
timer = Timer()
timer.start("tmp_sqlite_to_sqlalchemy.py")
timer.start("import sqlite3")
import sqlite3
timer.print("import sqlite3")
from sqlalchemy import create_engine, text
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import Session

def test_sqlite_to_sqlalchemy():
    # Create SQLite connection and insert test data
    sqlite_conn = sqlite3.connect(':memory:')
    cursor = sqlite_conn.cursor()
    
    # Create table using raw SQL
    cursor.execute("""
        CREATE TABLE test_table (
            category TEXT,
            name TEXT
        )
    """)
    
    # Insert test data using raw SQL
    cursor.execute("""
        INSERT INTO test_table (category, name) VALUES
        ('A', 'Apple'),
        ('A', 'Astronaut'),
        ('B', 'Banana'),
        ('B', 'Bird'),
        ('B', 'Bison')
    """)
    sqlite_conn.commit()
    
    # Verify data using raw SQL
    cursor.execute("SELECT * FROM test_table")
    raw_results = cursor.fetchall()
    print("\nRaw SQLite results:")
    print(raw_results)
    
    # Convert to SQLAlchemy
    engine = create_engine(
        'sqlite://',
        creator=lambda: sqlite_conn,
        poolclass=StaticPool
    )
    
    # Use SQLAlchemy session to query
    with Session(engine) as session:
        # Query using SQLAlchemy
        result = session.execute(
            text("SELECT * FROM test_table WHERE category = :cat"),
            {"cat": "A"}
        )
        sqlalchemy_results = result.fetchall()
        print("\nSQLAlchemy results (category = 'A'):")
        print(sqlalchemy_results)
        
        # Try another query
        result = session.execute(
            text("SELECT category, COUNT(*) as count FROM test_table GROUP BY category")
        )
        group_results = result.fetchall()
        print("\nSQLAlchemy results (grouped):")
        print(group_results)
    
    # Clean up
    sqlite_conn.close()

if __name__ == "__main__":
    test_sqlite_to_sqlalchemy()
timer.print("tmp_sqlite_to_sqlalchemy.py")
