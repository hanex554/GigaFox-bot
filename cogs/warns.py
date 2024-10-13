import disnake
from disnake.ext import commands
from disnake import embeds
import sqlite3

intents = disnake.Intents.all()

# Initialize the SQLite database
conn = sqlite3.connect('warnings.db')
c = conn.cursor()

# Create a table to store warnings for each guild separately
c.execute('''CREATE TABLE IF NOT EXISTS warnings (
                guild_id INTEGER,
                user_id INTEGER,
                moderator_id INTEGER,
                reason TEXT
             )''')
conn.commit()

class Warns(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(
        name="пред",
        description="Выдать предупреждение пользователю",
    )
    async def warn(self, ctx: disnake.ApplicationCommandInteraction, user: disnake.User, reason: str):
        if not ctx.author.guild_permissions.mute_members:
            embed = disnake.Embed(
                title="Ошибка",
                description="У вас нет разрешения на выполнение этой команды.",
                color=disnake.Colour.red()
            )
            await ctx.send(embed=embed)
            return

        warning_embed = embeds.Embed(
            title="⚠️ Предупреждение",
            description=f"Уважаемый(ая) {user.mention},",
            color=disnake.Colour.orange()
        )

        warning_embed.add_field(name="**Причина предупреждения**", value=reason, inline=False)

        warning_embed.add_field(
            name="**Пожалуйста, обратите внимание на данное предупреждение и соблюдайте правила сервера.**",
            value=f"С наилучшими пожеланиями,\nКоманда {ctx.guild.name}",
            inline=False
        )

        if ctx.author.avatar:
            warning_embed.set_footer(text=f"Выдано администратором {ctx.author.display_name}", icon_url=ctx.author.avatar.url)
        else:
            warning_embed.set_footer(text=f"Выдано администратором {ctx.author.display_name}")

        await ctx.send(embed=warning_embed)

        try:
            await user.send(embed=warning_embed)
        except disnake.errors.Forbidden:
            pass

        # Store the warning in the database with guild_id
        c.execute("INSERT INTO warnings (guild_id, user_id, moderator_id, reason) VALUES (?, ?, ?, ?)",
                  (ctx.guild.id, user.id, ctx.author.id, reason))
        conn.commit()

    @commands.slash_command(
        name="преды",
        description="Просмотреть предупреждения пользователя",
    )
    async def warnings(self, ctx: disnake.ApplicationCommandInteraction, member: disnake.Member):
        c.execute("SELECT moderator_id, reason FROM warnings WHERE guild_id=? AND user_id=?", (ctx.guild.id, member.id))
        warnings = c.fetchall()

        if warnings:
            embed = disnake.Embed(title=f"Предупреждения пользователя {member.display_name}", color=disnake.Color.red())
            for moderator_id, reason in warnings:
                moderator = ctx.guild.get_member(moderator_id)
                if moderator:
                    embed.add_field(name=f"Модератор: {moderator.display_name}", value=f"Причина: {reason}", inline=False)
                else:
                    embed.add_field(name=f"Модератор: (недоступен)", value=f"Причина: {reason}", inline=False)
            await ctx.response.send_message(embed=embed)
        else:
            embed = disnake.Embed(
                title="Предупреждения не найдены",
                description=f"{member.mention} не имеет предупреждений.",
                color=disnake.Color.orange()
            )
            await ctx.response.send_message(embed=embed)

    @commands.slash_command(
        name="удалитьпреды",
        description="Удалить все предупреждения пользователя",
    )
    async def delete_warnings(self, ctx: disnake.ApplicationCommandInteraction, member: disnake.Member):
        if not ctx.author.guild_permissions.mute_members:
            embed = disnake.Embed(
                title="Ошибка",
                description="У вас нет разрешения на выполнение этой команды.",
                color=disnake.Colour.red()
            )
            await ctx.response.send_message(embed=embed)
            return

        # Delete all warnings for the specified user in the current guild
        c.execute("DELETE FROM warnings WHERE guild_id=? AND user_id=?", (ctx.guild.id, member.id))
        conn.commit()

        embed = disnake.Embed(
            title="Предупреждения удалены",
            description=f"Все предупреждения пользователя {member.mention} удалены.",
            color=disnake.Colour.green()
        )
        await ctx.response.send_message(embed=embed)

    @commands.slash_command(
        name="удалитьпред",
        description="Удалить конкретное предупреждение пользователя",
    )
    async def delete_warning(self, ctx: disnake.ApplicationCommandInteraction, member: disnake.Member, warning_id: int):
        if not ctx.author.guild_permissions.mute_members:
            embed = disnake.Embed(
                title="Ошибка",
                description="У вас нет разрешения на выполнение этой команды.",
                color=disnake.Colour.red()
            )
            await ctx.response.send_message(embed=embed)
            return

        c.execute("SELECT rowid FROM warnings WHERE guild_id=? AND user_id=?", (ctx.guild.id, member.id))
        warning_rows = c.fetchall()

        if warning_rows:
            if warning_id <= 0 or warning_id > len(warning_rows):
                embed = disnake.Embed(
                    title="Ошибка",
                    description="Указанный номер предупреждения недопустим.",
                    color=disnake.Colour.red()
                )
                await ctx.response.send_message(embed=embed)
                return

            selected_warning_rowid = warning_rows[warning_id - 1][0]

            # Delete the selected warning by rowid
            c.execute("DELETE FROM warnings WHERE rowid=?", (selected_warning_rowid,))
            conn.commit()

            embed = disnake.Embed(
                title="Предупреждение удалено",
                description=f"Предупреждение {warning_id} для пользователя {member.mention} удалено.",
                color=disnake.Colour.green()
            )
            await ctx.response.send_message(embed=embed)
        else:
            embed = disnake.Embed(
                title="Предупреждения не найдены",
                description=f"{member.mention} не имеет предупреждений.",
                color=disnake.Colour.orange()
            )
            await ctx.response.send_message(embed=embed)

def setup(bot):
    bot.add_cog(Warns(bot))
