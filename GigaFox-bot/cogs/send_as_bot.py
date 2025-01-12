import disnake
from disnake.ext import commands

class SendAsBot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Slash-команда с проверкой на админа
    @commands.slash_command(description="Отправить сообщение от имени бота")
    @commands.has_permissions(administrator=True)  # Проверка на права администратора
    async def send_as_bot(
        self,
        inter: disnake.ApplicationCommandInteraction,
        channel: disnake.TextChannel,
        message: str
    ):
        await channel.send(message)
        await inter.response.send_message(
            f"Сообщение успешно отправлено в канал {channel.mention}.",
            ephemeral=True
        )

# Функция для подключения Cog
def setup(bot):
    bot.add_cog(SendAsBot(bot))