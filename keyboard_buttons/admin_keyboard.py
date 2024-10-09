from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

admin_button = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Количество пользователей"),
            KeyboardButton(text="Отправить рекламу"),
        ]
    ],
   resize_keyboard=True,
   input_field_placeholder="Выберите один из пунктов меню"
)

admin_button1 = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="👨‍💼Запрос администратору"),        
        ]      
    ],
  resize_keyboard=True
)
