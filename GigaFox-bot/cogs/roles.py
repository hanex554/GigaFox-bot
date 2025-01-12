import disnake
from disnake.ext import commands

# Проверка разрешения для управления ролями
def can_manage_roles(ctx):
    return ctx.author.guild_permissions.manage_roles

class RoleCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(
        name="роль",
        description="Управление ролями пользователя"
    )
    async def role_command(self, ctx: disnake.ApplicationCommandInteraction):
        pass  # Этот метод служит контейнером для подкоманд

    @role_command.sub_command(
        name="добавить",
        description="Добавить роль пользователю"
    )
    @commands.check(can_manage_roles)
    async def add_role(self, ctx: disnake.ApplicationCommandInteraction, member: disnake.Member,
                            role: disnake.Role):
        await self.process_role(ctx, member, role, "added")

    @role_command.sub_command(
        name="снять",
        description="Снять роль у пользователя"
    )
    @commands.check(can_manage_roles)
    async def remove_role(self, ctx: disnake.ApplicationCommandInteraction, member: disnake.Member,
                          role: disnake.Role):
        await self.process_role(ctx, member, role, "removed")

    @role_command.sub_command(
        name="изменить_цвет",
        description="Изменить цвет роли"
    )
    @commands.check(can_manage_roles)
    async def change_role_color(self, ctx: disnake.ApplicationCommandInteraction, role: disnake.Role, color: str):
        # Проверка, что цвет в правильном формате
        if not color.startswith("#") or len(color) != 7:
            await ctx.response.send_message("Цвет должен быть в формате #RRGGBB.", ephemeral=True)
            return
        
        try:
            # Изменяем цвет роли
            await role.edit(color=disnake.Color(int(color[1:], 16)))

            embed = disnake.Embed(
                title="Цвет роли изменен",
                description=f"Цвет роли {role.name} был успешно изменен на {color}.",
                color=disnake.Color.green()
            )
            await ctx.response.send_message(embed=embed)

        except disnake.errors.Forbidden:
            await self.send_error(ctx, "У меня нет прав для изменения цвета роли.")
        except Exception as e:
            await self.send_error(ctx, f"Произошла ошибка при изменении цвета роли: {e}")

    async def process_role(self, ctx, member, role, action):
        # Проверяем права бота и валидность роли
        if not ctx.guild.me.guild_permissions.manage_roles:
            await ctx.response.send_message("У меня нет прав для управления ролями.", ephemeral=True)
            return

        if (action == "added" and role >= ctx.guild.me.top_role) or (action == "removed" and role >= ctx.author.top_role):
            await ctx.response.send_message(
                f"Я не могу {action} эту роль, так как она выше моей самой высокой роли.",
                ephemeral=True)
            return

        if member == ctx.author and action == "added":
            await ctx.response.send_message("Вы не можете добавить себе роль.", ephemeral=True)
            return

        # Пытаемся добавить или снять роль
        try:
            if action == "added":
                await member.add_roles(role)
            else:
                await member.remove_roles(role)

            embed = disnake.Embed(
                title=f"Role {action}",
                description=f"Роль {role.name} была успешно {action} пользователю {member.mention}.",
                color=disnake.Color.green()
            )
            await ctx.response.send_message(embed=embed)
        except disnake.errors.Forbidden:
            await self.send_error(ctx, f"У меня нет прав для {action} этой роли.")
        except Exception as e:
            await self.send_error(ctx, f"Произошла ошибка при {action} роли: {e}")

    @staticmethod
    async def send_error(ctx, message):
        embed = disnake.Embed(
            title="Error",
            description=message,
            color=disnake.Color.red()
        )
        await ctx.response.send_message(embed=embed, ephemeral=True)

# Добавление расширения к боту
def setup(bot):
    bot.add_cog(RoleCog(bot))