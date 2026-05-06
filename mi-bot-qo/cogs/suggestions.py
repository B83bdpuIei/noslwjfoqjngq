import discord
from discord.ext import commands
import asyncio

class Suggestions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.emojis = ['✅', '🤔', '❌'] # Emoji de la mitad cambiado

    async def mover_info(self, canal):
        # Busca el recordatorio viejo y lo borra
        async for msg in canal.history(limit=20):
            if msg.author == self.bot.user and msg.embeds:
                if "💡 **¿Tienes alguna idea?**" in msg.embeds[0].description:
                    await msg.delete()
                    break
        
        # Envía el nuevo recordatorio
        embed = discord.Embed(
            description="💡 **¿Tienes alguna idea?**\nUsa el comando `.suggest [tu sugerencia]` para enviar una propuesta al equipo.",
            color=0x00BFFF
        )
        embed.set_footer(text="Cromi System • Info")
        await canal.send(embed=embed)

    @commands.command(name="suggest")
    async def suggest(self, ctx, *, sugerencia: str = None):
        if sugerencia is None:
            try: await ctx.message.delete()
            except: pass
            return

        # Borrar el comando .suggest a los 5 segundos
        try: await ctx.message.delete(delay=5.0)
        except: pass

        embed = discord.Embed(description=sugerencia, color=0x00BFFF)
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.display_avatar.url)
        embed.set_footer(text="Cromi System • Suggest")
        
        msg = await ctx.send(embed=embed)
        
        for emoji in self.emojis:
            await msg.add_reaction(emoji)
        
        # Mover el mensaje informativo al final
        await self.mover_info(ctx.channel)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.user_id == self.bot.user.id: return
        canal = self.bot.get_channel(payload.channel_id)
        mensaje = await canal.fetch_message(payload.message_id)
        
        if mensaje.author == self.bot.user and mensaje.embeds:
            footer = mensaje.embeds[0].footer.text
            if footer and "Cromi System • Suggest" in footer:
                if str(payload.emoji) in self.emojis:
                    for reaction in mensaje.reactions:
                        if str(reaction.emoji) != str(payload.emoji) and str(reaction.emoji) in self.emojis:
                            async for user in reaction.users():
                                if user.id == payload.user_id:
                                    await mensaje.remove_reaction(reaction.emoji, user)

async def setup(bot):
    await bot.add_cog(Suggestions(bot))
