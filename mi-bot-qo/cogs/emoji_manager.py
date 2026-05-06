import discord
from discord.ext import commands

class EmojiManager(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # El ID que me acabas de pasar (tu canal almacén)
        self.ID_CANAL_ALMACEN = 1501603232642765061 
        self.biblioteca_emojis = {}

    @commands.Cog.listener()
    async def on_ready(self):
        """Carga los emojis en cuanto el bot se enciende"""
        # Esperamos un poco para que el bot esté bien conectado antes de leer canales
        await self.bot.wait_until_ready()
        await self.actualizar_biblioteca()
        print(f"✅ Mochila cargada: {len(self.biblioteca_emojis)} emojis listos.")

    async def actualizar_biblioteca(self):
        """Escanea el canal y guarda los emojis por su nombre"""
        canal = self.bot.get_channel(self.ID_CANAL_ALMACEN)
        if not canal:
            print(f"⚠️ No pude encontrar el canal {self.ID_CANAL_ALMACEN}")
            return

        nueva_biblioteca = {}
        async for mensaje in canal.history(limit=100):
            # 1. Guardar emojis personalizados (los 'raros' animados o estáticos)
            for emoji in mensaje.emojis:
                nueva_biblioteca[emoji.name.lower()] = emoji
            
            # 2. Guardar emojis de texto si pones: nombre 🍎
            partes = mensaje.content.split()
            if len(partes) >= 2 and not mensaje.emojis:
                nombre = partes[0].lower()
                emoji_texto = partes[1]
                nueva_biblioteca[nombre] = emoji_texto
        
        self.biblioteca_emojis = nueva_biblioteca

    def get_emoji(self, nombre):
        """Usa esto para sacar un emoji por su nombre"""
        return self.biblioteca_emojis.get(nombre.lower())

    @commands.command(name="update_mochila")
    @commands.has_permissions(administrator=True)
    async def update_mochila(self, ctx):
        """Comando para actualizar la lista sin reiniciar el bot"""
        await self.actualizar_biblioteca()
        total = len(self.biblioteca_emojis)
        await ctx.send(f"🎒 **Mochila de Cromi actualizada.**\nHe guardado **{total}** emojis del canal <#{self.ID_CANAL_ALMACEN}>.")

async def setup(bot):
    await bot.add_cog(EmojiManager(bot))
