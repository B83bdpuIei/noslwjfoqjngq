import discord
from discord.ext import commands

class Autoroles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.CANAL_ROLES = 1501564084477235301

        # --- DICCIONARIOS DE ROLES ---
        self.roles_colores = {
            "❤️": 1501554375204802671,
            "🧡": 1501554811185664010,
            "💛": 1501554310960648302,
            "💚": 1501554496067862661,
            "🩵": 1501554174381523045,
            "🩷": 1501553906298392636,
            "💜": 1501554569719844986
        }

        self.roles_clases = {
            "<:guerrero:1501603848240894062>": 1501949098301984828,
            "<:picaro:1501604017292316692>": 1501949273984466954,
            "<:mago:1501603897637212310>": 1501949311116640397,
            "<:sacerdote:1501605504823328928>": 1501949344574865648,
            "<:cazador:1501604289808830484>": 1501949363344375908,
            "<:druida:1501605445008228493>": 1501949424719499264,
            "<:chaman:1501604072950726806>": 1501949450971775116,
            "<:paladin:1501604338903154879>": 1501949472165335061,
            "<:dk:1501604217100570705>": 1501949485369131098,
            "<:brujo:1501604123659735243>": 1501949616403386469,
            "<:monje:1501603949445255368>": 1501949636196307044,
            "<:dh:1501605335201349847>": 1501949668425207968,
            "<:evocador:1501604167003930644>": 1501997005147213946
        }

        self.roles_profesiones = {
            "🔮": 1501947899058061445,
            "📜": 1501947962992103455,
            "⚙️": 1501948000543576177,
            "🧥": 1501948043698766017,
            "🧪": 1501948071595085914,
            "🛡️": 1501948414126981290,
            "💎": 1501948566917353483,
            "🧵": 1501948595950059562,
            "🔪": 1501948622500266034,
            "🌿": 1501948648131530802,
            "⛏️": 1501948673142292620,
            "🏳️": 1501948696122622064
        }

    # --- COMANDOS GENERADORES ---

    @commands.command(name="generar_colores")
    @commands.has_permissions(administrator=True)
    async def generar_colores(self, ctx):
        canal = self.bot.get_channel(self.CANAL_ROLES)
        descripcion = (
            "<:campage:1501596925080764586> **¡Elige tu color!**\n"
            "Reacciona con el emoji del color que más te guste:\n\n"
            "❤️ | Rojo\n🧡 | Naranja\n💛 | Amarillo\n💚 | Verde\n"
            "🩵 | Azul\n🩷 | Rosa\n💜 | Morado\n\n"
            "Dale color a tu nombre y personalízate, hazte notar 🎨"
        )
        embed = discord.Embed(description=descripcion, color=discord.Color.orange())
        embed.set_footer(text="Cromi System • Autoroles")
        msg = await canal.send(embed=embed)
        for emoji in self.roles_colores.keys():
            await msg.add_reaction(emoji)
        await ctx.message.delete()

    @commands.command(name="generar_clases")
    @commands.has_permissions(administrator=True)
    async def generar_clases(self, ctx):
        canal = self.bot.get_channel(self.CANAL_ROLES)
        descripcion = (
            "<:campage:1501596925080764586> **¡Elige tu clase!**\n"
            "Reacciona con la clase que juegas en WoW (Máximo 3):\n\n"
            "<:guerrero:1501603848240894062> | Guerrero\n<:picaro:1501604017292316692> | Pícaro\n"
            "<:mago:1501603897637212310> | Mago\n<:sacerdote:1501605504823328928> | Sacerdote\n"
            "<:cazador:1501604289808830484> | Cazador\n<:druida:1501605445008228493> | Druida\n"
            "<:chaman:1501604072950726806> | Chamán\n<:paladin:1501604338903154879> | Paladín\n"
            "<:dk:1501604217100570705> | Caballero de la Muerte\n<:brujo:1501604123659735243> | Brujo\n"
            "<:monje:1501603949445255368> | Monje\n<:dh:1501605335201349847> | Cazador de Demonios\n"
            "<:evocador:1501604167003930644> | Evocador\n\n"
            "Encuentra sinergias y arma grupos <a:LFG:1501598403895885834>"
        )
        embed = discord.Embed(description=descripcion, color=discord.Color.orange())
        embed.set_footer(text="Cromi System • Autoroles")
        msg = await canal.send(embed=embed)
        for emoji in self.roles_clases.keys():
            await msg.add_reaction(emoji)
        await ctx.message.delete()

    @commands.command(name="generar_profesiones")
    @commands.has_permissions(administrator=True)
    async def generar_profesiones(self, ctx):
        canal = self.bot.get_channel(self.CANAL_ROLES)
        descripcion = (
            "<:campage:1501596925080764586> **¡Elige tus profesiones y encuentra a tu equipo!**\n"
            "Reacciona con el emoji de las profesiones que tengas en WoW:\n\n"
            "🔮 | Encantamiento\n📜 | Inscripción\n⚙️ | Ingeniería\n"
            "🧥 | Peletería\n🧪 | Alquimia\n🛡️ | Herrería\n"
            "💎 | Joyería\n🧵 | Sastrería\n🔪 | Desuello\n"
            "🌿 | Herboristería\n⛏️ | Minería\n🏳️ | No cotizo\n\n"
            "Encuentra crafters, comparte recursos y saca partido 🔥"
        )
        embed = discord.Embed(description=descripcion, color=discord.Color.orange())
        embed.set_footer(text="Cromi System • Autoroles")
        msg = await canal.send(embed=embed)
        for emoji in self.roles_profesiones.keys():
            await msg.add_reaction(emoji)
        await ctx.message.delete()

    # --- LÓGICA DE AÑADIR ROLES ---

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.user_id == self.bot.user.id: return
        emoji_name = str(payload.emoji)
        
        guild = self.bot.get_guild(payload.guild_id)
        member = guild.get_member(payload.user_id)
        if not member: return

        # 1. SISTEMA DE COLORES (Máximo 1, se sustituye)
        if emoji_name in self.roles_colores:
            roles_a_quitar = [guild.get_role(r_id) for e, r_id in self.roles_colores.items() if e != emoji_name and guild.get_role(r_id) in member.roles]
            if roles_a_quitar:
                await member.remove_roles(*roles_a_quitar)
            rol_nuevo = guild.get_role(self.roles_colores[emoji_name])
            if rol_nuevo: await member.add_roles(rol_nuevo)

        # 2. SISTEMA DE CLASES (Máximo 3, se bloquea)
        elif emoji_name in self.roles_clases:
            # Contamos cuántos roles de clase tiene ya el usuario
            clases_actuales = [rol for rol in member.roles if rol.id in self.roles_clases.values()]
            
            if len(clases_actuales) >= 3:
                # Si ya tiene 3, le quitamos la reacción para que vea que no puede
                canal = self.bot.get_channel(payload.channel_id)
                if canal:
                    try:
                        mensaje = await canal.fetch_message(payload.message_id)
                        await mensaje.remove_reaction(payload.emoji, member)
                        # Le avisamos (el mensaje se borra solo a los 4 segundos)
                        await canal.send(f"❌ {member.mention}, solo puedes elegir un máximo de **3 clases**.", delete_after=4)
                    except: pass
                return # Detenemos aquí para no darle el cuarto rol
            
            # Si tiene menos de 3, le damos el rol normal
            rol_nuevo = guild.get_role(self.roles_clases[emoji_name])
            if rol_nuevo: await member.add_roles(rol_nuevo)

        # 3. SISTEMA DE PROFESIONES (Ilimitados)
        elif emoji_name in self.roles_profesiones:
            rol_nuevo = guild.get_role(self.roles_profesiones[emoji_name])
            if rol_nuevo: await member.add_roles(rol_nuevo)

    # --- LÓGICA DE QUITAR ROLES ---

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        emoji_name = str(payload.emoji)
        guild = self.bot.get_guild(payload.guild_id)
        member = guild.get_member(payload.user_id)
        if not member: return

        # Si quitan la reacción, buscamos de qué sistema era y le quitamos el rol
        rol_id = None
        if emoji_name in self.roles_colores: rol_id = self.roles_colores[emoji_name]
        elif emoji_name in self.roles_clases: rol_id = self.roles_clases[emoji_name]
        elif emoji_name in self.roles_profesiones: rol_id = self.roles_profesiones[emoji_name]

        if rol_id:
            rol_a_quitar = guild.get_role(rol_id)
            if rol_a_quitar and rol_a_quitar in member.roles:
                await member.remove_roles(rol_a_quitar)

async def setup(bot):
    await bot.add_cog(Autoroles(bot))
