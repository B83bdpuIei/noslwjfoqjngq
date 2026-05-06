import discord
from discord.ext import commands

class DashboardView(discord.ui.View):
    def __init__(self, bot):
        self.bot = bot
        super().__init__(timeout=None)

    @discord.ui.button(label="Auto-Roles", style=discord.ButtonStyle.primary, emoji="🎭")
    async def autoroles_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("⚙️ Configuración de Auto-Roles próximamente...", ephemeral=True)

    @discord.ui.button(label="Sugerencias", style=discord.ButtonStyle.success, emoji="💡")
    async def suggestions_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("💡 Configuración de Sugerencias próximamente...", ephemeral=True)

    @discord.ui.button(label="Enviar Nota", style=discord.ButtonStyle.danger, emoji="📝")
    async def note_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        # Usamos un Modal (ventana emergente) para escribir la nota
        modal = NoteModal(self.bot)
        await interaction.response.send_modal(modal)

# Ventana emergente para escribir la nota
class NoteModal(discord.ui.Modal, title='Nueva Nota Digital'):
    nota_content = discord.ui.TextInput(
        label='¿Qué quieres guardar?',
        style=discord.TextStyle.long,
        placeholder='Escribe aquí la información importante...',
        required=True,
    )

    def __init__(self, bot):
        super().__init__()
        self.bot = bot

    async def on_submit(self, interaction: discord.Interaction):
        # Buscamos el canal de notas usando la lógica de main.py (simplificada aquí)
        from main import log_to_private_channel
        await log_to_private_channel(interaction.guild, f"📌 **Nueva nota de {interaction.user.name}:**\n{self.nota_content.value}")
        await interaction.response.send_message("✅ Nota guardada en el canal privado.", ephemeral=True)

class Utility(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="dashboard")
    async def dashboard(self, ctx):
        embed = discord.Embed(
            title="🛠️ Panel de Control - Mejora de Vida",
            description="Gestiona las funciones del bot desde aquí.",
            color=discord.Color.blue()
        )
        await ctx.send(embed=embed, view=DashboardView(self.bot))

async def setup(bot):
    await bot.add_cog(Utility(bot))
