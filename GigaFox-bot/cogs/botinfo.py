import disnake
from disnake.ext import commands
import datetime


class BotInfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.start_time = datetime.datetime.now(datetime.UTC)  # Время запуска бота в UTC

    @commands.slash_command(
        name="информация",
        description="Получить информацию о боте")
    async def information(self, inter: disnake.ApplicationCommandInteraction):
        # Получаем информацию о пользователе
        user_id = 1227009761438990387  # ID пользователя
        user = await self.bot.fetch_user(user_id)  # Получаем пользователя по ID

        user_nickname = str(user)  # Ник и ID
        user_avatar_url = user.avatar.url if user.avatar else None  # Фото профиля

        # Подсчет общего количества участников
        total_members = sum(guild.member_count for guild in self.bot.guilds)

        # Создаем Embed
        embed = disnake.Embed(
            title="Информация о боте",
            color=disnake.Color.blue(),
            description="Узнайте больше о GigaFox!"
        )
        embed.add_field(name="Имя", value=self.bot.user.name, inline=True)
        embed.add_field(name="Серверов", value=len(self.bot.guilds), inline=True)
        embed.add_field(name="Участников", value=total_members, inline=True)

        # Время запуска в формате Discord
        unix_start_time = int(self.start_time.timestamp())  # Преобразуем в UNIX формат
        embed.add_field(name="Время запуска", value=f"<t:{unix_start_time}:R>", inline=True)

        embed.set_footer(text=f"С любовью от: {user_nickname}", icon_url=user_avatar_url)

        await inter.send(embed=embed)


def setup(bot):
    bot.add_cog(BotInfo(bot))
