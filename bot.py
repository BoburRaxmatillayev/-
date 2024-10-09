from loader import dp, bot, db, ADMINS
from aiogram import Bot, Dispatcher, types
from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, FSInputFile, InputMediaPhoto, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, ContentType
from aiogram.filters import CommandStart
import asyncio
import logging
import os
import sys
import handlers
from aiogram.utils.keyboard import InlineKeyboardBuilder
from menucommands.set_bot_commands import set_default_commands
from insta import insta_save
from tiktok import tiktok_save
from yt import youtube_save
from pinterest import pinterest_save
from aiogram.fsm.state import StatesGroup, State

#bot ishga tushganini xabarini yuborish
class AdminStates(StatesGroup):
    waiting_for_admin_message = State()
    waiting_for_reply_message = State()


# Initialize logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define admin states
class AdminStates(StatesGroup):
    waiting_for_admin_message = State()
    waiting_for_reply_message = State()

# Function to create inline keyboard for reply
def create_inline_keyboard(user_id):
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(
        text="Ответить",
        callback_data=f"reply:{user_id}"
    )

    return keyboard_builder.as_markup()


# Admin message handler
@dp.message(F.text == "👨‍💼Запрос администратору")
async def admin_message(message: Message, state: FSMContext):
    await message.answer("Отправить сообщение администратору:")
    await state.set_state(AdminStates.waiting_for_admin_message)

