import discord
from discord.ext import commands
import asyncio

class Suggestions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.emojis = ['✅', '〰️', '❌']

    @commands.command(name="suggest")
    async def suggest(self, ctx, *, sugerencia: str):
        # Borramos el mensaje del comando después de 5 segundos
        try:
            await ctx.message.delete(delay=5.0)
        except:
            pass

        embed = discord.Embed(
            title=ctx.author.name,
            description=sugerencia,
            color=0x00BFFF
        )
        embed.set_footer(text="Cromi System • Suggest")
        
        msg = await ctx.send(embed=embed)
        
        for emoji in self.emojis:
            await msg.add_reaction(emoji)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.user_id == self.bot.user.id:
            return

        canal = self.bot.get_channel(payload.channel_id)
        mensaje = await canal.fetch_message(payload.message_id)
        usuario = self.bot.get_user(payload.user_id)

        if mensaje.author == self.bot.user and mensaje.embeds:
            footer_text = mensaje.embeds[0].footer.text
            if footer_text and "Cromi System • Suggest" in footer_text:
                if str(payload.emoji) in self.emojis:
                    # Sistema de voto único
                    for reaction in mensaje.reactions:
                        if str(reaction.emoji) != str(payload.emoji) and str(reaction.emoji) in self.emojis:
                            # Solo intentamos quitar la reacción si el usuario que reaccionó es el mismo
                            async for user in reaction.users():
                                if user.id == payload.user_id:
                                    await mensaje.remove_reaction(reaction.emoji, usuario)

async def setup(bot):
    await bot.add_cog(Suggestions(bot))
