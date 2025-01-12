import disnake
from disnake.ext import commands
import random
import os

# Список случайных фраз для объятий
hug_phrases = [
    "дарит объятия",
    "дает теплые объятия",
    "обнимает нежно",
    "обнимает крепко",
    "поднимает настроение объятиями",
]

class Hug(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.image_folder = 'image-hug'

    @commands.slash_command(
        name="обнять",
        description="Отправить объятия",
    )
    async def hug_slash(self, ctx, targets: str = None):
        await self.send_hugs(ctx, targets)

    async def send_hugs(self, ctx, targets):
        # Генерация случайной фразы объятий
        hug_phrase = random.choice(hug_phrases)

        # Разбивка списка имен пользователей и создание текста объятий
        if targets:
            target_names = []
            for target_mention in targets.split():
                try:
                    target_id = int(target_mention.strip('<@!>'))
                    target_member = ctx.guild.get_member(target_id)
                    if target_member:
                        target_names.append(f"**{target_member.display_name}**")
                except ValueError:
                    pass
            if target_names:
                hug_text = f"**{ctx.author.display_name}** {hug_phrase} {' '.join(target_names)}!"
            else:
                hug_text = f"**{ctx.author.display_name}** {hug_phrase} всем!"
        else:
            hug_text = f"**{ctx.author.display_name}** {hug_phrase} всем!"

        # Случайный выбор изображения из папки
        image_files = [file for file in os.listdir(self.image_folder) if
                       file.endswith('.jpg') or file.endswith('.png') or file.endswith('.gif')]
        if image_files:
            random_image = random.choice(image_files)
            image_path = os.path.join(self.image_folder, random_image)

            # Отправка сообщения с текстом объятий и файлом изображения
            await ctx.send(hug_text, file=disnake.File(image_path, filename=random_image))
        else:
            # Отправка сообщения только с текстом объятий, без изображения
            await ctx.send(hug_text)

def setup(bot):
    bot.add_cog(Hug(bot))