@dp.message(AdminStates.waiting_for_admin_message, F.content_type.in_([
    ContentType.TEXT, ContentType.AUDIO, ContentType.VOICE, ContentType.VIDEO,
    ContentType.PHOTO, ContentType.ANIMATION, ContentType.STICKER, 
    ContentType.LOCATION, ContentType.DOCUMENT, ContentType.CONTACT,
    ContentType.VIDEO_NOTE
]))
async def handle_admin_message(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    username = message.from_user.username
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name or ""  # Some users may not have a last name

    # Use username if available, otherwise use first name + last name
    if username:
        user_identifier = f"@{username}"
    else:
        user_identifier = f"{first_name} {last_name}".strip()  # Remove any extra spaces

    video_note = message.video_note
    inline_keyboard = create_inline_keyboard(user_id)
    for admin_id in ADMINS:
        try:
            if video_note:
                print('adfs', message.video_note.file_id)
                # Echo the video note back to the user
                await bot.send_video_note(
                    admin_id,
                    video_note.file_id,
                    reply_markup=inline_keyboard
                )
            elif message.text:
                await bot.send_message(
                    admin_id,
                    f"Пользователь: {user_identifier}\nСообщение:\n{message.text}",
                    reply_markup=inline_keyboard
                )
            elif message.audio:
                await bot.send_audio(
                    admin_id,
                    message.audio.file_id,
                    caption=f"Пользователь: {user_identifier}\nАудио сообщение",
                    reply_markup=inline_keyboard
                )
            elif message.voice:
                await bot.send_voice(
                    admin_id,
                    message.voice.file_id,
                    caption=f"Пользователь: {user_identifier}\nГолосовое сообщение",
                    reply_markup=inline_keyboard
                )
            elif message.video:
                await bot.send_video(
                    admin_id,
                    message.video.file_id,
                    caption=f"Пользователь: {user_identifier}\nВидео сообщение",
                    reply_markup=inline_keyboard
                )
            elif message.photo:
                await bot.send_photo(
                    admin_id,
                    message.photo[-1].file_id,  # using the highest resolution photo
                    caption=f"Пользователь: {user_identifier}\nСообщение с фото",
                    reply_markup=inline_keyboard
                )
            elif message.animation:
                await bot.send_animation(
                    admin_id,
                    message.animation.file_id,
                    caption=f"Пользователь: {user_identifier}\nGIF сообщение",
                    reply_markup=inline_keyboard
                )
            elif message.sticker:
                await bot.send_sticker(
                    admin_id,
                    message.sticker.file_id,
                    reply_markup=inline_keyboard
                )
            elif message.location:
                await bot.send_location(
                    admin_id,
                    latitude=message.location.latitude,
                    longitude=message.location.longitude,
                    reply_markup=inline_keyboard
                )
            elif message.document:
                await bot.send_document(
                    admin_id,
                    message.document.file_id,
                    caption=f"Пользователь: {user_identifier}\nСообщение с документом",
                    reply_markup=inline_keyboard
                )
            elif message.contact:
                await bot.send_contact(
                    admin_id,
                    phone_number=message.contact.phone_number,
                    first_name=message.contact.first_name,
                    last_name=message.contact.last_name or "",
                    reply_markup=inline_keyboard
                )
        except Exception as e:
            logging.error(f"Error sending message to admin {admin_id}: {e}")

    await state.clear()
    await bot.send_message(user_id, "Администратор может вам ответить.")

# Callback query handler for the reply button
@dp.callback_query(lambda c: c.data.startswith('reply:'))
async def process_reply_callback(callback_query: CallbackQuery, state: FSMContext):
    user_id = int(callback_query.data.split(":")[1])
    await callback_query.message.answer("Напишите свой ответ. Ваш ответ будет отправлен пользователю.")
    await state.update_data(reply_user_id=user_id)
    await state.set_state(AdminStates.waiting_for_reply_message)
    await callback_query.answer()

# Handle admin reply and send it back to the user
@dp.message(AdminStates.waiting_for_reply_message)
async def handle_admin_reply(message: Message, state: FSMContext):
    data = await state.get_data()
    original_user_id = data.get('reply_user_id')

    if original_user_id:
        try:
            if message.text:
                await bot.send_message(original_user_id, f"Ответ администратора:\n{message.text}")
            elif message.voice:
                await bot.send_voice(original_user_id, message.voice.file_id)

            elif message.video_note:
                await bot.send_video_note(original_user_id, message.video_note.file_id)

            elif message.audio:
                await bot.send_audio(original_user_id, message.audio.file_id)
            
            elif message.sticker:
                await bot.send_sticker(original_user_id, message.sticker.file_id)
            
            elif message.video:
                await bot.send_video(original_user_id, message.video.file_id)

            await bot.send_message(ADMINS[0], "Ваше сообщение было отправлено пользователю!!!")            
            await state.clear()  # Clear state after sending the reply
        except Exception as e:
            logger.error(f"Error sending reply to user {original_user_id}: {e}")
            await message.reply("Ошибка: Произошла ошибка при отправке ответа.")
    else:
        await message.reply("Ошибка: ID пользователя для отправки ответа не найден.")

@dp.startup()
async def on_startup_notify(bot: Bot):
    for admin in ADMINS:
        try:
            await bot.send_message(chat_id=int(admin),text="Бот запущен")
        except Exception as err:
            logging.exception(err)

#bot ishdan to'xtadi xabarini yuborish
@dp.shutdown()
async def off_startup_notify(bot: Bot):
    for admin in ADMINS:
        try:
            await bot.send_message(chat_id=int(admin),text="Бот остановлен!")
        except Exception as err:
            logging.exception(err)

@dp.message(F.text.contains("yout"))
async def video_yuklash(message: Message):
    link = message.text
    try:
        loading_message = await message.answer("Видео загружается...✍️💬")
        yuklangan_video = youtube_save(link)
        await loading_message.delete()
        await message.answer_video(video=yuklangan_video)
    except Exception as e:
        await message.reply("Извините, произошла ошибка при загрузке ссылки.")

@dp.message(F.text.contains("instagram"))
async def instagram_download(message:Message):
    link = message.text
    loading_message = await message.answer("Данные загружаются...✍️💬")
    instagram = insta_save(link)
    await loading_message.delete()
    video = instagram.get("video")
    rasmlar = instagram.get("images")
    if rasmlar:
        rasm = []
        for i, r in enumerate(rasmlar):
            rasm.append(InputMediaPhoto(media=r))
            if (i + 1) % 10 == 0:
                await message.answer_media_group(rasm)
                rasm = []
        if rasm:
            await message.answer_media_group(rasm)
    if video:
        await message.answer_video(video=video)

@dp.message(F.text.contains("tiktok"))
async def tiktok_download(message: Message):
    link = message.text
    loading_message = await message.answer("Данные загружаются...✍️💬")
    tiktok_data = tiktok_save(link)  # TikTok ma'lumotlarini olish
    await loading_message.delete()
    video = tiktok_data.get("video")
    music = tiktok_data.get("music")
    rasmlar = tiktok_data.get("images")
    
    # Отправка изображений
    if rasmlar: 
        rasm = []
        for i, r in enumerate(rasmlar):
            if not r.startswith("http"):
                print(f"URL изображения неверен: {r}")
                continue
            rasm.append(InputMediaPhoto(media=r))
            if (i + 1) % 10 == 0:
                await message.answer_media_group(rasm)
                rasm = []
        if rasm:
            await message.answer_media_group(rasm)
    
    # Отправка видео
    if video:
        if not video.startswith("http"):
            print(f"URL видео неверен: {video}")
        else:
            await message.answer_video(video=video)
    
    # Отправка аудио
    if music: 
        if not music.startswith("http"):
            print(f"URL аудио неверен: {music}")
        else:
            await message.answer_audio(audio=music)
    
@dp.message(F.text.contains("pin"))
async def pinterest_download(message:Message):
    link = message.text
    try:
        loading_message = await message.answer("Загрузка данных...✍️💬")
        download_link = pinterest_save(link)
        await loading_message.delete()
        await message.reply(f"Вот ссылка для скачивания: {download_link}")
    except Exception as e:
        await message.reply("Извините, произошла ошибка при загрузке ссылки.")

def setup_middlewares(dispatcher: Dispatcher, bot: Bot) -> None:
    """MIDDLEWARE"""
    from middlewares.throttling import ThrottlingMiddleware

    # Классическая внутренняя промежуточная программа для защиты от спама. Основное время между запросами 0,5 секунд.
    dispatcher.message.middleware(ThrottlingMiddleware(slow_mode_delay=0.5))

async def main() -> None:
    await set_default_commands(bot)
    db.create_table_users()
    setup_middlewares(dispatcher=dp, bot=bot)
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)

    asyncio.run(main())
