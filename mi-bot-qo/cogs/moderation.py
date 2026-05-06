import discord
from discord.ext import commands
from discord import app_commands
import asyncio

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="clear", description="Elimina mensajes (Incluso antiguos)")
    @app_commands.describe(cantidad="Número de mensajes a borrar")
    async def clear(self, interaction: discord.Interaction, cantidad: int):
        if not interaction.user.guild_permissions.manage_messages:
            return await interaction.response.send_message("❌ No tienes permisos.", ephemeral=True)
        
        await interaction.response.defer(ephemeral=True)
        deleted = await interaction.channel.purge(limit=cantidad, bulk=True)
        
        if len(deleted) < cantidad:
            async for message in interaction.channel.history(limit=cantidad - len(deleted)):
                try:
                    await message.delete()
                    await asyncio.sleep(1.2)
                except:
                    continue
        await interaction.followup.send(f"✅ Limpieza completada.", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Moderation(bot))
