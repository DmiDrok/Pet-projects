import config
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

storage = MemoryStorage() ##Делаем хранилище

bot = Bot(config.TOKEN, parse_mode="HTML")
dp = Dispatcher(bot, storage=storage)

async def start_send_and_attach_help_commands(dp):
    ##Прикрепляем команды для удобства пользователя
    await dp.bot.set_my_commands([
        types.BotCommand("start", "Начать игру"),
        types.BotCommand("records", "Топ игроков"),
        types.BotCommand("statgame", "Статистика текущей игры"),
        types.BotCommand("rules", "Правила"),
        types.BotCommand("endgame", "Закончить игру"),
    ])

    ##Отсылаем сообщение админу, что бот запущен успешно
    await bot.send_message(config.admin_id, "Бот успешно запущен!")
    print("-----Бот успешно запущен и администратор уведомлён в личные сообщения.-----")

if __name__ == "__main__":
    from handlers import dp
    executor.start_polling(dp, on_startup=start_send_and_attach_help_commands, skip_updates=True)