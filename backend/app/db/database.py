from sqlmodel import create_engine

DATABASE_URL = "sqlite:///./okcthunder.db"

engine = create_engine(DATABASE_URL, echo=True, connect_args={"check_same_thread": False})