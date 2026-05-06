import discord
from discord.ext import commands

class EmojiManager(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # ID del canal donde vas a pegar los emojis
        self.ID_CANAL_ALMACEN = 1501564312265687213 
        self.biblioteca_emojis = {}

    @commands.Cog.listener()
    async def on_ready(self):
        """Carga los emojis en cuanto el bot se enciende"""
        await self.actualizar_biblioteca()
        print(f"✅ Biblioteca de emojis cargada: {len(self.biblioteca_emojis)} emojis guardados.")

    async def actualizar_biblioteca(self):
        """Escanea el canal y guarda los emojis por su nombre"""
        canal = self.bot.get_channel(self.ID_CANAL_ALMACEN)
        if not canal:
            return

        async for mensaje in canal.history(limit=100):
            # Guardar emojis personalizados (normales y animados)
            for emoji in mensaje.emojis:
                self.biblioteca_emojis[emoji.name.lower()] = emoji
            
            # Guardar emojis de texto si los pones como "nombre 🍎"
            partes = mensaje.content.split()
            if len(partes) >= 2 and not mensaje.emojis:
                nombre = partes[0].lower()
                emoji_texto = partes[1]
                self.biblioteca_emojis[nombre] = emoji_texto

    def get_emoji(self, nombre):
        """Función para sacar un emoji de la mochila por su nombre"""
        return self.biblioteca_emojis.get(nombre.lower())

    @commands.command(name="reload_emojis")
    @commands.has_permissions(administrator=True)
    async def reload_emojis(self, ctx):
        """Comando manual por si añades emojis nuevos al canal"""
        await self.actualizar_biblioteca()
        await ctx.send(f"🔄 ¡Mochila actualizada! He guardado {len(self.biblioteca_emojis)} emojis.")

async def setup(bot):
    await bot.add_cog(EmojiManager(bot))
