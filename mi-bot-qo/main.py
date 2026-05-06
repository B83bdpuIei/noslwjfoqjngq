# main.py
import discord
from discord.ext import commands
import os
import asyncio
from keep_alive import keep_alive # Importamos el truco de Render

# --- Configuración Básica del Bot ---
intents = discord.Intents.default()
intents.message_content = True # NECESARIO para comandos de texto (!clear)
intents.members = True          # NECESARIO para bienvenidas

# Definimos el prefijo y los intents
bot = commands.Bot(command_prefix="!", intents=intents)

# --- Carga Automática de Cogs ---
async def load_extensions():
    # Buscamos archivos .py dentro de la carpeta 'cogs'
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py') and not filename.startswith('__'):
            # El formato es 'cogs.nombre_del_archivo'
            extension_name = f'cogs.{filename[:-3]}'
            try:
                await bot.load_extension(extension_name)
                print(f'✅ Extensión cargada: {extension_name}')
            except Exception as e:
                print(f'❌ Error cargando {extension_name}: {e}')

# --- Evento: Bot Listo ---
@bot.event
async def on_ready():
    print(f'------------------------------------')
    print(f'🤖 Bot online como: {bot.user.name}')
    print(f'🆔 ID: {bot.user.id}')
    print(f'🛠️ Prefijo: {bot.command_prefix}')
    print(f'------------------------------------')
    
    # Establecemos una actividad para el bot
    await bot.change_presence(activity=discord.Game(name="¡Usa !dashboard!"))

# --- Punto de Entrada Principal ---
async def main():
    async with bot:
        # 1. Cargamos los módulos (Cogs)
        await load_extensions()
        
        # 2. Arrancamos el servidor web para Render
        keep_alive()
        
        # 3. Iniciamos el bot con el TOKEN (desde variables de entorno)
        token = os.getenv('DISCORD_TOKEN')
        if token is None:
            print("❌ ERROR: No se encontró la variable de entorno 'DISCORD_TOKEN'.")
        else:
            await bot.start(token)

if __name__ == '__main__':
    # Ejecutamos la función principal asíncrona
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot apagado por el usuario.")
