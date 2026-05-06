import discord
from discord.ext import commands
from discord import app_commands

# --- 1. LOS BOTONES QUE DAN LOS ROLES ---
class RoleButton(discord.ui.Button):
    def __init__(self, role_id: int, label: str, emoji: str):
        # Usamos custom_id para que el bot lo reconozca siempre
        super().__init__(
            label=label,
            style=discord.ButtonStyle.secondary,
            emoji=emoji,
            custom_id=f"role_{role_id}"
        )

    async def callback(self, interaction: discord.Interaction):
        # Extraemos el ID del rol del custom_id
        role_id = int(self.custom_id.split("_")[1])
        role = interaction.guild.get_role(role_id)

        if not role:
            return await interaction.response.send_message("❌ No encuentro ese rol.", ephemeral=True)

        try:
            if role in interaction.user.roles:
                await interaction.user.remove_roles(role)
                await interaction.response.send_message(f"🗑️ Rol quitado: **{role.name}**", ephemeral=True)
            else:
                await interaction.user.add_roles(role)
                await interaction.response.send_message(f"✅ Rol añadido: **{role.name}**", ephemeral=True)
        except discord.Forbidden:
            await interaction.response.send_message("❌ No tengo permisos suficientes (mi rol debe estar por encima del que quiero dar).", ephemeral=True)

# --- 2. EL FORMULARIO (MODAL) ---
class AutoRoleModal(discord.ui.Modal, title='Configurar Autoroles'):
    titulo_panel = discord.ui.TextInput(label='Título del Panel', placeholder='Ej: Roles de colores')
    rol_data = discord.ui.TextInput(
        label='Roles (Emoji | Nombre | ID)', 
        style=discord.TextStyle.paragraph,
        placeholder='🔴 | Rojo | 123456789\n🔵 | Azul | 987654321',
        required=True
    )

    async def on_submit(self, interaction: discord.Interaction):
        embed = discord.Embed(title=self.titulo_panel.value, color=discord.Color.green())
        view = discord.ui.View(timeout=None) # Los botones duran para siempre

        # Procesamos cada línea del cuadro de texto
        lines = self.rol_data.value.split('\n')
        for line in lines:
            if '|' in line:
                try:
                    parts = line.split('|')
                    emoji = parts[0].strip()
                    name = parts[1].strip()
                    r_id = int(parts[2].strip())
                    view.add_item(RoleButton(role_id=r_id, label=name, emoji=emoji))
                except Exception:
                    continue

        await interaction.channel.send(embed=embed, view=view)
        await interaction.response.send_message("✅ Panel enviado al canal.", ephemeral=True)

# --- 3. EL MENÚ DESPLEGABLE ---
class ConfigSelect(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="Autoroles", description="Configura el panel de botones", emoji="🎭"),
            discord.SelectOption(label="Sugerencias", description="Próximamente...", emoji="💡")
        ]
        super().__init__(placeholder="Selecciona una automatización...", options=options)

    async def callback(self, interaction: discord.Interaction):
        if self.values[0] == "Autoroles":
            # Aquí está el truco: enviamos el Modal directamente
            await interaction.response.send_modal(AutoRoleModal())
        else:
            await interaction.response.send_message("Esta opción aún no está disponible.", ephemeral=True)

class ConfigView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(ConfigSelect())

# --- 4. EL COMANDO /CONFIG ---
class Utility(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="config", description="Configura las funciones del bot")
    async def config(self, interaction: discord.Interaction):
        # Solo para administradores
        if not interaction.user.guild_permissions.administrator:
            return await interaction.response.send_message("❌ No tienes permisos.", ephemeral=True)
        
        embed = discord.Embed(
            title="⚙️ Panel de Configuración",
            description="Elige qué quieres configurar hoy:",
            color=discord.Color.blue()
        )
        await interaction.response.send_message(embed=embed, view=ConfigView(), ephemeral=True)

async def setup(bot):
    await bot.add_cog(Utility(bot))
