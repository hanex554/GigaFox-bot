import disnake
from disnake.ext import commands

class Kick(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(
        name="выгнать",
        description="Выгнать участника сервера",
    )
    async def kick(self, ctx, member: disnake.Member):
        # Проверяем, есть ли у пользователя права на кик участников
        if not ctx.author.guild_permissions.kick_members:
            embed = disnake.Embed(
                title="Недостаточно прав",
                description="У вас нет прав на кик участников.",
                color=disnake.Color.red()
            )
            await ctx.send(embed=embed)
            return

        # Проверяем, есть ли участник на сервере
        if member not in ctx.guild.members:
            embed = disnake.Embed(
                title="Ошибка",
                description=f"Участник {member.display_name} не найден на сервере.",
                color=disnake.Color.red()
            )
            await ctx.send(embed=embed)
            return

        reason = "Не указана"  # Здесь можно указать причину, если нужно

        try:
            # Попытка отправить личное сообщение пользователю
            await member.send(f"Вы были выгнаны из сервера '{ctx.guild.name}' по причине: {reason}")
        except disnake.HTTPException:
            # Не удалось отправить сообщение
            await ctx.send(
                f"Не удалось отправить личное сообщение {member.display_name}. Возможно, он отключил личные сообщения.")

        # Кик участника
        await member.kick(reason=reason)
        embed = disnake.Embed(
            title="Участник выгнан",
            description=f"{member.display_name} был выгнан из сервера '{ctx.guild.name}' по причине: {reason}",
            color=disnake.Color.red()
        )
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Kick(bot))
