import disnake
from disnake.ext import commands
from disnake import Embed


class BlockUnblock(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(
        name="блок",
        description="Заблокировать канал для отправки сообщений."
    )
    async def block(self, ctx):
        """Команда для блокировки канала."""
        await self.set_channel_permission(ctx, block=True)

    @commands.slash_command(
        name="разблок",
        description="Разблокировать канал для отправки сообщений."
    )
    async def unblock(self, ctx):
        """Команда для разблокировки канала."""
        await self.set_channel_permission(ctx, block=False)

    @staticmethod
    async def set_channel_permission(ctx, block: bool):
        """Функция для установки прав канала: блокировка или разблокировка."""
        if ctx.author.guild_permissions.administrator:
            # Проверка, является ли канал текстовым
            channel = ctx.channel
            if isinstance(channel, disnake.TextChannel) or isinstance(channel, disnake.Thread):
                # Используйте родительский канал, если это тред
                parent_channel = channel if isinstance(channel, disnake.TextChannel) else channel.parent

                # Установка разрешений на уровень по умолчанию
                if block:
                    # Запретить отправку сообщений для роли @everyone
                    await parent_channel.set_permissions(ctx.guild.default_role, send_messages=False)
                    action = "заблокирован"
                    color = disnake.Color.red()
                else:
                    # Вернуть разрешения на уровень по умолчанию (разрешить отправку сообщений)
                    await parent_channel.set_permissions(ctx.guild.default_role, send_messages=None)
                    action = "разблокирован"
                    color = disnake.Color.green()

                embed_message = Embed(
                    title=f"Канал {action}",
                    description=f"Канал {parent_channel.mention} был {action}.",
                    color=color
                )
                await ctx.send(embed=embed_message)
            else:
                embed_message = Embed(
                    title="Ошибка",
                    description="Эта команда может быть использована только в текстовых каналах.",
                    color=disnake.Color.red()
                )
                await ctx.send(embed=embed_message, ephemeral=True)
        else:
            embed_message = Embed(
                title="Ошибка",
                description="У вас нет прав на выполнение этой команды.",
                color=disnake.Color.red()
            )
            await ctx.send(embed=embed_message, ephemeral=True)


def setup(bot):
    bot.add_cog(BlockUnblock(bot))
