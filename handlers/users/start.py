from aiogram.types import Message
from loader import dp,db
from aiogram.filters import CommandStart


@dp.message(CommandStart())
async def start_command(message:Message):
    full_name = message.from_user.full_name
    telegram_id = message.from_user.id
    try:
        db.add_user(full_name=full_name,telegram_id=telegram_id) #foydalanuvchi bazaga qo'shildi
        await message.answer(text="Привет! При помощи этого бота вы сможете скачивать из Inst, YouTube, TikTok, Likee и Pinterest.\n/help • О боте\n")
    except:
        await message.answer(text="Привет! При помощи этого бота вы сможете скачивать из Inst, YouTube, TikTok, Likee и Pinterest.\n/help • О боте\n")

