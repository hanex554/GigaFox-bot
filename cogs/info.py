import disnake
from disnake.ext import commands

class BotInfoCog(commands.Cog):  # Исправил название класса
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(
        name="информация",
        description="Информация о боте GigaFox")
    async def info(self, ctx):  # Убрал префикс `bot_` у метода
        # Текст с информацией о боте GigaFox
        embed = disnake.Embed(
            title="Информация о GigaFox 🦊",
            description=(
                "GigaFox — это Discord-бот, разработанный для безопасного общения и развлечения на вашем сервере. "
                "Имя GigaFox происходит от комбинации слов 'Gigantic' и 'Fox', что подчёркивает его силу и функциональность.\n\n"
                "GigaFox использует кастомный API и написан с использованием библиотеки `Disnake` для обеспечения максимальной гибкости.\n\n"
                "Текущая версия бота — **1.0.3**.\n\n"
                "Этот проект не мог бы существовать без поддержки многочисленных участников, которые вносят вклад в его развитие. "
            ),
            color=disnake.Color.orange()
        )

        embed.set_footer(text="Связаться со мной можно по нику hanex554 в Discord")

        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(BotInfoCog(bot))
