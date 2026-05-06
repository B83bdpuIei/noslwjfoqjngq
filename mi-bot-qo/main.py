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
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        # Cargamos los archivos de la carpeta cogs
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py') and not filename.startswith('__'):
                await self.load_extension(f'cogs.{filename[:-3]}')
        
        # Esto sincroniza los comandos "/" con los servidores de Discord
        await self.tree.sync()
        print("✅ Comandos / sincronizados globalmente.")

bot = MyBot()

@bot.event
async def on_ready():
    print(f'🤖 {bot.user} conectado y listo.')
    keep_alive()

async def main():
    async with bot:
        token = os.getenv('DISCORD_TOKEN')
        await bot.start(token)

if __name__ == '__main__':
    asyncio.run(main())
