import discord
from discord.ext import commands
from discord import app_commands
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
        # Carga de Cogs
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py') and not filename.startswith('__'):
                await self.load_extension(f'cogs.{filename[:-3]}')
        
        # Sincroniza los comandos de barra (/) con Discord
        await self.tree.sync()
        print("✅ Comandos de barra sincronizados.")

bot = MyBot()

@bot.event
async def on_ready():
    print(f'🤖 {bot.user.name} está online.')
    keep_alive()

async def main():
    async with bot:
        token = os.getenv('DISCORD_TOKEN')
        await bot.start(token)

if __name__ == '__main__':
    asyncio.run(main())
