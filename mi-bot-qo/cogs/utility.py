# cogs/utility.py
import discord
from discord.ext import commands
from discord import app_commands # Para comandos de barra si los quieres usar luego

# --- Definición del Dashboard (Vista con Botones) ---
class DashboardView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None) # Timeout=None para que los botones no caduquen

    @discord.ui.button(label="Auto-Roles", style=discord.ButtonStyle.primary, emoji="🎭", custom_id="db_autoroles")
    async def autoroles_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        # Esta es la lógica que se ejecuta al pulsar el botón
        embed = discord.Embed(title="🎭 Configuración de Auto-Roles", description="Usa el comando `/autoroles setup` para crear un panel de roles.", color=discord.Color.blue())
        await interaction.response.send_message(embed=embed, ephemeral=True) # Ephemeral=True solo lo ve quien pulsa

    @discord.ui.button(label="Bienvenida", style=discord.ButtonStyle.success, emoji="👋", custom_id="db_welcome")
    async def welcome_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(title="👋 Configuración de Bienvenida", description="Usa el comando `/welcome setchannel` y `/welcome message`.", color=discord.Color.green())
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @discord.ui.button(label="Sugerencias", style=discord.ButtonStyle.secondary, emoji="💡", custom_id="db_suggestions")
    async def suggestions_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(title="💡 Configuración de Sugerencias", description="Usa el comando `/suggestions setchannel`.", color=discord.Color.gold())
        await interaction.response.send_message(embed=embed, ephemeral=True)

# --- Clase del Cog (El contenedor de comandos) ---
class Utility(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="dashboard", aliases=["panel", "db"], help="Abre el panel de control interactivo del bot.")
    async def dashboard(self, ctx):
        """Muestra el panel de control interactivo."""
        embed = discord.Embed(
            title="🛠️ Panel de Control - Mejora de Vida",
            description="Bienvenido al centro de configuración. Pulsa los botones de abajo para gestionar cada módulo.",
            color=discord.Color.blurple()
        )
        embed.set_footer(text="Solo los administradores pueden ver este panel.")
        
        # Enviamos el embed junto con la vista (los botones)
        await ctx.send(embed=embed, view=DashboardView())

    # --- Aquí irían los comandos 'reales' para configurar cada cosa ---
    # Por ahora solo hemos creado el Dashboard interactivo que te guía.
    # ¡Necesitarás programar la lógica completa de sugerencias y bienvenida!

async def setup(bot):
    await bot.add_cog(Utility(bot))
