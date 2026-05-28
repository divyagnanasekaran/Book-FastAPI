# from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker

# # SQLALCHEMY_DATABASE_URL = "sqlite:///./books.db"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@host/dbname"


# engine = create_engine(
#     SQLALCHEMY_DATABASE_URL,
#     connect_args={"check_same_thread": False}
# )

# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base = declarative_base()

#postgresql://book_postgre_api_user:veXqxZSNBNgnsSy2mskUZZuOREExcf9c@dpg-d8c48c4p3tds73avg9ag-a/book_postgre_api
# import os
# from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker

# # Reads the Render environment variable, falls back to local sqlite if not found
# DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./local.db")

# # Render uses 'postgresql://', but SQLAlchemy 1.4+ sometimes requires 'postgresql+psycopg2://'
# if DATABASE_URL.startswith("postgresql://"):
#     DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+psycopg2://", 1)

# engine = create_engine(DATABASE_URL)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Base = declarative_base()

import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 1. Look for the Render database string. If not found, use a local fallback.
DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL:
    # Render provides 'postgresql://', but SQLAlchemy 1.4+ requires 'postgresql+psycopg2://'
    if DATABASE_URL.startswith("postgresql://"):
        DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+psycopg2://", 1)
else:
    # Fallback to local SQLite if running on your machine for testing
    DATABASE_URL = "sqlite:///./local.db"

# 2. Create the engine
# SQLite needs 'connect_args', but PostgreSQL will error out if it's included.
if "sqlite" in DATABASE_URL:
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
else:
    engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
