import discord
from discord.ext import commands

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="clear")
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, cantidad: int):
        await ctx.channel.purge(limit=cantidad + 1)
        await ctx.send(f"✅ Mensajes borrados: {cantidad}", delete_after=3)

async def setup(bot):
    await bot.add_cog(Moderation(bot))
