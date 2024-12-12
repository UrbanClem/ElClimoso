import random
import asyncio
import discord
from discord.ext import commands, tasks
import threading

def Mojave():
    # Definir los eventos y sus pesos
    eventos = [
        {"nombre": "nada xd", "descripcion": "No hay eventos programados."},
        {"nombre": "Tormenta Electrica", "descripcion": "Una gran tormenta electrica te puede hacer la vida imposible. (-3 AG -2 PE daño electrico es triplicado)", "imagen": "https://media.discordapp.net/attachments/1023451309774487573/1261890086883033118/703da922be9694a209dd851c2c4eefe6.gif"},
        {"nombre": "Tormenta de Arena", "descripcion": "Preparate para vaciar tus calcetines, porque se te va a meter la arena hasta las nalgas. (-4 PE -3 AG)", "imagen": "https://media.discordapp.net/attachments/1023451309774487573/1261889466772099228/db69aed749f0c03e96290fb4f3498c2b.gif"},
        {"nombre": "Tormenta", "descripcion": "Una fuerte lluvia comienza a caer, dificultando el movimiento. (-2 AG -1 PE)", "imagen": "https://cdn.discordapp.com/attachments/1023451309774487573/1261898210562146344/main-qimg-8a5f94928a220a2bc6ffeb37d1580628-ezgif.com-webp-to-gif-converter.gif"},
        {"nombre": "Tormenta Radioactiva", "descripcion": "Esto es la peor de las tormentas que puedes encontrarte, y se recomienda que encuentres refugio lo antes posible si no quieres morir irradiado. (-2 PE -2 AG -2 RE 50\u2622\ufe0f por turno)||{mojave_role}||", "imagen": "https://media.discordapp.net/attachments/1023451309774487573/1261889466335756399/tumblr_nxp6ol3IYB1u8thp6o3_500.gif"},
    ]

    intents = discord.Intents.default()
    intents.message_content = True
    bot = commands.Bot(command_prefix='!', intents=intents)

    # ID del canal y variables globales
    CHANNEL_ID = CHANNEL_ID
    SERVER_ID = SERVER_ID
    evento_actual = None
    duracion_evento = 0

    @bot.event
    async def on_ready():
        print(f'Bot conectado como {bot.user}. Chat: {CHANNEL_ID}')
        enviar_eventos.start()

    @tasks.loop(seconds=1)
    async def enviar_eventos():
        nonlocal evento_actual, duracion_evento

        # Obtener el rol Mojave
        guild = bot.get_guild(SERVER_ID)  # Reemplazar con el ID del servidor
        if not guild:
            print(f"No se encontró el servidor con ID: {SERVER_ID}")
            return
        mojave_role = discord.utils.get(guild.roles, name="Mojave")

        if not mojave_role:
            print("No se encontró el rol Mojave.")
            return

        # Si hay un evento en curso
        if evento_actual and duracion_evento > 0:
            duracion_evento -= 1
            if duracion_evento == 0:
                channel = bot.get_channel(CHANNEL_ID)
                embed = discord.Embed(
                    title=f"La {evento_actual['nombre']} ha terminado!",
                    description=f"El evento duró {horas_evento // 3600} horas.",
                    color=discord.Color.green()
                )
                embed.set_image(url="https://media.discordapp.net/attachments/1023451309774487573/1261895046433603644/disco-elysium-rave.gif")
                if evento_actual["nombre"] != "nada xd":
                    await channel.send(embed=embed)

                # Reiniciar variables
                evento_actual = None
                await asyncio.sleep(random.randint(12 * 3600, 24 * 3600))

        # Generar nuevo evento si no hay uno en curso
        if not evento_actual:
            evento_actual = random.choices(eventos, weights=[75, 10, 7, 5, 3], k=1)[0]
            duracion_evento = random.randint(1 * 3600, 24 * 3600)
            horas_evento = duracion_evento

            # Si es "nada xd", omitir el mensaje
            if evento_actual["nombre"] == "nada xd":
                print(f'No paso nada xdxdxddd. Chat: {CHANNEL_ID}')
                return

            # Crear y enviar el mensaje del evento
            channel = bot.get_channel(CHANNEL_ID)
            embed = discord.Embed(
                title=evento_actual["nombre"],
                description=f"{evento_actual['descripcion']}\n\n{mojave_role.mention}",
                color=discord.Color.blue()
            )
            print(f'{evento_actual}. Chat: {CHANNEL_ID}')
            if "imagen" in evento_actual:
                embed.set_image(url=evento_actual["imagen"])
            await channel.send(embed=embed)

    bot.run('TOKEN')

