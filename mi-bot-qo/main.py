import discord
from discord.ext import commands
import os
import asyncio
from keep_alive import keep_alive

# --- Configuración ---
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Función global para el canal de notas
async def log_to_private_channel(guild, content):
    channel = discord.utils.get(guild.text_channels, name="bot-notas-privadas")
    if not channel:
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            guild.me: discord.PermissionOverwrite(read_messages=True)
        }
        channel = await guild.create_text_channel('bot-notas-privadas', overwrites=overwrites)
    await channel.send(content)

# Inyectamos la función en el bot para que los Cogs la usen fácil
bot.log_notes = log_to_private_channel

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
    await bot.change_presence(activity=discord.Game(name="!dashboard"))

async def main():
    async with bot:
        await load_extensions()
        keep_alive() # Arranca el servidor web antes que el bot
        token = os.getenv('DISCORD_TOKEN')
        if token:
            await bot.start(token)
        else:
            print("❌ ERROR: Falta la variable DISCORD_TOKEN en Render")

if __name__ == '__main__':
    asyncio.run(main())
