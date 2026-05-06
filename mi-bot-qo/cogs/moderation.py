import discord
from discord.ext import commands
from discord import app_commands

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Comando de barra /clear
    @app_commands.command(name="clear", description="Elimina una cantidad de mensajes (1-100)")
    @app_commands.describe(cantidad="Número de mensajes a borrar (máximo 100)")
    async def clear(self, interaction: discord.Interaction, cantidad: int):
        # Verificación de permisos
        if not interaction.user.guild_permissions.manage_messages:
            return await interaction.response.send_message("❌ No tienes permiso para gestionar mensajes.", ephemeral=True)

        # Validación del rango
        if cantidad < 1 or cantidad > 100:
            return await interaction.response.send_message("❌ La cantidad debe estar entre 1 y 100.", ephemeral=True)

        # Respondemos primero para evitar el error de "Interacción fallida"
        await interaction.response.defer(ephemeral=True)

        try:
            # Borramos los mensajes
            deleted = await interaction.channel.purge(limit=cantidad)
            await interaction.followup.send(f"✅ Se han eliminado **{len(deleted)}** mensajes.", ephemeral=True)
        except Exception as e:
            await interaction.followup.send(f"❌ Error al intentar borrar: {e}", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Moderation(bot))