def Washington():
    # Definir los eventos y sus pesos
    eventos = [
        {"nombre": "nada xd", "descripcion": "No hay eventos programados."},
        {"nombre": "Neblina", "descripcion": "Una densa niebla se pone, dificultando la visión. (-3 PE)", "imagen": "https://media.discordapp.net/attachments/1023451309774487573/1261889467120357386/giphy.gif?ex=669499a5&is=66934825&hm=66c3a23795fb9cb0a1103a2d7cde457e67c0992449b25413b798965487f71167&="},
        {"nombre": "Tormenta Electrica", "descripcion": "Una gran tormenta electrica te puede hacer la vida imposible. (-3 AG -2 PE daño electrico es triplicado)", "imagen": "https://media.discordapp.net/attachments/1023451309774487573/1261890086883033118/703da922be9694a209dd851c2c4eefe6.gif?ex=66949a39&is=669348b9&hm=3b09708839cc645c51f785f1582e669a8e417df0e722cd4bcffb91893d32f22b&=&width=450&height=676"},
        {"nombre": "Tormenta", "descripcion": "Una fuerte lluvia comienza a caer, dificultando el movimiento. (-2 AG -1 PE)", "imagen": "https://cdn.discordapp.com/attachments/1023451309774487573/1261898210562146344/main-qimg-8a5f94928a220a2bc6ffeb37d1580628-ezgif.com-webp-to-gif-converter.gif?ex=6694a1ca&is=6693504a&hm=3a5fd1aed45f77a6db94b77180ecb3f346a30991fa0cf23989953a4d66ddf800&"},
        {"nombre": "Tormenta Radioactiva", "descripcion": "Esto es la peor de las tormentas que puedes encontrarte, y se recomienda que encuentres refugio lo antes posible si no quieres morir irradiado. (-2 PE -2 AG -2 RE 50☢️ por turno). ||{washington_role.mention}||", "imagen": "https://media.discordapp.net/attachments/1023451309774487573/1261889466335756399/tumblr_nxp6ol3IYB1u8thp6o3_500.gif?ex=669499a5&is=66934825&hm=2acc882a69f3329fba5bf8b7d6d739f139dc0e401e7c3e136a0c5a41911d9deb&="},
    ]

    intents = discord.Intents.default()
    intents.message_content = True
    bot = commands.Bot(command_prefix='!', intents=intents)

    # ID del canal y variables globales
    CHANNEL_ID = CHANNEL_ID
    SERVER_ID = SERVER_ID
    evento_actual = None
    duracion_evento = 0

    @bot.event
    async def on_ready():
        print(f'Bot conectado como {bot.user}. Chat: {CHANNEL_ID}')
        enviar_eventos.start()

    @tasks.loop(seconds=1)
    async def enviar_eventos():
        nonlocal evento_actual, duracion_evento

        # Obtener el rol Mojave
        guild = bot.get_guild(SERVER_ID)  # Reemplazar con el ID del servidor
        washington_role = discord.utils.get(guild.roles, name="Yermo Capital")

        if not washington_role:
            print("No se encontró el rol Mojave.")
            return

        # Si hay un evento en curso
        if evento_actual and duracion_evento > 0:
            duracion_evento -= 1
            if duracion_evento == 0:
                channel = bot.get_channel(CHANNEL_ID)
                embed = discord.Embed(
                    title=f"La {evento_actual['nombre']} ha terminado!",
                    description=f"El evento duró {horas_evento // 3600} horas.",
                    color=discord.Color.green()
                )
                embed.set_image(url="https://media.discordapp.net/attachments/1023451309774487573/1261895046433603644/disco-elysium-rave.gif")
                if evento_actual["nombre"] != "nada xd":
                    await channel.send(embed=embed)

                # Reiniciar variables
                evento_actual = None
                await asyncio.sleep(random.randint(12 * 3600, 24 * 3600))

        # Generar nuevo evento si no hay uno en curso
        if not evento_actual:
            evento_actual = random.choices(eventos, weights=[75, 10, 7, 5, 3], k=1)[0]
            duracion_evento = random.randint(1 * 3600, 24 * 3600)
            horas_evento = duracion_evento

            # Si es "nada xd", omitir el mensaje
            if evento_actual["nombre"] == "nada xd":
                print(f'No paso nada xdxdxddd. Chat: {CHANNEL_ID}')
                return

            # Crear y enviar el mensaje del evento
            channel = bot.get_channel(CHANNEL_ID)
            embed = discord.Embed(
                title=evento_actual["nombre"],
                description=f"{evento_actual['descripcion']}\n\n{washington_role.mention}",
                color=discord.Color.blue()
            )
            print(f'{evento_actual}. Chat: {CHANNEL_ID}')
            if "imagen" in evento_actual:
                embed.set_image(url=evento_actual["imagen"])
            await channel.send(embed=embed)

    # Ejecutar el bot
    bot.run('TOKEN')

