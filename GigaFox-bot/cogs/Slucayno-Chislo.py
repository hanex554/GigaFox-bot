import disnake
from disnake.ext import commands
import random

class RandomNumberCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(
        name='случайно',
        description='Генерирует случайное число в заданном диапазоне.'
    )
    async def random_number_slash(self, ctx, min_value: int, max_value: int):
        await self.random_number(ctx, min_value, max_value)

    @commands.command(
        name='случайно',
        description='Генерирует случайное число в заданном диапазоне.'
    )
    async def random_number_command(self, ctx, min_value: int, max_value: int):
        await self.random_number(ctx, min_value, max_value)

    @staticmethod
    async def random_number(ctx, min_value: int, max_value: int):
        if min_value >= max_value:
            await ctx.send("Минимальное значение должно быть меньше максимального значения.")
            return

        random_number = random.randint(min_value, max_value)

        embed_message = disnake.Embed(
            title=f'Случайное число ({min_value} - {max_value})',
            description=str(random_number),
            color=disnake.Color.random()
        )

        await ctx.send(embed=embed_message)

def setup(bot):
    bot.add_cog(RandomNumberCog(bot))
