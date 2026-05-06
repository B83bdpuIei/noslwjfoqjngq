import discord
from discord.ext import commands

class Autoroles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.CANAL_ROLES = 1501564084477235301

        self.roles_colores = {
            "❤️": 1501554375204802671,
            "🧡": 1501554811185664010,
            "💛": 1501554310960648302,
            "💚": 1501554496067862661,
            "🩵": 1501554174381523045,
            "🩷": 1501553906298392636,
            "💜": 1501554569719844986
        }

    @commands.command(name="generar_colores")
    @commands.has_permissions(administrator=True)
    async def generar_colores(self, ctx):
        canal_destino = self.bot.get_channel(self.CANAL_ROLES)
        if not canal_destino:
            await ctx.send(f"❌ Error: No encuentro el canal con ID {self.CANAL_ROLES}")
            return

        # 1. Intentamos sacar el emoji de la mochila
        mochila = self.bot.get_cog('EmojiManager')
        emoji_obj = mochila.get_emoji("campage") if mochila else None
        
        # 2. Si la mochila falla, lo buscamos directamente en el servidor
        if not emoji_obj:
            emoji_obj = discord.utils.get(ctx.guild.emojis, name="campage")

        # 3. Si por algún motivo divino no existe, ponemos el escudo
        emoji_campage = str(emoji_obj) if emoji_obj else "🛡️"

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

        embed = discord.Embed(description=descripcion, color=discord.Color.orange())
        embed.set_footer(text="Cromi System • Autoroles")

        nuevo_msg = await canal_destino.send(embed=embed)

        for emoji in self.roles_colores.keys():
            await nuevo_msg.add_reaction(emoji)
            
        await ctx.send("✅ Mensaje de colores generado.", delete_after=3)
        try: await ctx.message.delete()
        except: pass

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.user_id == self.bot.user.id: return
        emoji_name = str(payload.emoji)
        
        if emoji_name in self.roles_colores:
            guild = self.bot.get_guild(payload.guild_id)
            member = guild.get_member(payload.user_id)
            if not member: return

            roles_a_quitar = []
            for emoji, role_id in self.roles_colores.items():
                if role_id != self.roles_colores[emoji_name]:
                    rol = guild.get_role(role_id)
                    if rol and rol in member.roles:
                        roles_a_quitar.append(rol)
            
            if roles_a_quitar:
                await member.remove_roles(*roles_a_quitar)

            rol_nuevo = guild.get_role(self.roles_colores[emoji_name])
            if rol_nuevo: await member.add_roles(rol_nuevo)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        emoji_name = str(payload.emoji)
        if emoji_name in self.roles_colores:
            guild = self.bot.get_guild(payload.guild_id)
            member = guild.get_member(payload.user_id)
            if not member: return

            rol_a_quitar = guild.get_role(self.roles_colores[emoji_name])
            if rol_a_quitar and rol_a_quitar in member.roles:
                await member.remove_roles(rol_a_quitar)

async def setup(bot):
    await bot.add_cog(Autoroles(bot))
