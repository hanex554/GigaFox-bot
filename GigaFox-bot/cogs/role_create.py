import disnake
from disnake.ext import commands

class Roles(commands.Cog):
    """Класс для управления ролями на сервере Discord."""

    def __init__(self, bot):
        """
        Инициализация класса Roles.

        :param bot: Экземпляр бота.
        """
        self.bot = bot

    @commands.slash_command(
        name="создать_роль",
        description="Создать новую роль на сервере с указанным цветом (HEX). Пример: #FF5733"
    )
    @commands.has_permissions(manage_roles=True)
    async def create_role(self, ctx: disnake.ApplicationCommandInteraction, название: str, цвет: str = None):
        """
        Создать новую роль на сервере.

        :param ctx: Контекст команды.
        :param название: Название создаваемой роли.
        :param цвет: Цвет роли в формате HEX (по умолчанию - стандартный цвет).
        """
        guild = ctx.guild

        # Проверка прав бота на создание ролей
        if not guild.me.guild_permissions.manage_roles:
            await ctx.response.send_message("У меня нет прав для создания ролей.", ephemeral=True)
            return

        try:
            # Обработка цвета
            if цвет:
                if цвет.startswith('#'):
                    цвет = цвет[1:]
                hex_int = int(цвет, 16)
                цвет_obj = disnake.Color(hex_int)
            else:
                цвет_obj = disnake.Color.default()  # Стандартный цвет

            # Создание роли
            новая_роль = await guild.create_role(name=название, color=цвет_obj)
            embed = disnake.Embed(
                title="Роль создана",
                description=f"Роль {новая_роль.mention} была успешно создана.",
                color=новая_роль.color
            )
            await ctx.response.send_message(embed=embed)

        except ValueError:
            await ctx.response.send_message(
                "Некорректный формат HEX-кода. Убедитесь, что он состоит из 6 символов (например, #FF5733).",
                ephemeral=True
            )
        except disnake.Forbidden:
            await ctx.response.send_message("У меня недостаточно прав для создания роли.", ephemeral=True)
        except commands.MissingPermissions:
            await ctx.response.send_message("У вас нет прав на создание ролей.", ephemeral=True)
        except Exception as e:
            await ctx.response.send_message(f"Произошла ошибка при создании роли: {e}", ephemeral=True)

def setup(bot):
    """Добавить класс Roles в бот."""
    bot.add_cog(Roles(bot))
