# Импортируются необходимые модули
import os
import disnake
from disnake.ext import commands

# Создается объект intents, который включает все разрешения для бота,
# а также добавляются права администратора.
intents = disnake.Intents.all()

# Создается экземпляр класса Bot с префиксом команд "!" и указанными разрешениями.
bot = commands.Bot(
    command_prefix=["."],
    intents=intents
)
bot.remove_command('help')
# Определяется функция on_ready, которая будет вызываться, когда бот будет готов к использованию.
# В данном случае, она просто выводит сообщение "Bot is ready!" в консоль.
@bot.event
async def on_ready():
    print("Bot is ready!")

    """activity = disnake.Activity(type=disnake.ActivityType.playing, name="Влюблён в Hanex✨")
    await bot.change_presence(activity=activity) это на память"""

# При готовности бота, загружает расширения из папки "cogs"
for file in os.listdir("./cogs"):
    if file.endswith(".py"):
        bot.load_extension(f"cogs.{file[:-3]}")

# Запускается бот с помощью метода run, передавая ему токен для авторизации.
bot.run("TOKEN")