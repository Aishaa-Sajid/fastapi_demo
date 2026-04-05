from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from src.database.config import SQLALCHEMY_DATABASE_URL, settings

# factory engine _ main connection gateway to database
engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL,
    echo=settings.echo_sql,
    pool_pre_ping=True,
)

# session factory _ creates database sessions
SessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
)
