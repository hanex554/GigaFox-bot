import disnake
from disnake.ext import commands
import sqlite3
import os

class MuteCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db_path = "dbs/mute_roles.db"
        self._ensure_db()

    def _ensure_db(self):
        # Создание папки для базы данных, если ее нет
        if not os.path.exists("dbs"):
            os.makedirs("dbs")

        # Создание таблицы для хранения данных о "чёрных списках"
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS mute_roles (
                guild_id INTEGER,
                user_id INTEGER,
                role_id INTEGER,
                PRIMARY KEY (guild_id, user_id)
            )
        ''')
        conn.commit()
        conn.close()

    @commands.slash_command(
        description="Добавляет пользователя в чёрный список сервера.",
        name="чс")
    async def add_role(self, ctx: disnake.ApplicationCommandInteraction, member: disnake.Member):
        if not ctx.author.guild_permissions.mute_members:
            embed = disnake.Embed(
                title='Ошибка',
                description='У вас нет разрешения для выполнения этой команды!',
                color=disnake.Color.red()
            )
            await ctx.send(embed=embed, ephemeral=True)
            return

        role_name = "В чёрном списке"
        role = disnake.utils.get(ctx.guild.roles, name=role_name)

        if role is None:
            try:
                role = await ctx.guild.create_role(name=role_name, permissions=disnake.Permissions.none())
            except Exception as e:
                embed = disnake.Embed(
                    title='Ошибка',
                    description=f'Произошла ошибка при создании роли: {e}',
                    color=disnake.Color.red()
                )
                await ctx.send(embed=embed)
                return

        try:
            await member.add_roles(role)

            # Сохранение роли в базе данных
            self._add_role_to_db(ctx.guild.id, member.id, role.id)

            embed = disnake.Embed(
                title='Успешно',
                description=f'Успешно добавлена роль {role.name} для {member.mention}',
                color=disnake.Color.green()
            )
            await ctx.send(embed=embed)
        except Exception as e:
            embed = disnake.Embed(
                title='Ошибка',
                description=f'Произошла ошибка: {e}',
                color=disnake.Color.red()
            )
            await ctx.send(embed=embed)

    @commands.slash_command(
        description="Удаляет пользователя из чёрного списка сервера.",
        name="разчс")
    async def delete_role(self, ctx: disnake.ApplicationCommandInteraction, member: disnake.Member):
        if not ctx.author.guild_permissions.mute_members:
            embed = disnake.Embed(
                title='Ошибка',
                description='У вас нет разрешения для выполнения этой команды!',
                color=disnake.Color.red()
            )
            await ctx.send(embed=embed, ephemeral=True)
            return

        role_name = "В чёрном списке"
        role = disnake.utils.get(ctx.guild.roles, name=role_name)

        if role is None:
            embed = disnake.Embed(
                title='Ошибка',
                description=f'Роль {role_name} не существует в сервере!',
                color=disnake.Color.red()
            )
            await ctx.send(embed=embed)
            return

        try:
            await member.remove_roles(role)

            # Удаление записи из базы данных
            self._remove_role_from_db(ctx.guild.id, member.id)

            embed = disnake.Embed(
                title='Успешно',
                description=f'Успешно удалена роль {role.name} у {member.mention}',
                color=disnake.Color.green()
            )
            await ctx.send(embed=embed)
        except Exception as e:
            embed = disnake.Embed(
                title='Ошибка',
                description=f'Произошла ошибка: {e}',
                color=disnake.Color.red()
            )
            await ctx.send(embed=embed)

    def _add_role_to_db(self, guild_id, user_id, role_id):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('INSERT OR REPLACE INTO mute_roles (guild_id, user_id, role_id) VALUES (?, ?, ?)',
                       (guild_id, user_id, role_id))
        conn.commit()
        conn.close()

    def _remove_role_from_db(self, guild_id, user_id):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM mute_roles WHERE guild_id = ? AND user_id = ?', (guild_id, user_id))
        conn.commit()
        conn.close()

    @commands.Cog.listener()
    async def on_member_join(self, member):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT role_id FROM mute_roles WHERE guild_id = ? AND user_id = ?', (member.guild.id, member.id))
        result = cursor.fetchone()
        conn.close()

        if result:
            role_id = result[0]
            role = member.guild.get_role(role_id)
            if role:
                await member.add_roles(role)

def setup(bot):
    bot.add_cog(MuteCog(bot))
