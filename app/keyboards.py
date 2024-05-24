from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

from aiogram.utils.keyboard import InlineKeyboardBuilder
from app.database.requests import get_categories, get_category_article

main = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Статьи')],
                                     [KeyboardButton(text='Ситуации'),
                                      KeyboardButton(text='О боте')]
                                     ],
                           resize_keyboard=True,
                           input_field_placeholder='Выберите пункт меню...')

async def categories():
    all_categories = await get_categories()
    keyboard = InlineKeyboardBuilder()
    for category in all_categories:
        keyboard.add(InlineKeyboardButton(text=category.name, callback_data=f"category_{category.id}"))
    return keyboard.adjust(2).as_markup()


async def articles(category_id):
    all_items = await get_category_article(category_id)
    keyboard = InlineKeyboardBuilder()
    for item in all_items:
        keyboard.add(InlineKeyboardButton(text=item.number, callback_data=f"item_{item.id}"))
    return keyboard.adjust(3).as_markup()