import discord
from discord.ext import commands
import os
import asyncio
from keep_alive import keep_alive

class MyBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        intents.guilds = True
        intents.voice_states = True 
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        # Carga de extensiones (Cogs)
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py') and not filename.startswith('__'):
                try:
                    await self.load_extension(f'cogs.{filename[:-3]}')
                    print(f'✅ Extensión cargada: {filename}')
                except Exception as e:
                    print(f'❌ Error cargando {filename}: {e}')
        
        # Sincronización de comandos de barra (/)
        await self.tree.sync()
        print("✅ Comandos / sincronizados.")

bot = MyBot()

# --- CONFIGURACIÓN DE CANALES DINÁMICOS ---
ID_CANAL_CREADOR = 1500872439943532699 
canales_activos = []

@bot.event
async def on_voice_state_update(member, before, after):
    # 1. CREACIÓN: El usuario entra al canal generador
    if after.channel and after.channel.id == ID_CANAL_CREADOR:
        guild = member.guild
        category = after.channel.category
        
        # Overwrites: Le damos permisos de Administrar Canal solo en SU sala
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(connect=True),
            member: discord.PermissionOverwrite(
                manage_channels=True, 
                manage_permissions=True,
                move_members=True, 
                mute_members=True,
                deafen_members=True
            )
        }
        
        nuevo_canal = await guild.create_voice_channel(
            name=f"🎙️ Sala de {member.name}",
            category=category,
            overwrites=overwrites
        )
        
        await member.move_to(nuevo_canal)
        canales_activos.append(nuevo_canal.id)

    # 2. LIMPIEZA: El canal se queda vacío
    if before.channel and before.channel.id in canales_activos:
        if len(before.channel.members) == 0:
            try:
                await before.channel.delete()
                canales_activos.remove(before.channel.id)
            except discord.NotFound:
                if before.channel.id in canales_activos:
                    canales_activos.remove(before.channel.id)
            except Exception as e:
                print(f"Error al limpiar canal: {e}")

@bot.event
async def on_ready():
    print(f'------------------------------------')
    print(f'🤖 Bot: {bot.user.name}')
    print(f'🟢 Estado: Online')
    print(f'------------------------------------')
    keep_alive()

async def main():
    async with bot:
        token = os.getenv('DISCORD_TOKEN')
        if token:
            await bot.start(token)
        else:
            print("❌ ERROR: No se encontró DISCORD_TOKEN en las variables de entorno.")

if __name__ == '__main__':
    asyncio.run(main())
