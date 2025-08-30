# app/db/setup.py

"""
Database setup utilities for manual database management.
Implements functions to:
    - CREATE
    - DROP
    - RECREATE (dropd - create)
    - VIEW & VIEW verbose
    - IF EXISTS
    - EXECUTE STATEMENT
"""

from .db_models import (
    DepartmentMembership,
    Department,
    Organization,
    SystemClaim,
    SystemType,
    System,
    User
)

from .session import Base, engine
from sqlalchemy import text
from typing import List

metadata = Base.metadata

def create_all_tables() -> None:
    """ Create all the tables in the model """

    print("Creating all tables...")

    try:
        with engine.connect():
            metadata.create_all(bind=engine)
        print("Tables created sucesfully")
    except Exception as e:
        print(f"Error creating table: {e}")


def drop_all_tables() -> None:
    """ Drops all the tables """

    print("Dropping all the tables...")

    try:
        with engine.connect():
            metadata.drop_all(bind=engine)
        print("All tables dropped.")
    except Exception as e:
        print(f"Failed to drop tables: {e}")


def recreate_all_tables() -> None:
    """ Drops and creates all tables in the model """

    print("Reseting database ...")

    try:
        with engine.connect():
            drop_all_tables()
            create_all_tables()
        print("Database is reset,")
    except Exception as e:
        print(f"Database reset failed: {e}")


def list_tables() -> List:
    """ 
    List all the tables in the database by fetching the name of the tables
    in the information_schema.

    The 'public' table is the default schema name. This filters out other tables
    such as pg_catalog and custom schemas.

    The tables are sorted alphabetically.
    """

    with engine.connect() as connection:
        result = connection.execute(text(
                                """
                                SELECT table_name
                                FROM information_schema.tables
                                WHERE table_schema = 'public'
                                ORDER BY table_name;
                                """
                            ))
    tables = [row[0] for row in result] # Show the first column

    if tables:
        for table in tables:
            print(f" - {table}")            
    else:
        print("No tables found.")
        
    return tables


def list_tables_verobse() -> List:
    """
    As list_tables but includes:
    - Table name
    - Table type
    - Schema name
    """

    with engine.connect() as connection:
        result = connection.execute(text(
                                """
                                SELECT 
                                    table_name,
                                    table_type,
                                    table_schema
                                FROM information_schema.tables
                                WHERE table_schema = 'public'
                                ORDER BY table_name;
                                """
                            ))

    tables = [row[0] for row in result] # Show the first column

    if tables:
        for table in tables:
            print(f" - {table}")

    return tables


def if_table(table: str) -> bool:
    """ Checks if a table exists """

    with engine.connect() as connection:
        result = connection.execute(text(
            """
            SELECT EXISTS(
                    SELECT 1
                    FROM information_schema.tables
                    WHERE table_schema = 'public'
                    AND table_name = :table_name
                );
            """
            ), {"table_name": table}
        )

    return result.scalar()

def execute_statement(statement: str):
    """ Execute an SQL statement """

    with engine.connect() as connection:
        connection.execute(statement)
    print(f"Executed {statement[:50]}")



# TODO:

def backup_database():
    """Backup database to SQL file - useful before major changes"""
    pass

def get_table_row_counts():
    """Show how many records are in each table - useful for debugging"""
    pass

def truncate_all_tables():
    """Clear all data but keep table structure - useful for testing"""
    pass

def create_sample_data():
    """Insert test data - useful for development"""
    pass

def show_table_columns(table_name: str):
    """Show column details for a specific table"""
    pass

def show_foreign_keys():
    """List all foreign key relationships"""
    pass