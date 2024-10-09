from aiogram.types import Message
from loader import dp
from aiogram.filters import Command
from keyboard_buttons.admin_keyboard import admin_button1

#help commands
@dp.message(Command("help"))
async def help_commands(message:Message):
    await message.answer("🤖 All Saver может скачать для вас видео ролики и аудио из\n популярных социальных сетей.\nКак пользоваться:\n 1. Зайдите в одну из социальных сетей.\n  2. Выберите интересное для вас видео.\n  3. Нажми кнопку «Скопировать».\n  4. Отправьте нашему боту и получите ваш файл!\nБот может скачивать с:\n1. TikTok (https://www.tiktok.com/)\n  2. YouTube (https://www.youtube.com/)\n 3. Pinterest (https://www.pinterest.com/)\n  4. Instagram (https://www.instagram.com/)\n\nЕсли возникла проблема с ботом, отправьте 👨‍💼Запрос администратору, нажав кнопку Запросить администратора.",reply_markup=admin_button1)
