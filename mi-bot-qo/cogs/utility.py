import discord
from discord.ext import commands
from discord import app_commands

# --- LÓGICA DE ASIGNACIÓN DE ROLES (BOTONES) ---
class RoleButton(discord.ui.Button):
    def __init__(self, role_id: int, label: str, emoji: str):
        super().__init__(
            label=label, 
            style=discord.ButtonStyle.secondary, 
            emoji=emoji, 
            custom_id=f"role_{role_id}" # ID único para persistencia
        )

    async def callback(self, interaction: discord.Interaction):
        role_id = int(self.custom_id.split("_")[1])
        role = interaction.guild.get_role(role_id)

        if role is None:
            return await interaction.response.send_message("❌ No encuentro ese rol en el servidor.", ephemeral=True)

        if role in interaction.user.roles:
            await interaction.user.remove_roles(role)
            await interaction.response.send_message(f"🗑️ Se te ha quitado el rol **{role.name}**", ephemeral=True)
        else:
            await interaction.user.add_roles(role)
            await interaction.response.send_message(f"✅ Ahora tienes el rol **{role.name}**", ephemeral=True)

# --- FORMULARIO PARA CREAR EL PANEL ---
class AutoRoleModal(discord.ui.Modal, title='Configurar Panel de Roles'):
    titulo = discord.ui.TextInput(label='Título del Panel', placeholder='Ej: Elige tus Colores')
    desc = discord.ui.TextInput(label='Descripción', style=discord.TextStyle.paragraph, placeholder='Pulsa los botones para obtener roles...')
    
    # Pedimos formato: Emoji, Nombre, ID
    rol1 = discord.ui.TextInput(label='Rol 1 (Emoji | Nombre | ID)', placeholder='🔴 | Rojo | 123456789...')
    rol2 = discord.ui.TextInput(label='Rol 2 (Emoji | Nombre | ID)', placeholder='🔵 | Azul | 123456789...', required=False)
    rol3 = discord.ui.TextInput(label='Rol 3 (Emoji | Nombre | ID)', placeholder='🟢 | Verde | 123456789...', required=False)

    async def on_submit(self, interaction: discord.Interaction):
        embed = discord.Embed(title=self.titulo.value, description=self.desc.value, color=discord.Color.blue())
        view = discord.ui.View(timeout=None)

        # Procesar los roles ingresados
        roles_data = [self.rol1.value, self.rol2.value, self.rol3.value]
        
        for r_info in roles_data:
            if r_info:
                try:
                    parts = r_info.split("|")
                    emoji = parts[0].strip()
                    name = parts[1].strip()
                    r_id = int(parts[2].strip())
                    view.add_item(RoleButton(role_id=r_id, label=name, emoji=emoji))
                except:
                    continue

        await interaction.channel.send(embed=embed, view=view)
        await interaction.response.send_message("✅ Panel de Autoroles creado con éxito.", ephemeral=True)

# --- MENÚ DESPLEGABLE ---
class ConfigSelect(discord.ui.Select):
    def __init__(self, bot):
        self.bot = bot
        options = [
            discord.SelectOption(label="Autoroles", description="Crea un panel con botones", emoji="🎭"),
            discord.SelectOption(label="Sugerencias", description="Activa el buzón", emoji="💡")
        ]
        super().__init__(placeholder="Elige una opción...", options=options)

    async def callback(self, interaction: discord.Interaction):
        if self.values[0] == "Autoroles":
            await interaction.response.send_modal(AutoRoleModal())
        else:
            await interaction.response.send_message("Módulo en construcción...", ephemeral=True)

class ConfigView(discord.ui.View):
    def __init__(self, bot):
        super().__init__()
        self.add_item(ConfigSelect(bot))

class Utility(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="config", description="Panel de configuración")
    async def config(self, interaction: discord.Interaction):
        if not interaction.user.guild_permissions.administrator:
            return await interaction.response.send_message("❌ Solo admins pueden usar esto.", ephemeral=True)
        
        embed = discord.Embed(title="⚙️ Configuración del Servidor", color=discord.Color.gold())
        await interaction.response.send_message(embed=embed, view=ConfigView(self.bot), ephemeral=True)

async def setup(bot):
    await bot.add_cog(Utility(bot))
