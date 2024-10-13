import disnake
from disnake.ext import commands

class ClearCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(
        name="очистить",
        description="Удалить сообщения из текущего канала",
    )
    async def clear(self, ctx, amount: int, target_user: str = None):
        # Проверка прав на управление сообщениями
        if not ctx.author.guild_permissions.manage_messages:
            await ctx.send(embed=self.error_embed("У вас нет разрешения на выполнение этой команды."), ephemeral=True)
            return

        # Проверка на валидность числа
        if not (0 < amount <= 100):
            await ctx.send("Введите количество сообщений от 1 до 100.", ephemeral=True)
            return

        # Проверка и преобразование target_user, если указан
        target_member = None
        if target_user:
            try:
                target_member = await commands.MemberConverter().convert(ctx, target_user)
            except commands.BadArgument:
                await ctx.send("Не удалось найти указанного пользователя.", ephemeral=True)
                return

        # Удаление сообщений по условию (если указан пользователь)
        deleted = await ctx.channel.purge(limit=amount, check=lambda msg: msg.author == target_member if target_member else True)

        # Создание embed с результатами очистки
        embed = disnake.Embed(
            title="Очистка сообщений",
            description=f"{ctx.author.mention} удалил {len(deleted)} сообщений.",
            color=disnake.Color.green(),
        )
        await ctx.send(embed=embed)

    @staticmethod
    def error_embed(description: str):
        return disnake.Embed(title="Ошибка", description=description, color=disnake.Color.red())

def setup(bot):
    bot.add_cog(ClearCog(bot))
