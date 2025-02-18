from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DB_URL = "sqlite:///db/database.db"
engine = create_engine(DB_URL, echo=True)  # noqa: F811
Session = sessionmaker(engine)
