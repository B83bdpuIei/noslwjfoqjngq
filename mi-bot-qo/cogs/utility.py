import discord
from discord.ext import commands
from discord import app_commands

class Utility(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="config", description="Panel de configuración de automatizaciones")
    async def config(self, interaction: discord.Interaction):
        if not interaction.user.guild_permissions.administrator:
            return await interaction.response.send_message("❌ Solo administradores pueden usar esto.", ephemeral=True)
        
        embed = discord.Embed(
            title="⚙️ Configuración del Bot",
            description="Módulo de automatizaciones en desarrollo. \n\nPróximamente: Sugerencias y Auto-Roles.",
            color=discord.Color.blue()
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(bot):
    await bot.add_cog(Utility(bot))
