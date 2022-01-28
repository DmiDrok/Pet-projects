from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import emoji

##Кнопки на /start, /help
help_city_onclick = InlineKeyboardButton(f"Подсказка", callback_data="help")
replace_city_onclick = InlineKeyboardButton(f"Замена города", callback_data="replace")

frame_start_buttons = InlineKeyboardMarkup().add(replace_city_onclick).insert(help_city_onclick)