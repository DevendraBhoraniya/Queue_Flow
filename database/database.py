from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
import os
from dotenv import load_dotenv

# Load the .env file 
load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')


# Create the engine to interact with the database
engine = create_engine(DATABASE_URL)

# Create a session factory to manage transactions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class that our database models will inherit from
Base = declarative_base()

# Dependency injector to pass database sessions to our API routes
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()