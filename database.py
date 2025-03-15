from sqlalchemy import create_engine, Column, Integer, Float
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv, dotenv_values

# loading variables from .env file
load_dotenv() 

# accessing and printing value
username = os.getenv("MYSQL_USERNAME")
password = os.getenv("MYSQL_PASSWORD")
sql_host = os.getenv("MYSQL_HOST")
database = os.getenv("MYSQL_DATABASE")




DATABASE_URL = f"mysql+pymysql://{username}:{password}@{sql_host}/{database}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class Prediction(Base):
    __tablename__ = "predictions"

    trip_id = Column(Integer, primary_key=True, index=True, autoincrement=True)  # Make trip_id the primary key
    user_id = Column(Integer, index=True)  # Keep user_id as an indexed column
    activity_code = Column(Integer, nullable=False)
    duration = Column(Float, nullable=False)
    carbon_footprint = Column(Float, nullable=False)


def init_db():
    Base.metadata.create_all(bind=engine)
