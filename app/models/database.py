from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from config.database import DatabaseConfig

db_config = DatabaseConfig()

if not db_config.url:
    db_config.url = f'postgresql://{db_config.username}{":" + db_config.password if db_config.password else ""}@{db_config.host}{":" + str(db_config.port) if db_config.port else ""}/{db_config.database}'

engine = create_engine(db_config.url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
