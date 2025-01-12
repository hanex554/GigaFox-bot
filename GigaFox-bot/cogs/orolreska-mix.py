import disnake
from disnake.ext import commands
import random

class CoinCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(
        name="монетка",
        description="Игра в орла и решку.",
        options=[
            disnake.Option(
                name="choice",
                description="Ваш выбор: орел или решка.",
                type=disnake.OptionType.string,
                required=False,
                choices=[
                    disnake.OptionChoice(name="Орел 🦅", value="Орел 🦅"),
                    disnake.OptionChoice(name="Решка 🪙", value="Решка 🪙"),
                ]
            )
        ]
    )
    async def coin_slash(self, ctx, choice: str = None):
        """Игра в орла и решку с выбором."""
        choices = ["Орел 🦅", "Решка 🪙"]
        result = random.choice(choices)

        if choice:
            if choice == result:
                outcome = f"Вы выбрали: {choice}. Поздравляем, вы угадали!"
            else:
                outcome = f"Вы выбрали: {choice}. К сожалению, выпало {result}."
        else:
            outcome = f"Монета выпала: {result}"

        # Создаем embed для отображения результата
        embed = disnake.Embed(
            title="Игра в орла и решку",
            description=outcome,
            color=disnake.Color.random()
        )

        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(CoinCog(bot))