def Boston():
    # Definir los eventos y sus pesos
    eventos = [
        {"nombre": "nada xd", "descripcion": "No hay eventos programados."},
        {"nombre": "Neblina", "descripcion": "Una densa niebla se pone, dificultando la visión. (-3 PE)", "imagen": "https://media.discordapp.net/attachments/1023451309774487573/1261889467120357386/giphy.gif?ex=669499a5&is=66934825&hm=66c3a23795fb9cb0a1103a2d7cde457e67c0992449b25413b798965487f71167&="},
        {"nombre": "Tormenta Electrica", "descripcion": "Una gran tormenta electrica te puede hacer la vida imposible. (-3 AG -2 PE daño electrico es triplicado)", "imagen": "https://media.discordapp.net/attachments/1023451309774487573/1261890086883033118/703da922be9694a209dd851c2c4eefe6.gif?ex=66949a39&is=669348b9&hm=3b09708839cc645c51f785f1582e669a8e417df0e722cd4bcffb91893d32f22b&=&width=450&height=676"},
        {"nombre": "Tormenta", "descripcion": "Una fuerte lluvia comienza a caer, dificultando el movimiento. (-2 AG -1 PE)", "imagen": "https://cdn.discordapp.com/attachments/1023451309774487573/1261898210562146344/main-qimg-8a5f94928a220a2bc6ffeb37d1580628-ezgif.com-webp-to-gif-converter.gif?ex=6694a1ca&is=6693504a&hm=3a5fd1aed45f77a6db94b77180ecb3f346a30991fa0cf23989953a4d66ddf800&"},
        {"nombre": "Tormenta Radioactiva", "descripcion": "Esto es la peor de las tormentas que puedes encontrarte, y se recomienda que encuentres refugio lo antes posible si no quieres morir irradiado. (-2 PE -2 AG -2 RE 50☢️ por turno)", "imagen": "https://media.discordapp.net/attachments/1023451309774487573/1261889466335756399/tumblr_nxp6ol3IYB1u8thp6o3_500.gif?ex=669499a5&is=66934825&hm=2acc882a69f3329fba5bf8b7d6d739f139dc0e401e7c3e136a0c5a41911d9deb&="},
    ]


    intents = discord.Intents.default()
    intents.message_content = True
    bot = commands.Bot(command_prefix='!', intents=intents)

    # ID del canal y variables globales
    CHANNEL_ID = CHANNEL_ID
    SERVER_ID = SERVER_ID
    evento_actual = None
    duracion_evento = 0

    @bot.event
    async def on_ready():
        print(f'Bot conectado como {bot.user}. Chat: {CHANNEL_ID}')
        enviar_eventos.start()

    @tasks.loop(seconds=1)
    async def enviar_eventos():
        nonlocal evento_actual, duracion_evento

        # Obtener el rol Mojave
        guild = bot.get_guild(SERVER_ID)  # Reemplazar con el ID del servidor
        boston_role = discord.utils.get(guild.roles, name="Commonwealth")

        if not boston_role:
            print("No se encontró el rol Boston.")
            return

        # Si hay un evento en curso
        if evento_actual and duracion_evento > 0:
            duracion_evento -= 1
            if duracion_evento == 0:
                embed = discord.Embed(
                    title=f"La {evento_actual['nombre']} ha terminado!",
                    description=f"El evento duró {horas_evento // 3600} horas.",
                    color=discord.Color.green()
                )
                embed.set_image(url="https://media.discordapp.net/attachments/1023451309774487573/1261895046433603644/disco-elysium-rave.gif")
                if evento_actual["nombre"] != "nada xd":
                    await channel.send(embed=embed)

                # Reiniciar variables
                evento_actual = None
                await asyncio.sleep(random.randint(12 * 3600, 24 * 3600))

        # Generar nuevo evento si no hay uno en curso
        if not evento_actual:
            evento_actual = random.choices(eventos, weights=[75, 10, 7, 5, 3], k=1)[0]
            duracion_evento = random.randint(1 * 3600, 24 * 3600)
            horas_evento = duracion_evento

            # Si es "nada xd", omitir el mensaje
            if evento_actual["nombre"] == "nada xd":
                print(f'No paso nada xdxdxddd. Chat: {CHANNEL_ID}')
                return

            # Crear y enviar el mensaje del evento
            channel = bot.get_channel(CHANNEL_ID)
            embed = discord.Embed(
                title=evento_actual["nombre"],
                description=f"{evento_actual['descripcion']}\n\n{boston_role.mention}",
                color=discord.Color.blue()
            )
            print(f'{evento_actual}. Chat: {CHANNEL_ID}')
            if "imagen" in evento_actual:
                embed.set_image(url=evento_actual["imagen"])
            await channel.send(embed=embed)

    # Ejecutar el bot
    bot.run('TOKEN')

# Define las funciones Mojave y Washington como funciones normales, no invocándolas directamente
def run_mojave():
    Mojave()

def run_washington():
    Washington()

def run_boston():
    Boston()

# Crear hilos para ejecutar las funciones simultáneamente
thread_mojave = threading.Thread(target=run_mojave)
thread_washington = threading.Thread(target=run_washington)
thread_boston = threading.Thread(target=run_boston)

# Iniciar ambos hilos
thread_mojave.start()
thread_washington.start()
thread_boston.start()

# Esperar a que ambos hilos terminen (esto no bloquea otros procesos en el hilo principal)
thread_mojave.join()
thread_washington.join()
thread_boston.join()