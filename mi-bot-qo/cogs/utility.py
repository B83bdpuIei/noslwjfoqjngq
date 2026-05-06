import discord
from discord.ext import commands
from discord import app_commands

# --- FORMULARIO (MODAL) PARA AUTOROLES ---
class AutoRoleModal(discord.ui.Modal, title='Configuración de Auto-Roles'):
    titulo = discord.ui.TextInput(label='Título del Mensaje', placeholder='Ej: Elige tus roles')
    opcion1 = discord.ui.TextInput(label='Emoji y Nombre (Opción 1)', placeholder='🍎 | Rojo - ID:123456789...')
    opcion2 = discord.ui.TextInput(label='Emoji y Nombre (Opción 2)', placeholder='🔵 | Azul - ID:123456789...', required=False)
    
    async def on_submit(self, interaction: discord.Interaction):
        # Aquí crearíamos el mensaje con botones para que la gente haga clic
        await interaction.response.send_message(f"✅ Se ha configurado: **{self.titulo.value}**. (Lógica de asignación en desarrollo)", ephemeral=True)

# --- MENÚ DESPLEGABLE ---
class ConfigSelect(discord.ui.Select):
    def __init__(self, bot):
        self.bot = bot
        options = [
            discord.SelectOption(label="Autoroles", description="Configura roles por reacción", emoji="🎭"),
            discord.SelectOption(label="Sugerencias", description="Activa el sistema de votos", emoji="💡"),
            discord.SelectOption(label="Bienvenidas", description="Mensajes automáticos", emoji="👋")
        ]
        super().__init__(placeholder="Selecciona una automatización...", options=options)

    async def callback(self, interaction: discord.Interaction):
        if self.values[0] == "Autoroles":
            await interaction.response.send_modal(AutoRoleModal(self.bot))
        else:
            await interaction.response.send_message(f"Has seleccionado {self.values[0]}, pero aún estamos trabajando en ello.", ephemeral=True)

class ConfigView(discord.ui.View):
    def __init__(self, bot):
        super().__init__()
        self.add_item(ConfigSelect(bot))

# --- EL COG CON EL COMANDO / ---
class Utility(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="config", description="Configura las automatizaciones del servidor")
    async def config(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="⚙️ Panel de Configuración",
            description="Selecciona qué módulo quieres configurar en el menú de abajo.",
            color=discord.Color.gold()
        )
        await interaction.response.send_message(embed=embed, view=ConfigView(self.bot), ephemeral=True)

async def setup(bot):
    await bot.add_cog(Utility(bot))
