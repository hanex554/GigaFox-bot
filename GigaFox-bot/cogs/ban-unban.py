import disnake
from disnake.ext import commands
from typing import Literal


# Функция для отправки сообщения пользователю о бане
async def send_ban_notification(user, guild, reason):
    ban_embed = disnake.Embed(
        title="🚫 Уведомление о бане",
        description=f"Уважаемый(ая) {user.mention},",
        color=disnake.Colour.red()
    )

    if user.avatar:
        ban_embed.set_thumbnail(url=user.avatar.url)

    if reason:
        ban_embed.add_field(name="**Причина бана**", value=reason, inline=False)

    ban_embed.add_field(
        name="**Уведомление от администрации**",
        value=(
            f"С сожалением, мы вынуждены вас уведомить о том, что вы были заблокированы на сервере "
            f"**{guild.name}**.\n\n"
            "Если у вас есть вопросы или вы хотите подать апелляцию, "
            "свяжитесь с администрацией."
        ),
        inline=False
    )

    try:
        await user.send(embed=ban_embed)
    except disnake.errors.Forbidden:
        pass


# Функция для создания Embed с информацией о бане/разбане
def create_action_embed(user, action, guild, author=None, reason=None, delete_days=None):
    color = disnake.Color.red() if action == "забанен" else disnake.Color.green()
    embed = disnake.Embed(
        title=f"Пользователь {action}",
        description=f"{user.mention} был успешно {action} на сервере {guild.name}.",
        color=color
    )

    if author and author.avatar:
        embed.set_footer(text=f"Действие выполнено: {author.display_name}", icon_url=author.avatar.url)
    elif author:
        embed.set_footer(text=f"Действие выполнено: {author.display_name}")
    else:
        embed.set_footer(text="Действие выполнено: Неизвестный пользователь")

    if reason:
        embed.add_field(name="**Причина**", value=reason, inline=False)

    if action == "забанен" and delete_days:
        embed.add_field(
            name="**Сообщения удалены за последние дни**",
            value=f"{delete_days} дней",
            inline=False
        )

    return embed


# Функция для выполнения бана
async def ban(ctx, user, reason, delete_days):
    if user.id == ctx.author.id:
        raise commands.CommandError("Вы не можете забанить самого себя.")

    await send_ban_notification(user, ctx.guild, reason)

    try:
        await ctx.guild.ban(user, reason=reason, clean_history_duration=delete_days)
    except disnake.errors.Forbidden:
        raise commands.CommandError("Не удалось забанить пользователя. У бота нет прав.")

    embed = create_action_embed(user, "забанен", ctx.guild, ctx.author, reason, delete_days)
    if isinstance(ctx, disnake.ApplicationCommandInteraction):
        await ctx.response.send_message(embed=embed)
    else:
        await ctx.send(embed=embed)


# Функция для выполнения разбана
async def unban(ctx, user):
    try:
        await ctx.guild.unban(user)
        embed = create_action_embed(user, "разбанен", ctx.guild, ctx.author)
        if isinstance(ctx, disnake.ApplicationCommandInteraction):
            await ctx.response.send_message(embed=embed, ephemeral=True)
        else:
            await ctx.send(embed=embed)
    except disnake.NotFound:
        raise commands.CommandError("Указанный пользователь не найден или не был забанен.")
    except disnake.Forbidden:
        raise commands.CommandError("У меня нет прав на разблокировку пользователей.")


# Класс для управления баном/разбаном
class Ban(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="бан", description="Забанить пользователя на сервере")
    async def ban_command(self, ctx: disnake.MessageCommandInteraction, user: disnake.User, reason: str = None,
                          delete_days: Literal[0, 1, 2, 3, 4, 5, 6, 7] = 0):
        if not ctx.author.guild_permissions.ban_members:
            await ctx.send("У вас нет прав на выполнение этой команды.")
            return

        try:
            await ban(ctx, user, reason, delete_days)
        except commands.CommandError as e:
            await ctx.send(str(e))

    @commands.slash_command(name="бан", description="Забанить пользователя на сервере")
    async def ban_slash(self, ctx: disnake.ApplicationCommandInteraction, user: disnake.User, reason: str = None,
                        delete_days: Literal[0, 1, 2, 3, 4, 5, 6, 7] = 0):
        if not ctx.author.guild_permissions.ban_members:
            await ctx.response.send_message("У вас нет прав на выполнение этой команды.", ephemeral=True)
            return

        try:
            await ban(ctx, user, reason, delete_days)
        except commands.CommandError as e:
            await ctx.response.send_message(str(e), ephemeral=True)

    @commands.command(name="разбан", description="Разбанить указанного пользователя на сервере")
    async def unban_command(self, ctx, user: disnake.User = None):
        if not ctx.author.guild_permissions.ban_members:
            await ctx.send("У вас нет прав на выполнение этой команды.")
            return

        if user is None:
            await ctx.send("Вы должны указать пользователя для разбана.")
            return

        try:
            await unban(ctx, user)
        except commands.CommandError as e:
            await ctx.send(str(e))

    @commands.slash_command(name="разбан", description="Разбанить указанного пользователя на сервере")
    async def unban_slash(self, ctx, user: disnake.User):
        if not ctx.author.guild_permissions.ban_members:
            await ctx.response.send_message("У вас нет прав на выполнение этой команды.", ephemeral=True)
            return

        try:
            await unban(ctx, user)
        except commands.CommandError as e:
            await ctx.response.send_message(str(e), ephemeral=True)


# Функция setup для добавления COG
def setup(bot):
    bot.add_cog(Ban(bot))
