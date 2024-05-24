from app.database.models import async_session
from app.database.models import User, Category, Article, Situation
from sqlalchemy import select


async def set_user(tg_id: int) -> None:
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        if not user:
            session.add(User(tg_id=tg_id))
            await session.commit()

async def get_categories():
    async with async_session() as session:
        return await session.scalars(select(Category))

async def get_category_article(category_id):
    async with async_session() as session:
        return await session.scalars(select(Article).where(Article.category == category_id))
async def get_article(article_id):
    async with async_session() as session:
        return await session.scalar(select(Article).where(Article.id == article_id))

async def get_situation(situation_id):
    async with async_session() as session:
        return await session.scalar(select(Situation).where(Situation.id == situation_id))

async def get_article_by_number(article_id):
    async with async_session() as session:
        return await session.scalar(select(Article).where(Article.id == article_id))

async def get_all_situations():
    async with async_session() as session:
        result = await session.execute(select(Situation))
        return result.scalars().all()