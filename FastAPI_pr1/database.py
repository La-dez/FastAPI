from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQL_DB_URL = "sqlite:///./itproger.db"

engine = create_engine(SQL_DB_URL, connect_args={"check_same_thread": False})

session_local = sessionmaker(autoflush=False, autocommit=False, bind=engine) #autoflush - автоматически очищает сессию после каждого запроса (=false),
                                                                            # autocommit - автоматически фиксирует транзакцию после каждого запроса (=false)

Base = declarative_base()
