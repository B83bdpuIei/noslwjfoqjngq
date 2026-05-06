import discord
from discord.ext import commands
import asyncio

class Suggestions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.emojis = ['✅', '〰️', '❌']

    @commands.command(name="suggest")
    async def suggest(self, ctx, *, sugerencia: str = None):
        # Si el usuario solo pone .suggest sin nada, borramos y salimos
        if sugerencia is None:
            try: await ctx.message.delete()
            except: pass
            return

        # Borramos el mensaje del comando después de 5 segundos para que se vea limpio
        try: await ctx.message.delete(delay=5.0)
        except: pass

        embed = discord.Embed(
            description=sugerencia,
            color=0x00BFFF
        )
        # Ponemos el nombre y la foto del autor arriba
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.display_avatar.url)
        embed.set_footer(text="Cromi System • Suggest")
        
        msg = await ctx.send(embed=embed)
        
        for emoji in self.emojis:
            await msg.add_reaction(emoji)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.user_id == self.bot.user.id: return

        canal = self.bot.get_channel(payload.channel_id)
        mensaje = await canal.fetch_message(payload.message_id)
        
        if mensaje.author == self.bot.user and mensaje.embeds:
            footer = mensaje.embeds[0].footer.text
            if footer and "Cromi System • Suggest" in footer:
                if str(payload.emoji) in self.emojis:
                    # Sistema de voto único
                    for reaction in mensaje.reactions:
                        if str(reaction.emoji) != str(payload.emoji) and str(reaction.emoji) in self.emojis:
                            async for user in reaction.users():
                                if user.id == payload.user_id:
                                    await mensaje.remove_reaction(reaction.emoji, user)

async def setup(bot):
    await bot.add_cog(Suggestions(bot))
