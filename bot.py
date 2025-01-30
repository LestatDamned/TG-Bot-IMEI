import asyncio
import logging
from aiogram import Bot, Router, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message

from main import check_imei, imei_validator
from config import TELEGRAM_TOKEN, WHITELISTED_USER_IDS

logging.basicConfig(level=logging.INFO)


router = Router()

async def main():
    bot = Bot(token=TELEGRAM_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())

@router.message(Command("start"))
async def send_welcome(message: Message):
    """Команда /start для запуска бота"""

    await message.answer("Отправьте IMEI для проверки.")

@router.message(Command("id"))
async def send_id(msg: Message):
    """Команда /id для получения ID пользователя"""
    await msg.answer(f"Твой ID: {msg.from_user.id}")

@router.message(Command("add_to_whitelist"))
async def add_to_whitelist(msg: Message):
    """Команда /add_to_whitelist для добавления пользователя в белый список"""
    WHITELISTED_USER_IDS.add(msg.from_user.id)
    await msg.answer(f"Пользователь {msg.from_user.id} добавлен в белый список.")
    await msg.answer(f"Текущий белый список: {WHITELISTED_USER_IDS}")

@router.message()
async def handle_message(message: Message):
    """Принимает в чате IMEI код и делает проверку на участи в белом списке,
     валидирует IMEI, дальше отправляет запрос к API для получения информации"""
    if message.from_user.id not in WHITELISTED_USER_IDS:
        await message.answer(f"Вас нет в белом списке")
        return

    await message.answer(f'Вы ввели: {message.text}')
    imei = message.text.strip()
    try:
        imei_validator(imei)
    except ValueError as e:
        await message.answer(f'Ошибка {e}')

    else:
        result = await check_imei(imei)

        response = f"""IMEI: {result.get('properties', {}).get('imei')}
Название девайса: {result.get('properties', {}).get('deviceName')}
Сеть: {result.get('properties', {}).get('network', "Неизвестно")}
Режим потери: {result.get('properties', {}).get('lostMode', "Неизвестно")}
Ссылка на изображение девайса: {result.get('properties', {}).get('image')}"""

        await message.answer(response)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
