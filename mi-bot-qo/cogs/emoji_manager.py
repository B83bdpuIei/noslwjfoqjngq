import discord
from discord.ext import commands

class EmojiManager(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.ID_CANAL_ALMACEN = 1501603232642765061 
        self.biblioteca_emojis = {}

    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.wait_until_ready()
        await self.actualizar_biblioteca()
        print("🎒 Mochila automática lista y cargada.")

    @commands.Cog.listener()
    async def on_message(self, message):
        # Si pones algo en el canal almacén, la mochila se actualiza sola
        if message.channel.id == self.ID_CANAL_ALMACEN:
            await self.actualizar_biblioteca()

    async def actualizar_biblioteca(self):
        canal = self.bot.get_channel(self.ID_CANAL_ALMACEN)
        if not canal: return

        nueva_biblioteca = {}
        async for mensaje in canal.history(limit=100):
            for emoji in mensaje.emojis:
                nueva_biblioteca[emoji.name.lower()] = emoji
            
            partes = mensaje.content.split()
            if len(partes) >= 2 and not mensaje.emojis:
                nombre = partes[0].lower()
                emoji_texto = partes[1]
                nueva_biblioteca[nombre] = emoji_texto
        
        self.biblioteca_emojis = nueva_biblioteca

    def get_emoji(self, nombre):
        return self.biblioteca_emojis.get(nombre.lower())

async def setup(bot):
    await bot.add_cog(EmojiManager(bot))
