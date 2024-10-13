
import disnake
from disnake.ext import commands, tasks
import random

class StatusChanger(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.statuses = [
            "Влюблён в Hanex✨",
            "Фыр фыр фыр🦊",
            "Обожаю ночь⭐",
            "Фыр-фырные функции🌟",
            "UwU",
            "OwO",
            "Кушает ягоды🫐"
        ]
        self.current_statuses = self.statuses.copy()  # Копируем список статусов
        random.shuffle(self.current_statuses)  # Перемешиваем статусы
        self.change_status.start()  # Запускаем задачу смены статуса

    @tasks.loop(seconds=300)  # Указываем интервал смены статуса
    async def change_status(self):
        if not self.current_statuses:  # Если список статусов пуст
            self.current_statuses = self.statuses.copy()  # Обновляем его
            random.shuffle(self.current_statuses)  # Перемешиваем статусы

        status = self.current_statuses.pop(0)  # Берём первый статус из списка
        activity = disnake.Activity(type=disnake.ActivityType.playing, name=status)
        await self.bot.change_presence(activity=activity)

    @change_status.before_loop
    async def before_change_status(self):
        await self.bot.wait_until_ready()  # Ждём, пока бот будет готов

    def cog_unload(self):
        self.change_status.stop()  # Останавливаем задачу при выгрузке cog'а

def setup(bot):
    bot.add_cog(StatusChanger(bot))
