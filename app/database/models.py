from sqlalchemy import BigInteger, String, ForeignKey, Integer
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine

engine = create_async_engine(url='sqlite+aiosqlite:///db.sqlite3')

async_session = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id = mapped_column(BigInteger)


class Category(Base):
    __tablename__ = 'categories'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(25))


class Article(Base):
    __tablename__ = 'articles'

    id: Mapped[int] = mapped_column(primary_key=True)
    number: Mapped[str] = mapped_column(String(25))
    name: Mapped[str] = mapped_column(String(120))
    description: Mapped[str] = mapped_column(String(255))
    category: Mapped[int] = mapped_column(ForeignKey('categories.id'))

class Situation(Base):
    __tablename__ = 'situations'

    id: Mapped[int] = mapped_column(primary_key=True)
    situation: Mapped[str] = mapped_column(String(25))
    article_id: Mapped[str] = mapped_column(String(120))
    penalty: Mapped[int] = mapped_column(Integer) 

async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
