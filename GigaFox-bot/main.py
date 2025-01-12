import os
import disnake
import logging
from disnake.ext import commands
from logging.handlers import RotatingFileHandler
from datetime import datetime

# Создаем папку для логов, если она не существует
os.makedirs('logs', exist_ok=True)

# Формирование имени файла с датой и временем
log_filename = datetime.now().strftime("logs/bot_%Y-%m-%d_%H-%M.log")

# Настройка глобального логгера
logger = logging.getLogger('discord_bot')
logger.setLevel(logging.INFO)

# Добавляем ротацию логов - 5 MB на файл, сохраняем до 5 файлов
if not logger.handlers:
    file_handler = RotatingFileHandler(
        filename=log_filename,  # Путь к файлу лога с учетом даты и времени
        encoding='utf-8',
        mode='a',
        maxBytes=5 * 1024 * 1024,  # 5 MB
        backupCount=5  # Храним 5 файлов логов
    )
    file_handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
    logger.addHandler(file_handler)

    # Логи также выводятся в консоль
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
    logger.addHandler(console_handler)

# Создаем объект intents, который включает все разрешения для бота
intents = disnake.Intents.all()

# Создается экземпляр класса Bot с префиксом команд "." и указанными разрешениями.
bot = commands.Bot(
    command_prefix=["."],
    intents=intents
)
bot.remove_command('help')

# Логируем запуск бота
@bot.event
async def on_ready():
    logger.info(f"Бот {bot.user} готов к работе.")
    # Пример изменения статуса (оставлено в комментарии для памяти)
    """activity = disnake.Activity(type=disnake.ActivityType.playing, name="Влюблён в Hanex✨")
    await bot.change_presence(activity=activity)"""

# Логируем загрузку каждого Cog
for file in os.listdir("./cogs"):
    if file.endswith(".py"):
        try:
            bot.load_extension(f"cogs.{file[:-3]}")
            logger.info(f"Загружено расширение: {file}")
        except Exception as e:
            logger.error(f"Ошибка при загрузке {file}: {e}", exc_info=True)

# Логируем ошибки команд
@bot.event
async def on_command_error(ctx, error):
    logger.error(f"Ошибка в команде {ctx.command}: {error}", exc_info=True)
    await ctx.send(f"Произошла ошибка: {str(error)}")

# Запускается бот с помощью метода run, передавая ему токен для авторизации.
try:
    bot.run("TOKEN")
except Exception as e:
    logger.critical(f"Ошибка при запуске бота: {e}", exc_info=True)
