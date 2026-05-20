from config.settings import get_settings
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

configs = get_settings()

engine = create_engine(
    configs.database_url,
    echo=configs.database_echo,
    pool_pre_ping=True,
)

# Create a session factory bound to the engine
SessionLocal = sessionmaker(autocommit=False,autoflush=False, bind=engine)

# Create the base class for all ORM models
# The Base object serves as the parent for all database models you define in your application.
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try :
        yield db
    finally:
        db.close()
