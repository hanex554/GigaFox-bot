import disnake
from disnake.ext import commands
from typing import Literal


async def ban(ctx, user, reason, delete_messages, delete_days):
    # Проверяем, имеет ли участник, выполняющий команду, разрешение на Бан пользователей
    if not ctx.author or not ctx.author.guild_permissions.ban_members:
        raise commands.CommandError(
            "У вас нет необходимых разрешений для бана участников. "
            "Пожалуйста, свяжитесь с администратором сервера, чтобы получить соответствующие разрешения."
        )

    # Проверяем, не пытается ли пользователь забанить самого себя
    if user.id == ctx.author.id:
        raise commands.CommandError("Вы не можете забанить самого себя.")

    # Создаем текстовое embed сообщение для уведомления о бане
    ban_embed = disnake.Embed(
        title="🚫 Уведомление о бане",
        description=f"Уважаемый(ая) {user.mention},",
        color=disnake.Colour.red()  # Красный цвет
    )

    # Check if user has an avatar before setting it as the thumbnail URL
    if user.avatar:
        ban_embed.set_thumbnail(url=user.avatar.url)

    # Check if ctx.author is not None before using its attributes
    if ctx.author and ctx.author.avatar:
        ban_embed.set_footer(text=f"Выдал бан: {ctx.author.display_name}", icon_url=ctx.author.avatar.url)
    elif ctx.author:
        ban_embed.set_footer(text=f"Выдал бан: {ctx.author.display_name}")
    else:
        ban_embed.set_footer(text="Выдал бан: Неизвестный пользователь")

    if reason:
        ban_embed.add_field(name="**Причина бана**", value=reason, inline=False)

    ban_embed.add_field(
        name="**Уведомление от администрации**",
        value=(
            f"С сожалением, мы вынуждены вас уведомить о том, что вы были заблокированы на сервере "
            f"**{ctx.guild.name}**.\n\n"
            "Если у вас есть какие-либо вопросы или вы хотите подать апелляцию на это решение, "
            "пожалуйста, свяжитесь с администрацией сервера для получения дополнительной информации и разъяснений."
        ),
        inline=False
    )

    # Попытка отправить сообщение пользователю, игнорируя ошибку
    try:
        await user.send(embed=ban_embed)
    except disnake.errors.Forbidden:
        pass  # Пропускаем ошибку и продолжаем выполнение команды

    # Выполняем бан пользователя на сервере с указанным поводом (reason) и удалением сообщений (если выбрано).
    try:
        await ctx.guild.ban(user, reason=reason, clean_history_duration=delete_days)
    except disnake.errors.Forbidden:
        raise commands.CommandError(
            f"Не удалось забанить пользователя {user.mention}. Проверьте, что у бота есть право на бан участников."
        )

    # Отправляем информацию о бане в виде красочного embed сообщения
    ban_info_embed = disnake.Embed(
        title="Пользователь заблокирован",
        description=f"{user.mention} был успешно заблокирован на сервере {ctx.guild.name}.",
        color=disnake.Colour.red()  # Красный цвет
    )

    if ctx.author and ctx.author.avatar:
        ban_info_embed.set_footer(text=f"Выдал бан: {ctx.author.display_name}", icon_url=ctx.author.avatar.url)
    elif ctx.author:
        ban_info_embed.set_footer(text=f"Выдал бан: {ctx.author.display_name}")
    else:
        ban_info_embed.set_footer(text="Выдал бан: Неизвестный пользователь")

    if reason:
        ban_info_embed.add_field(
            name="**Причина бана**",
            value=reason,
            inline=False
        )
    if delete_messages and delete_days > 0:
        ban_info_embed.add_field(
            name="**Сообщения удалены за последние дни**",
            value=f"{delete_days} дней",
            inline=False
        )

    if isinstance(ctx, disnake.ApplicationCommandInteraction):
        await ctx.response.send_message(embed=ban_info_embed)
    else:
        await ctx.send(embed=ban_info_embed)


async def unban(ctx, user):
    # Проверяем, есть ли у пользователя разрешение на Бан на сервере
    if ctx.author.guild_permissions.ban_members:
        try:
            # Убираем бан с указанного пользователя на сервере.
            await ctx.guild.unban(user)

            # Создаем Embed для сообщения
            embed = disnake.Embed(
                title="Пользователь разбанен",
                description=f"Пользователь {user.mention} был успешно разбанен.",
                color=disnake.Color.green()
            )

            # Проверяем наличие фото профиля пользователя, который разбанил
            if ctx.author and ctx.author.avatar:
                embed.set_footer(text=f"Разбанил: {ctx.author.display_name}", icon_url=ctx.author.avatar)
            elif ctx.author:
                embed.set_footer(text=f"Разбанил: {ctx.author.display_name}")
            else:
                embed.set_footer(text="Разбанил: Неизвестный пользователь")

            # Добавляем информацию о модераторе, который разбанил
            embed.add_field(name="Модератор", value=ctx.author.mention)

            # Добавляем информацию о сервере
            embed.add_field(name="Сервер", value=ctx.guild.name)

            if isinstance(ctx, disnake.ApplicationCommandInteraction):
                await ctx.response.send_message(embed=embed, ephemeral=True)
            else:
                await ctx.send(embed=embed)

        except disnake.NotFound:
            raise commands.CommandError("Указанный пользователь не найден или не был забанен.")
        except disnake.Forbidden:
            raise commands.CommandError("У меня нет прав на разблокировку пользователей.")
    else:
        raise commands.CommandError("У вас нет прав на бан на этом сервере.")


class Ban(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name="бан",
        description="Забанить пользователя на сервере",
    )
    async def ban_command(self, ctx: disnake.MessageCommandInteraction, user: disnake.User, reason: str = None,
                          delete_messages: bool = False, delete_days: Literal[0, 1, 2, 3, 4, 5, 6, 7] = 0):
        if user is None:
            await ctx.send("Вы должны указать пользователя, которого хотите забанить.")
            return

        try:
            await ban(ctx, user, reason, delete_messages, delete_days)
        except commands.CommandError as e:
            await ctx.send(str(e))

    @commands.slash_command(
        name="бан",
        description="Забанить пользователя на сервере",
    )
    async def ban_slash(self, ctx: disnake.ApplicationCommandInteraction, user: disnake.User, reason: str = None,
                  delete_messages: bool = False, delete_days: Literal[0, 1, 2, 3, 4, 5, 6, 7] = 0):
        try:
            await ban(ctx, user, reason, delete_messages, delete_days)
        except commands.CommandError as e:
            await ctx.response.send_message(str(e), ephemeral=True)

    @commands.command(
        description="Разбанить указанного пользователя на сервере.",
        name="разбан"
    )
    async def unban_command(self, ctx, user: disnake.User = None):
        if user is None:
            await ctx.send("Вы должны указать пользователя, которого хотите разбанить.")
            return

        await unban(ctx, user)

    @commands.slash_command(
        description="Разбанить указанного пользователя на сервере.",
        name="разбан"
    )
    async def unban_slash(self, ctx, user: disnake.User):
        await unban(ctx, user)


# Функция setup, которая добавляет класс Ban как Cog (команду-расширение) в боте.
def setup(bot):
    bot.add_cog(Ban(bot))
