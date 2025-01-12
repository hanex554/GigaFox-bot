import disnake
from disnake.ext import commands
from disnake.utils import format_dt
from datetime import datetime, timezone
import sqlite3

class WelcomeCog(commands.Cog):
    def __init__(self, bot, db_path):
        self.bot = bot
        self.db_path = db_path

    @commands.Cog.listener()
    async def on_member_join(self, member):
        # Получаем информацию о новом пользователе
        member_name = member.display_name
        member_mention = member.mention

        # Получаем дату создания аккаунта пользователя
        member_created_date = member.created_at

        # Устанавливаем временную зону UTC для обеих дат
        member_created_date = member_created_date.replace(tzinfo=timezone.utc)
        current_date = datetime.now(timezone.utc)

        # Вычисляем разницу между текущей датой и датой создания аккаунта
        days_since_creation = (current_date - member_created_date).days

        # Проверяем, был ли аккаунт создан менее 7 дней назад
        recently_created = days_since_creation < 7

        # Получаем количество участников на сервере
        member_count = len(member.guild.members)

        # Проверяем, есть ли аватар у пользователя
        if member.avatar:
            avatar_url = member.avatar.url
        else:
            # Если у пользователя нет аватара, устанавливаем URL для аватара по умолчанию
            avatar_url = member.default_avatar.url

        # Создаем вложение (embed) с приветствием и информацией о новом пользователе
        embed = disnake.Embed(
            title=f'Добро пожаловать, {member_name}!',
            description=f'Аккаунт создан {format_dt(member_created_date, style="R")}',
            color=0x55FF55,  # Замените на цвет вашего выбора
        )
        embed.set_thumbnail(url=avatar_url)  # Устанавливаем фото профиля пользователя
        embed.add_field(name='Участник', value=member_mention, inline=True)
        embed.add_field(name='Число участника на сервере', value=f'{member_count} участников', inline=False)

        # Если аккаунт создан недавно, добавляем к тексту иконку и делаем его более заметным
        if recently_created:
            embed.set_footer(text='🚨 Аккаунт создан недавно 🚨')

        # Получаем ID канала для отправки приветствия с сервера
        welcome_channel_id = self.get_welcome_channel(member.guild)
        channel = member.guild.get_channel(welcome_channel_id)

        if channel:
            await channel.send(embed=embed)

    def get_welcome_channel(self, guild):
        # Подключаемся к базе данных SQLite
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Создаем таблицу, если она не существует
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS welcome_channels (
                guild_id INTEGER PRIMARY KEY,
                channel_id INTEGER
            )
        ''')

        # Пытаемся получить ID канала приветствия для данного сервера
        cursor.execute('SELECT channel_id FROM welcome_channels WHERE guild_id = ?', (guild.id,))
        result = cursor.fetchone()

        # Если канал приветствия не найден, используем ID канала по умолчанию
        if result:
            channel_id = result[0]
        else:
            # Замените это на ID канала по умолчанию
            channel_id = 123456789012345678

        # Закрываем соединение с базой данных
        conn.close()

        return channel_id

    @commands.command(name="выбратьканалприветсвие")
    @commands.has_permissions(administrator=True)
    async def set_welcome_channel(self, ctx, channel: disnake.TextChannel):
        # Подключаемся к базе данных SQLite
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Создаем таблицу, если она не существует
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS welcome_channels (
                guild_id INTEGER PRIMARY KEY,
                channel_id INTEGER
            )
        ''')

        # Сохраняем ID канала приветствия для данного сервера
        cursor.execute('INSERT OR REPLACE INTO welcome_channels (guild_id, channel_id) VALUES (?, ?)', (ctx.guild.id, channel.id))
        conn.commit()

        # Закрываем соединение с базой данных
        conn.close()

        await ctx.send(f"Канал приветствия установлен на {channel.mention}")

    @commands.command(name="удалитьканалпривествия")
    @commands.has_permissions(administrator=True)
    async def remove_welcome_channel(self, ctx):
        # Подключаемся к базе данных SQLite
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Удаляем запись о канале приветствия для данного сервера
        cursor.execute('DELETE FROM welcome_channels WHERE guild_id = ?', (ctx.guild.id,))
        conn.commit()

        # Закрываем соединение с базой данных
        conn.close()

        await ctx.send("Канал приветствия удален.")

    @commands.slash_command(
        name="выбрать_канал_приветсвие",
        description="Установить канал для приветствия новых участников на сервере.")
    async def slash_set_welcome_channel(self, ctx, channel: disnake.TextChannel):
        if ctx.author.guild_permissions.administrator:
            # Подключаемся к базе данных SQLite
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # Создаем таблицу, если она не существует
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS welcome_channels (
                    guild_id INTEGER PRIMARY KEY,
                    channel_id INTEGER
                )
            ''')

            # Сохраняем ID канала приветствия для данного сервера
            cursor.execute('INSERT OR REPLACE INTO welcome_channels (guild_id, channel_id) VALUES (?, ?)', (ctx.guild.id, channel.id))
            conn.commit()

            # Закрываем соединение с базой данных
            conn.close()

            await ctx.send(f"Канал приветствия установлен на {channel.mention}")
        else:
            await ctx.send("У вас нет прав для выполнения этой команды.", ephemeral=True)

    @commands.slash_command(
        name="удалить_канал_привествия",
        description="Удалить установленный канал для приветствия новых участников.")
    async def slash_remove_welcome_channel(self, ctx):
        if ctx.author.guild_permissions.administrator:
            # Подключаемся к базе данных SQLite
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # Удаляем запись о канале приветствия для данного сервера
            cursor.execute('DELETE FROM welcome_channels WHERE guild_id = ?', (ctx.guild.id,))
            conn.commit()

            # Закрываем соединение с базой данных
            conn.close()

            await ctx.send("Канал приветствия удален.")
        else:
            await ctx.send("У вас нет прав для выполнения этой команды.", ephemeral=True)

def setup(bot):
    # Укажите путь к вашей базе данных SQLite
    db_path = 'welcome_channels.db'
    bot.add_cog(WelcomeCog(bot, db_path))
