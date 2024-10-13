import datetime
import disnake
from disnake.ext import commands

class Timeout(commands.Cog):
    """Cog для работы с таймаутами."""

    def __init__(self, bot):
        """Инициализация класса Timeout."""
        self.bot = bot

    @commands.slash_command(
        name="таймаут",
        description="Замутить пользователя на указанное время с указанием причины (по желанию)."
    )
    async def timeout_slash(self, interaction, member: disnake.Member, time: int, reason: str = ""):
        """Слэш-команда для применения таймаута."""
        await self.timeout_common(interaction, member, time, reason)

    @commands.command(
        name="таймаут",
        description="Замутить пользователя на указанное время с указанием причины (по желанию)."
    )
    async def timeout_command(self, ctx, member: disnake.Member, time: int, reason: str = ""):
        """Команда для применения таймаута."""
        await self.timeout_common(ctx, member, time, reason)

    @staticmethod
    async def timeout_common(ctx, member: disnake.Member, time: int, reason: str):
        """Общая функция для обработки таймаутов."""
        if member == ctx.author:
            embed = disnake.Embed(
                title="Ошибка",
                description="Вы не можете замутить самого себя",
                color=0xFF0000
            )
            return await ctx.send(embed=embed)

        if not ctx.author.guild_permissions.mute_members:
            embed = disnake.Embed(
                title="Ошибка",
                description="У вас нет необходимых разрешений для выполнения этой команды (например, 'Мутить участников').",
                color=0xFF0000
            )
            return await ctx.send(embed=embed)

        if time < 1:
            embed = disnake.Embed(
                title="Ошибка",
                description="Вы не можете замутить пользователя на меньше 1 минуты",
                color=0xFF0000
            )
            return await ctx.send(embed=embed)

        end_time = datetime.datetime.now() + datetime.timedelta(minutes=time)

        timeout_message = (
            f"🌟 **━━━⭐ Важное Уведомление: Временный Тайм-аут ⭐━━━** 🌟\n\n"
            f"Уважаемый(ая) {member.mention},\n\n"
            f"🕒 Наступило время для особенного момента. Ваша учётная запись временно находится в состоянии тайм-аута.\n\n"
            f"**Длительность тайма-ута:** {time // (24 * 60)} дн. {time // 60 % 24} ч. {time % 60} мин.\n"
            f"**Причина:** {reason}\n\n"
            f"🌱 Жизнь — это непрерывное путешествие самопознания и роста. Ваш тайм-аут — это особое время, когда можно взглянуть на себя под новым углом, обрести вдохновение и наметить новые пути.\n\n"
            f"🌄 Пожалуйста, предайте этому периоду смысл и значимость. Позвольте себе уйти на небольшой отдых от шума мира и вернуться с новыми идеями и планами.\n\n"
            f"С нежными пожеланиями и поддержкой,\n"
            f"Команда {member.guild.name}"
        )

        try:
            await member.send(content=timeout_message)
        except disnake.errors.Forbidden:
            pass

        await member.timeout(until=end_time, reason=reason)
        formatted_time = end_time - datetime.datetime.now()
        formatted_time_str = f"{formatted_time.days} дн. {formatted_time.seconds // 3600} ч. {(formatted_time.seconds % 3600) // 60} мин."

        embed = disnake.Embed(
            title="Таймаут",
            description=f"Пользователь {member.mention} был затайм-аутен. Причина: {reason if reason else 'не указана'}. "
                        f"Длительность тайма-ута {formatted_time_str}",
            color=0x00FF00
        )
        embed.set_footer(text=f"Таймаут выдал: {ctx.author.display_name}")

        if isinstance(ctx, disnake.Interaction):
            await ctx.response.send_message(embed=embed)
        else:
            await ctx.send(embed=embed)

    @commands.slash_command(
        name="снять_таймаут",
        description="Снять временный мут с пользователя."
    )
    async def remove_timeout_slash(self, interaction, member: disnake.Member):
        """Слэш-команда для снятия таймаута."""
        await self.remove_timeout_common(interaction, member)

    @commands.command(
        name="снять_таймаут",
        description="Снять временный мут с пользователя."
    )
    async def remove_timeout_command(self, ctx, member: disnake.Member):
        """Команда для снятия таймаута."""
        await self.remove_timeout_common(ctx, member)

    @staticmethod
    async def remove_timeout_common(ctx, member: disnake.Member):
        """Общая функция для снятия таймаутов."""
        if ctx.author.guild_permissions.mute_members:
            await member.timeout(until=None, reason=None)
            embed = disnake.Embed(
                title="Снятие таймаута",
                description=f"Таймаут с пользователя {member.mention} был снят",
                color=0x00FF00
            )
            embed.set_footer(text=f"Таймаут снял: {ctx.author.display_name}")

            if isinstance(ctx, disnake.Interaction):
                await ctx.response.send_message(embed=embed)
            else:
                await ctx.send(embed=embed)
        else:
            embed = disnake.Embed(
                title="Ошибка",
                description="У вас нет прав на выполнение этой команды.",
                color=0xFF0000
            )
            if isinstance(ctx, disnake.Interaction):
                await ctx.response.send_message(embed=embed, ephemeral=True)
            else:
                await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Timeout(bot))
