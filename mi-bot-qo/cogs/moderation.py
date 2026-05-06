# cogs/moderation.py
import discord
from discord.ext import commands

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="clear", aliases=["purge", "borrar"], help="Elimina una cantidad específica de mensajes.")
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, cantidad: int):
        """Elimina 'x' cantidad de mensajes."""
        if cantidad <= 0:
            await ctx.send("❌ Por favor, introduce un número mayor que 0.", delete_after=5)
            return

        # Sumamos 1 para borrar también el comando del usuario
        deleted = await ctx.channel.purge(limit=cantidad + 1)
        
        # Mensaje de confirmación temporal
        confirm_msg = await ctx.send(f"✅ Se han eliminado **{len(deleted) - 1}** mensajes correctamente.", delete_after=5)

    # Manejo de errores para el comando clear
    @clear.error
    async def clear_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("❌ No tienes permisos para gestionar mensajes.", delete_after=5)
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("❌ Uso incorrecto: `!clear [cantidad]`", delete_after=5)
        elif isinstance(error, commands.BadArgument):
            await ctx.send("❌ Uso incorrecto: La cantidad debe ser un número entero.", delete_after=5)

async def setup(bot):
    await bot.add_cog(Moderation(bot))
