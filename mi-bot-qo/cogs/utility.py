import discord
from discord.ext import commands

class NoteModal(discord.ui.Modal, title='Nueva Nota Digital'):
    nota_input = discord.ui.TextInput(
        label='Información a guardar',
        style=discord.TextStyle.long,
        placeholder='Escribe aquí...',
        required=True
    )

    def __init__(self, bot):
        super().__init__()
        self.bot = bot

    async def on_submit(self, interaction: discord.Interaction):
        await self.bot.log_notes(interaction.guild, f"📌 **Nota de {interaction.user}:**\n{self.nota_input.value}")
        await interaction.response.send_message("✅ Guardado en el canal privado.", ephemeral=True)

class DashboardView(discord.ui.View):
    def __init__(self, bot):
        super().__init__(timeout=None)
        self.bot = bot

    @discord.ui.button(label="Auto-Roles", style=discord.ButtonStyle.primary, emoji="🎭")
    async def autoroles(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("⚙️ Próximamente...", ephemeral=True)

    @discord.ui.button(label="Enviar Nota", style=discord.ButtonStyle.danger, emoji="📝")
    async def send_note(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(NoteModal(self.bot))

class Utility(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="dashboard")
    async def dashboard(self, ctx):
        embed = discord.Embed(title="🛠️ Panel de Control", color=discord.Color.blue())
        await ctx.send(embed=embed, view=DashboardView(self.bot))

async def setup(bot):
    await bot.add_cog(Utility(bot))
