from sqlalchemy import create_engine
from models import Base
from sqlalchemy.orm import sessionmaker
from database import engine

DB_URL = 'sqlite:///db/database.db'
engine = create_engine(DB_URL, echo=True)
Session = sessionmaker(engine)

def create_db_and_tables() -> None:
    Base.metadata.create_all(engine)
 
 

with Session() as session:
	#какие-то операции с БД
 