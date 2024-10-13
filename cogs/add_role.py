import disnake
from disnake.ext import commands

# Проверка разрешения для управления ролями
def can_manage_roles(ctx):
    return ctx.author.guild_permissions.manage_roles

# Определение класса "RoleCog" как расширения бота
class RoleCog1(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(
        name="добавить_роль",
        description="Добавить роль пользователю"
    )
    @commands.check(can_manage_roles)
    async def add_role(self, ctx: disnake.ApplicationCommandInteraction, member: disnake.Member,
                            role: disnake.Role):
        await self.process_the_command(ctx, member, role, "added")

    @commands.slash_command(
        name="снять_роль",
        description="Снять роль у пользователя"
    )
    @commands.check(can_manage_roles)
    async def remove_role(self, ctx: disnake.ApplicationCommandInteraction, member: disnake.Member,
                         role: disnake.Role):
        await self.process_the_command(ctx, member, role, "removed")

    @staticmethod
    async def process_the_command(ctx, member, role, action):
        # Проверяем, может ли бот управлять ролями
        if not ctx.guild.me.guild_permissions.manage_roles:
            await ctx.response.send_message("У меня нет прав для управления ролями.", ephemeral=True)
            return

        # Проверяем, имеет ли бот право выполнить указанное действие с ролью
        if (action == "added" and role >= ctx.guild.me.top_role) or (
                action == "removed" and role >= ctx.author.top_role):
            await ctx.response.send_message(
                f"Я не могу выполнить это действие, так как указанная роль {action} выше моей самой высокой роли.",
                ephemeral=True)
            return

        # Проверяем, не является ли участник целью команды
        if member == ctx.author and action == "added":
            await ctx.response.send_message("Вы не можете добавить себе роль.", ephemeral=True)
            return

        # Пытаемся выполнить действие с ролью у пользователя
        try:
            if action == "added":
                await member.add_roles(role)
            elif action == "removed":
                await member.remove_roles(role)

            embed = disnake.Embed(
                title="Role " + action,
                description=f"Роль {role.name} была успешно {action} пользователю {member.mention}.",
                color=disnake.Color.green()
            )
            await ctx.response.send_message(embed=embed)
        except disnake.errors.Forbidden:
            embed = disnake.Embed(
                title="Error",
                description=f"У меня нет прав для {action} этой роли.",
                color=disnake.Color.red()
            )
            await ctx.response.send_message(embed=embed)
        except Exception as e:
            embed = disnake.Embed(
                title="Error",
                description=f"Произошла ошибка при {action} роли: {e}",
                color=disnake.Color.red()
            )
            await ctx.response.send_message(embed=embed)

# Добавление расширения к боту
def setup(bot):
    bot.add_cog(RoleCog1(bot))
