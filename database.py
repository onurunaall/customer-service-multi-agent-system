import sqlite3
import requests
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool
from langchain_community.utilities.sql_database import SQLDatabase

_CHINOOK_URL = "https://raw.githubusercontent.com/lerocha/chinook-database/master/ChinookDatabase/DataSources/Chinook_Sqlite.sql"

def get_engine_for_chinook_db():
    """
    Downloads the Chinook SQL schema and initializes an in-memory SQLite DB.
    Returns a SQLAlchemy engine bound to that DB.
    """
    # Download the Chinook database SQL script from the official repository
    try:
      response = requests.get(_CHINOOK_URL)
      sql_script = response.text
    except requests.exceptions.RequestException as e:
        print(f"Failed to download Chinook schema: {e}")
        raise
    
    # Create an in-memory SQLite database connection
    connection = sqlite3.connect(":memory:", check_same_thread=False)
    
    # Execute the SQL script to populate the database with sample data
    connection.executescript(sql_script)

    # Create a SQLAlchemy engine that uses the populated connection
    engine = create_engine(
        "sqlite://",
        creator=lambda: connection, # Function that returns the database connection
        poolclass=StaticPool, # Use StaticPool to maintain single connection
        connect_args={"check_same_thread": False} # Allow cross-thread usage
    )

    return engine
