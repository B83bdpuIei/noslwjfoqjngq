import discord
from discord.ext import commands

class Rules(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # ID del canal de normas configurado
        self.ID_CANAL_NORMAS = 1501370304067539066 

    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.wait_until_ready()
        
        canal = self.bot.get_channel(self.ID_CANAL_NORMAS)
        if not canal:
            print(f"❌ Rules: No he podido encontrar el canal {self.ID_CANAL_NORMAS}")
            return

        # Comprobamos si las reglas ya están puestas para no repetirlas cada vez que reinicies
        ya_existen = False
        async for msg in canal.history(limit=5):
            if msg.author == self.bot.user and msg.embeds:
                if "REGLAS" in msg.embeds[0].description:
                    ya_existen = True
                    break

        if not ya_existen:
            texto_reglas = (
                "# REGLAS\n\n"
                "> **1️⃣ Sé respetuoso y usa el sentido común**\n"
                "> Trata a los demás con respeto. No hagas doxxing, no acoses ni uses lenguaje ofensivo como insulto o spam. Si algo no está explícitamente en las reglas pero sabes que está mal, no lo hagas.\n"
                "> \n"
                "> **2️⃣ No hagas spam**\n"
                "> Se considera spam enviar más de 3 mensajes consecutivos solo con emojis, GIFs, repetir el mismo mensaje varias veces, abusar de mensajes en mayúsculas, enviar mensajes sin sentido o saturar los canales.\n"
                "> \n"
                "> **3️⃣ No contenido NSFW**\n"
                "> No se permite contenido explícito o inapropiado, cualquier tipo de mensaje del estilo será automáticamente baneo.\n"
                "> \n"
                "> **4️⃣ Evita temas controvertidos**\n"
                "> No se permiten discusiones sobre política, religión, humor negro u otros temas polémicos. Si sabes que puede crear polémica pregunta o ahórratelo para ti mismo.\n"
                "> ⚠️ El humor negro será permitido en el canal <#1501646588362100927> siempre y cuando no sea una indirecta hacia nadie.\n"
                "> \n"
                "> **5️⃣ No invites a Discords ajenos**\n"
                "> Está prohibido compartir enlaces de invitación de Discords ajenos a este servidor.\n"
                "> \n"
                "> **6️⃣ Da crédito cuando corresponda**\n"
                "> Si compartes algo que no es tuyo, menciona al autor original y etiqueta claramente el contenido generado por IA.\n"
                "> \n"
                "> **7️⃣ Usa los canales adecuados**\n"
                "> Mantén las conversaciones en los canales correspondientes para mantener la limpieza del servidor.\n"
                "> \n"
                "> **8️⃣ Denuncia a los infractores**\n"
                "> Si ves a alguien incumpliendo las normas, por favor, repórtalo a los Admins <@787372239979806741> <@819569749222096897>.\n\n"
                "Si estás dentro del servidor aceptas seguir estas reglas y entiendes que cualquier infracción puede resultar en un strike o ban.\n\n"
                "Respeta a los demás, sé amable, recuerda que se viene a conocer gente y no a buscar conflicto. Cualquier duda, no dudéis en preguntarme <@787372239979806741> y lo más importante: ¡Pasadlo bien!\n\n"
                "**El incumplimiento de estas normas puede resultar en silencios temporales o permanentes, e incluso en la expulsión del servidor.**"
            )

            embed = discord.Embed(
                description=texto_reglas,
                color=0xff69b4 # Color Rosita
            )
            embed.set_footer(text="Cromi System • Normas")
            
            await canal.send(embed=embed)
            print("✅ Reglas enviadas correctamente.")

async def setup(bot):
    await bot.add_cog(Rules(bot))
