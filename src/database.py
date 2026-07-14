from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import registry

from src.settings import Settings

engine = create_async_engine(Settings().DATABASE_URL)

convention = {
    'ix': 'ix_%(column_0_label)s',
    'uq': 'uq_%(table_name)s_%(column_0_name)s',
    'ck': 'ck_%(table_name)s_%(constraint_name)s',
    'fk': 'fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s',
    'pk': 'pk_%(table_name)s',
}

table_registry = registry(metadata=MetaData(naming_convention=convention))


async def get_session():
    async with AsyncSession(engine, expire_on_commit=False) as session:
        yield session
