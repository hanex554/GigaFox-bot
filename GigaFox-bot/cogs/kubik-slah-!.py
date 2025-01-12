import disnake
from disnake.ext import commands
import random

class DiceCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def dice(self, ctx, sides: int = 6):
        """Кидает кубик с указанным количеством граней и выводит результат в текстовом формате."""
        if sides < 2:
            await ctx.send("Количество граней должно быть как минимум 2.")
            return

        roll_result = random.randint(1, sides)

        # Генерируем случайный цвет для встроенного сообщения
        random_color = disnake.Color.from_rgb(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

        embed_message = disnake.Embed(
            title=f"Бросок кубика ({sides} граней)",
            description=f"Выпало: {roll_result}",
            color=random_color  # Используем случайный цвет здесь
        )

        await ctx.send(embed=embed_message)

    @commands.slash_command(
        name="кубик",
        description="Кидает кубик с указанным количеством граней.",
        options=[
            disnake.Option(
                name="sides",
                description="Количество граней на кубике.",
                type=disnake.OptionType.integer,
                required=False,
                choices=[
                    disnake.OptionChoice(name="6 граней", value=6),
                    disnake.OptionChoice(name="10 граней", value=10),
                    disnake.OptionChoice(name="20 граней", value=20),
                ]
            )
        ]
    )
    async def dice_slash(self, ctx, sides: int = None):
        """Кидает кубик с указанным количеством граней и выводит результат во встроенном сообщении."""
        if sides is None:
            sides = 6  # По умолчанию 6 граней, если пользователь не выбрал

        if sides < 2:
            await ctx.send("Количество граней должно быть как минимум 2.")
            return

        roll_result = random.randint(1, sides)

        # Генерируем случайный RGB цвет для встроенного сообщения
        random_color = disnake.Color.from_rgb(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

        embed_message = disnake.Embed(
            title=f"Бросок кубика ({sides} граней)",
            description=f"Выпало: {roll_result}",
            color=random_color  # Используем случайный цвет здесь
        )

        await ctx.send(embed=embed_message)

def setup(bot):
    bot.add_cog(DiceCog(bot))
