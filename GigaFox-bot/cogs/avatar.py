import disnake
from disnake.ext import commands
from colorthief import ColorThief
import requests
import io


class AvatarCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    def get_embed_color(image_url):
        try:
            # Получаем изображение по URL и создаем объект ColorThief
            with requests.get(image_url) as response:
                response.raise_for_status()
                image_content = io.BytesIO(response.content)
                color_thief = ColorThief(image_content)

            # Получаем доминирующий цвет и преобразуем его в Disnake Color
            dominant_color = color_thief.get_color(quality=1)
            return disnake.Color.from_rgb(*dominant_color)
        except (requests.exceptions.RequestException, OSError) as e:
            print(f"Ошибка при получении или обработке изображения: {e}")
            return disnake.Color.default()

    @commands.command(
        name="аватар",
        description="Отправляет аватар пользователя с цветом, зависящим от его фото профиля."
    )
    async def avatar_command(self, ctx, member: disnake.Member = None):
        """
        Отправляет аватар пользователя с цветом, зависящим от его фото профиля.

        :param ctx: Контекст команды
        :param member: Пользователь, аватар которого нужно отправить
        """
        member = member or ctx.author
        avatar_url = member.avatar.url if member.avatar else member.default_avatar.url

        embed_color = self.get_embed_color(avatar_url)

        embed = disnake.Embed(
            title=f"Аватар пользователя {member.display_name}",
            color=embed_color
        )
        embed.set_image(url=avatar_url)

        await ctx.send(embed=embed)

    @commands.slash_command(
        name="аватар",
        description="Отправляет аватар пользователя с цветом, зависящим от его фото профиля."
    )
    async def avatar_slash(self, inter, member: disnake.Member = None):
        """
        Отправляет аватар пользователя с цветом, зависящим от его фото профиля.

        :param inter: Взаимодействие с командой
        :param member: Пользователь, аватар которого нужно отправить
        """
        member = member or inter.author
        avatar_url = member.avatar.url if member.avatar else member.default_avatar.url

        embed_color = self.get_embed_color(avatar_url)

        embed = disnake.Embed(
            title=f"Аватар пользователя {member.display_name}",
            color=embed_color
        )
        embed.set_image(url=avatar_url)

        await inter.response.send_message(embed=embed)


def setup(bot):
    bot.add_cog(AvatarCog(bot))