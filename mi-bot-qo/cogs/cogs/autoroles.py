import discord
from discord.ext import commands

class Autoroles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
        # ID del canal donde se enviará el mensaje de colores
        self.CANAL_ROLES = 1501564084477235301

        # Diccionario de colores (Emoji -> ID del Rol)
        self.roles_colores = {
            "❤️": 1501554375204802671,  # Rojo
            "🧡": 1501554811185664010,  # Naranja
            "💛": 1501554310960648302,  # Amarillo
            "💚": 1501554496067862661,  # Verde
            "🩵": 1501554174381523045,  # Azul
            "🩷": 1501553906298392636,  # Rosa
            "💜": 1501554569719844986   # Morado
        }

    @commands.command(name="setup_colores")
    @commands.has_permissions(administrator=True)
    async def setup_colores(self, ctx):
        canal_destino = self.bot.get_channel(self.CANAL_ROLES)
        
        if not canal_destino:
            await ctx.send(f"❌ Error: No he podido encontrar el canal con ID {self.CANAL_ROLES}.")
            return

        # Intentamos sacar el emoji "campage" de la mochila
        mochila = self.bot.get_cog('EmojiManager')
        emoji_campage = ""
        if mochila:
            emoji_obj = mochila.get_emoji("campage")
            if emoji_obj:
                emoji_campage = str(emoji_obj)

        descripcion = (
            f"{emoji_campage} **¡Elige tu color!**\n"
            "Reacciona con el emoji del color que más te guste:\n\n"
            "❤️ | Rojo\n"
            "🧡 | Naranja\n"
            "💛 | Amarillo\n"
            "💚 | Verde\n"
            "🩵 | Azul\n"
            "🩷 | Rosa\n"
            "💜 | Morado\n\n"
            "Dale color a tu nombre y personalízate, hazte notar 🎨"
        )

        embed = discord.Embed(
            description=descripcion,
            color=discord.Color.orange()
        )
        embed.set_footer(text="Cromi System • Autoroles")

        # Enviamos el embed al canal específico
        msg = await canal_destino.send(embed=embed)

        # Añadimos los corazones de forma automática
        for emoji in self.roles_colores.keys():
            await msg.add_reaction(emoji)
            
        # Borramos el mensaje del comando (.setup_colores) para que no ensucie
        try:
            await ctx.message.delete()
        except discord.NotFound:
            pass

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.user_id == self.bot.user.id:
            return

        emoji_name = str(payload.emoji)
        
        # SISTEMA DE COLORES
        if emoji_name in self.roles_colores:
            guild = self.bot.get_guild(payload.guild_id)
            member = guild.get_member(payload.user_id)
            if not member: return

            # Quitar otros colores previos (para no parecer un arcoíris roto)
            roles_a_quitar = []
            for emoji, role_id in self.roles_colores.items():
                if role_id != self.roles_colores[emoji_name]:
                    rol = guild.get_role(role_id)
                    if rol and rol in member.roles:
                        roles_a_quitar.append(rol)
            
            if roles_a_quitar:
                await member.remove_roles(*roles_a_quitar)

            # Dar el color nuevo
            rol_nuevo = guild.get_role(self.roles_colores[emoji_name])
            if rol_nuevo:
                await member.add_roles(rol_nuevo)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        emoji_name = str(payload.emoji)
        
        # QUITAR SISTEMA DE COLORES
        if emoji_name in self.roles_colores:
            guild = self.bot.get_guild(payload.guild_id)
            member = guild.get_member(payload.user_id)
            if not member: return

            rol_a_quitar = guild.get_role(self.roles_colores[emoji_name])
            if rol_a_quitar and rol_a_quitar in member.roles:
                await member.remove_roles(rol_a_quitar)

async def setup(bot):
    await bot.add_cog(Autoroles(bot))
