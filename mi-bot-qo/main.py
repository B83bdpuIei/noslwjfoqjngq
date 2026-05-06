import discord
from discord.ext import commands
import os
import asyncio
from keep_alive import keep_alive

# --- Configuración ---
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True # Necesario para crear/ver canales

bot = commands.Bot(command_prefix="!", intents=intents)

# Función para enviar datos al canal privado de notas
async def log_to_private_channel(guild, content):
    # Busca un canal llamado 'bot-notas-privadas'
    channel = discord.utils.get(guild.text_channels, name="bot-notas-privadas")
    
    # Si no existe, lo crea
    if not channel:
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False), # Nadie lo ve
            guild.me: discord.PermissionOverwrite(read_messages=True)           # El bot sí
        }
        channel = await guild.create_text_channel('bot-notas-privadas', overwrites=overwrites)
        await channel.send("📝 **Canal de Notas Digitales creado.** Aquí guardaré la información necesaria.")
    
    await channel.send(content)

async def load_extensions():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py') and not filename.startswith('__'):
            try:
                await bot.load_extension(f'cogs.{filename[:-3]}')
                print(f'✅ Cargado: {filename}')
            except Exception as e:
                print(f'❌ Error en {filename}: {e}')

@bot.event
async def on_ready():
    print(f'🤖 Bot online: {bot.user.name}')
    keep_alive()

async def main():
    async with bot:
        await load_extensions()
        token = os.getenv('DISCORD_TOKEN')
        await bot.start(token)

if __name__ == '__main__':
    asyncio.run(main())
