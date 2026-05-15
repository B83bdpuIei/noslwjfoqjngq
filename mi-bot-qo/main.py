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
        super().__init__(command_prefix=".", intents=intents)

    async def setup_hook(self):
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py') and not filename.startswith('__'):
                try:
                    await self.load_extension(f'cogs.{filename[:-3]}')
                except Exception as e:
                    print(f'❌ Error cargando {filename}: {e}')
        await self.tree.sync()

bot = MyBot()

# --- CONFIGURACIÓN ---
ID_CANAL_CREADOR = 1500872439943532699 
ID_CANAL_SUGERENCIAS = 1501564312265687213

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    # Si escriben en el canal de sugerencias y no es el comando, borrar
    if message.channel.id == ID_CANAL_SUGERENCIAS:
        if not message.content.startswith(".suggest"):
            try:
                await message.delete()
            except:
                pass
    
    await bot.process_commands(message)

@bot.event
async def on_voice_state_update(member, before, after):
    # 1. LÓGICA DE CREACIÓN
    if after.channel and after.channel.id == ID_CANAL_CREADOR:
        guild = member.guild
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(connect=True),
            member: discord.PermissionOverwrite(manage_channels=True, manage_permissions=True, move_members=True, mute_members=True)
        }
        nuevo_canal = await guild.create_voice_channel(
            name=f"🎙️ Sala de {member.name}", 
            category=after.channel.category, 
            overwrites=overwrites
        )
        await member.move_to(nuevo_canal)

    # 2. LÓGICA DE BORRADO
    if before.channel:
        canal_creador = bot.get_channel(ID_CANAL_CREADOR)
        if canal_creador and before.channel.category_id == canal_creador.category_id:
            if len(before.channel.members) == 0 and before.channel.id != ID_CANAL_CREADOR:
                try:
                    await before.channel.delete()
                except:
                    pass

@bot.event
async def on_ready():
    print(f'🤖 Cromi System online.')
    
    # 3. LIMPIEZA AUTOMÁTICA AL ARRANCAR
    canal_creador = bot.get_channel(ID_CANAL_CREADOR)
    if canal_creador and canal_creador.category:
        for canal in canal_creador.category.voice_channels:
            if len(canal.members) == 0 and canal.id != ID_CANAL_CREADOR:
                try:
                    await canal.delete(reason="Limpieza automática al reiniciar")
                    print(f"🧹 Canal huérfano '{canal.name}' eliminado.")
                except:
                    pass

async def main():
    # ✅ EL KEEP ALIVE ESTÁ AHORA AQUÍ. SE EJECUTA UNA SOLA VEZ AL ARRANCAR.
    keep_alive()
    async with bot:
        token = os.getenv('DISCORD_TOKEN')
        await bot.start(token)

if __name__ == '__main__':
    asyncio.run(main())
