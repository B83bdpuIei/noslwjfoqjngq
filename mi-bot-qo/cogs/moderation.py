import discord
from discord.ext import commands
from discord import app_commands
import asyncio

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="clear", description="Elimina mensajes (Incluso mayores de 14 días)")
    @app_commands.describe(cantidad="Número de mensajes a borrar")
    async def clear(self, interaction: discord.Interaction, cantidad: int):
        if not interaction.user.guild_permissions.manage_messages:
            return await interaction.response.send_message("❌ No tienes permisos para gestionar mensajes.", ephemeral=True)

        if cantidad < 1 or cantidad > 100:
            return await interaction.response.send_message("❌ Por favor, elige un número entre 1 y 100.", ephemeral=True)

        await interaction.response.defer(ephemeral=True)

        try:
            # Intento de borrado masivo (rápido)
            deleted = await interaction.channel.purge(limit=cantidad, bulk=True)
            
            # Si faltan mensajes por borrar (son antiguos)
            if len(deleted) < cantidad:
                restantes = cantidad - len(deleted)
                await interaction.followup.send(f"✅ Se borraron {len(deleted)} mensajes nuevos. Borrando {restantes} antiguos uno a uno...", ephemeral=True)
                
                async for message in interaction.channel.history(limit=restantes):
                    try:
                        await message.delete()
                        await asyncio.sleep(1.2) # Evita el baneo de Discord por spam
                    except:
                        continue
                await interaction.followup.send("✨ Limpieza total completada.", ephemeral=True)
            else:
                await interaction.followup.send(f"✅ Se han eliminado **{len(deleted)}** mensajes.", ephemeral=True)
                
        except Exception as e:
            await interaction.followup.send(f"❌ Ocurrió un error: {e}", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Moderation(bot))
