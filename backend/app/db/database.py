from sqlmodel import create_engine

# define the database connection string
DATABASE_URL = "sqlite:///./okcthunder.db"

# create the SQLAlchemy engine
# echo=True enables logging of all SQL statements
# connect_args={"check_same_thread": False} is used for SQLite to allow multiple threads to use the same connection
engine = create_engine(DATABASE_URL, echo=True, connect_args={"check_same_thread": False})