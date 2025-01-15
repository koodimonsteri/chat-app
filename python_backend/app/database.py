from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
import settings

engine = create_engine(settings.DB_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
