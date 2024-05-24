import random

from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command

import app.keyboards as kb
import app.database.requests as rq

router = Router()

@router.message(Command("start"))
async def cmnd_start(message: Message):
    await rq.set_user(message.from_user.id)
    await message.reply(f"Привет, <b>{message.from_user.first_name}</b>!\nЯ бот, который выдает статьи", parse_mode="HTML")
    await message.answer_sticker(sticker = "CAACAgIAAxkBAAEMKcFmTaRuiMhbuTABdGbJYWcH4SPkHAACwz0AAoz_4UrLoyLnP928EDUE")
    await message.answer('Выберите пункт меню:', reply_markup=kb.main)


@router.message(F.text == 'Статьи')
async def articles(message: Message):
    await message.answer('Выберите категорию:', reply_markup=await kb.categories())


@router.message(F.text == 'О боте')
async def about(message: Message):
    await message.reply(f"Бот умеет показывать статьи, демонстрировать ситуации")
    await message.answer_sticker(sticker="CAACAgIAAxkBAAEMKpVmTi9LhwcaCmsSNfAUTYOPQdPSKAACvT8AAv-V4EqkHgFrFCk9LzUE")


@router.message(F.text == 'Ситуации')
async def situations(message: Message):
    all_situations = await rq.get_all_situations()
    response_text = "Ситуации:\n"
    for index, item in enumerate(all_situations, start=1):
        response_text += f"{index}. {item.situation}\n"
    await message.answer(response_text)
    await message.answer(f"Напишите номер ситуации")
    await message.answer_sticker(sticker="CAACAgIAAxkBAAEMK5xmTwz2g8tZxpxp-NP1jltXwV-2CwACMz8AAn1D6Ep73nrP1PsJ2DUE")



@router.message(lambda message: message.text.isdigit())
async def send_situation_info(message: Message):
    situation_id = int(message.text)
    situation = await rq.get_situation(situation_id)
    if situation:
        article_id = situation.article_id
        article = await rq.get_article_by_number(article_id)
        if article:
            response_text = (f'<i>Ситуация:</i> {situation.situation}\n'
                             f'<i>Номер статьи:</i> {article.number}\n'
                             f'<i>Описание статьи:</i> {article.name}\n'
                             f'<i>Штраф:</i> {situation.penalty} ₽')
            await message.answer(response_text, parse_mode="HTML")
        else:
            await message.answer("Статья с таким номером не найдена.")
    else:
        await message.answer("Ситуация с таким номером не найдена.")


@router.callback_query(F.data.startswith('category_'))
async def category(callback: CallbackQuery):
    await callback.answer('Вы выбрали категорию')
    await callback.message.answer('Выберите статью по категории:', reply_markup=await kb.articles(callback.data.split('_')[1]))


@router.callback_query(F.data.startswith('item_'))
async def category(callback: CallbackQuery):
    article_data = await rq.get_article(callback.data.split('_')[1])
    await callback.message.answer('Вы выбрали статью:')
    await callback.message.answer(f'<i>Статья:</i> {article_data.number}\n\n<i>Название:</i> {article_data.name}\n\n<i>Описание:</i> {article_data.description}', parse_mode="HTML")
    await callback.message.answer('Выберите категорию:', reply_markup=await kb.categories())


@router.message()
async def echo(message: Message):
    # Список ответов на непонятные сообщения
    responses = ["Я не понял...", "Не понимаю...", "Я вас не понимаю..."]
    # Отправляем рандомный ответ
    await message.answer(random.choice(responses))