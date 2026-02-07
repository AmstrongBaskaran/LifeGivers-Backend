from dotenv import load_dotenv
import os
from sqlalchemy.orm import sessionmaker,declarative_base
from sqlalchemy import create_engine

load_dotenv()
engine = create_engine(os.getenv("DB_URL"))
sessionLocal = sessionmaker(autoflush=False,autocommit=False,bind=engine)
Base = declarative_base()

def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()