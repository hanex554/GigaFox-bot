import disnake
from disnake.ext import commands
import os
import sqlite3

class Profile(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.data_folder = 'profiles'  # Папка для хранения баз данных

        # Убедитесь, что папка для хранения данных существует
        if not os.path.exists(self.data_folder):
            os.makedirs(self.data_folder)

    def connect_to_database(self, guild_id):
        db_path = os.path.join(self.data_folder, f'guild_{guild_id}_profiles.db')
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()
        cursor.execute('CREATE TABLE IF NOT EXISTS profiles (user_id INTEGER PRIMARY KEY, description TEXT)')
        connection.commit()
        return connection

    @commands.slash_command(
        name="установить_описание",
        description="Установить описание пользователя"
    )
    async def set_description(self, ctx, description: str):
        """Слеш-команда для установки описания пользователя."""
        connection = self.connect_to_database(ctx.guild.id)

        # Сохранение описания пользователя в базе данных
        cursor = connection.cursor()
        cursor.execute('INSERT OR REPLACE INTO profiles (user_id, description) VALUES (?, ?)',
                       (ctx.author.id, description))
        connection.commit()

        await ctx.send('Ваше описание успешно сохранено!')

    @commands.slash_command(
        name="получить_описание",
        description="Получить описание пользователя"
    )
    async def get_description(self, ctx, user: disnake.Member = None):
        """Слеш-команда для получения описания пользователя."""
        if user is None:
            user = ctx.author

        connection = self.connect_to_database(ctx.guild.id)
        cursor = connection.cursor()
        cursor.execute('SELECT description FROM profiles WHERE user_id = ?', (user.id,))
        result = cursor.fetchone()

        if result is not None and result[0] is not None:
            description = result[0]

            # Создаем встроенное сообщение (embed)
            embed = disnake.Embed(
                title=f"Профиль пользователя {user.display_name}",
                description=description,
                color=0x7289DA
            )

            # Устанавливаем аватарку пользователя как изображение для embed
            embed.set_thumbnail(url=user.avatar.url)

            await ctx.send(embed=embed)
        else:
            await ctx.send(f"{user.display_name} не имеет описания.")

def setup(bot):
    bot.add_cog(Profile(bot))
