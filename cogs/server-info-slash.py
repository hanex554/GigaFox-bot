import disnake
from disnake.ext import commands

class ServerInfo1(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(
        name="сервер",
        description="Получить информацию о сервере"
    )
    async def server(self, ctx):
        # Получаем объект сервера по его ID
        guild = await self.bot.fetch_guild(ctx.guild_id)

        if guild is not None:
            # Сопоставление уровней верификации читаемым строкам
            verification_levels = {
                disnake.VerificationLevel.none.value: "Нет",
                disnake.VerificationLevel.low.value: "Низкий",
                disnake.VerificationLevel.medium.value: "Средний",
                disnake.VerificationLevel.high.value: "Высокий",
                disnake.VerificationLevel.highest.value: "Максимальный",
            }

            # Определение строки уровня верификации
            verification_levels = verification_levels.get(guild.verification_level.value, "Неизвестно")

            # Создание вставки для отображения информации о сервере
            embed = disnake.Embed(
                title=f"Информация о сервере {ctx.guild.name}",
                color=disnake.Color.blue()
            )

            # Добавление информации о сервере во вставку
            embed.set_thumbnail(url=ctx.guild.icon.url)
            embed.add_field(name="**Создатель сервера**", value=ctx.guild.owner.display_name, inline=True)
            embed.add_field(name="**Участники**", value=str(len(ctx.guild.members)), inline=True)
            embed.add_field(name="**Люди**", value=str(len([member for member in ctx.guild.members if not member.bot])), inline=True)
            embed.add_field(name="**Боты**", value=str(len([member for member in ctx.guild.members if member.bot])), inline=True)
            embed.add_field(name="**Роли**", value=str(len(ctx.guild.roles)), inline=True)
            embed.add_field(name="**Каналы**",
                            value=f"**Всего:** {len(ctx.guild.channels)}\n**Текстовых:** {len([channel for channel in ctx.guild.channels if isinstance(channel, disnake.TextChannel)])}\n**Объявления:** {len([channel for channel in ctx.guild.channels if isinstance(channel, disnake.NewsChannel)])}\n**Голосовых:** {len([channel for channel in ctx.guild.channels if isinstance(channel, disnake.VoiceChannel)])}",
                            inline=True)
            embed.add_field(name="**Уровень проверки сервера**", value=verification_levels, inline=True)

            # ... Добавьте другие поля ...

            embed.set_footer(text=f"ID сервера: {ctx.guild.id}")

            await ctx.send(embed=embed)
        else:
            await ctx.send("Ошибка: сервер не найден.")

def setup(bot):
    bot.add_cog(ServerInfo1(bot))
