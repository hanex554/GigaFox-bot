import os
import disnake
from disnake.ext import commands
import aiosqlite  # Используем асинхронную версию SQLite

# Определите путь к файлу базы данных в папке "dbs"
db_path = os.path.join("dbs", "server_choices.db")

# Глобальная переменная для отслеживания состояния
is_member_cog_enabled = {}

class MemberCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        server_id = member.guild.id
        if is_member_cog_enabled.get(server_id, False):
            role_name = "Участник сервера"
            role = disnake.utils.get(member.guild.roles, name=role_name)

            if role is None:
                role = await member.guild.create_role(name=role_name)

            await member.add_roles(role)

    @commands.slash_command(
        name="рольучасникпризаходе",
        description="Включить или выключить функцию добавления роли"
    )
    async def toggle_member_cog(self, ctx: disnake.ApplicationCommandInteraction):
        server_id = ctx.guild.id
        global is_member_cog_enabled

        if not ctx.author.guild_permissions.administrator:
            await ctx.response.send_message(
                "У вас недостаточно прав для выполнения этой команды. Требуется право администратора.",
                ephemeral=True
            )
            return

        # Переключаем состояние функции
        is_member_cog_enabled[server_id] = not is_member_cog_enabled.get(server_id, False)

        if is_member_cog_enabled[server_id]:
            await ctx.response.send_message("Функция добавления роли включена.")
        else:
            await ctx.response.send_message("Функция добавления роли выключена.")

        # Записываем выбор сервера в базу данных
        async with aiosqlite.connect(db_path) as conn:
            await conn.execute('''
                CREATE TABLE IF NOT EXISTS server_choices (
                    server_id INTEGER PRIMARY KEY,
                    is_enabled BOOLEAN
                )
            ''')  # Создаем таблицу, если она не существует
            await conn.execute('REPLACE INTO server_choices (server_id, is_enabled) VALUES (?, ?)',
                               (server_id, is_member_cog_enabled[server_id]))
            await conn.commit()

def setup(bot):
    bot.add_cog(MemberCog(bot))

if __name__ == "__main__":
    # Создаем папку "dbs", если она не существует
    os.makedirs("dbs", exist_ok=True)

    # Загружаем состояние выбора сервера из базы данных
    async def load_server_choices():
        async with aiosqlite.connect(db_path) as conn:
            async with conn.execute('SELECT server_id, is_enabled FROM server_choices') as cursor:
                async for row in cursor:
                    server_id, is_enabled = row
                    is_member_cog_enabled[server_id] = is_enabled


    import asyncio
    asyncio.run(load_server_choices())
