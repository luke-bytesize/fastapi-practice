from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()

DATABASE_URL = "postgresql://user:password@localhost/dbname"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# FastAPI에서 DB 세션을 제공하기 위한 의존성 함수
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()