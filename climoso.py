import random
import asyncio
from datetime import datetime
import pytz
import discord
import time
from discord.ext import commands, tasks
import threading

def Mojave():
    # Definir los eventos y sus pesos
    eventos = [
        {"nombre": "nada xd", "descripcion": "No hay eventos programados."},
        {"nombre": "Tormenta Electrica", "descripcion": "Una gran tormenta electrica te puede hacer la vida imposible. (-3 AG -2 PE daño electrico es triplicado)", "imagen": "https://media.discordapp.net/attachments/1023451309774487573/1261890086883033118/703da922be9694a209dd851c2c4eefe6.gif?ex=66949a39&is=669348b9&hm=3b09708839cc645c51f785f1582e669a8e417df0e722cd4bcffb91893d32f22b&=&width=450&height=676"},
        {"nombre": "Tormenta de Arena", "descripcion": "Preparate para vaciar tus calcetines, porque se te va a meter la arena hasta las nalgas. (-4 PE -3 AG)", "imagen": "https://media.discordapp.net/attachments/1023451309774487573/1261889466772099228/db69aed749f0c03e96290fb4f3498c2b.gif?ex=669499a5&is=66934825&hm=e71fab7b5253e9fafda72fa6baf64ce3837a591179fbb9e8e39e5d04cb517474&="},
        {"nombre": "Tormenta", "descripcion": "Una fuerte lluvia comienza a caer, dificultando el movimiento. (-2 AG -1 PE)", "imagen": "https://cdn.discordapp.com/attachments/1023451309774487573/1261898210562146344/main-qimg-8a5f94928a220a2bc6ffeb37d1580628-ezgif.com-webp-to-gif-converter.gif?ex=6694a1ca&is=6693504a&hm=3a5fd1aed45f77a6db94b77180ecb3f346a30991fa0cf23989953a4d66ddf800&"},
        {"nombre": "Tormenta Radioactiva", "descripcion": "Esto es la peor de las tormentas que puedes encontrarte, y se recomienda que encuentres refugio lo antes posible si no quieres morir irradiado. (-2 PE -2 AG -2 RE 50☢️ por turno)||{mojave_role}||", "imagen": "https://media.discordapp.net/attachments/1023451309774487573/1261889466335756399/tumblr_nxp6ol3IYB1u8thp6o3_500.gif?ex=669499a5&is=66934825&hm=2acc882a69f3329fba5bf8b7d6d739f139dc0e401e7c3e136a0c5a41911d9deb&="},
        {"nombre": "Noche", "descripcion": "Es la hora de la oscuridad. (-2 PE)", "imagen": "https://i.gifer.com/origin/4b/4b6a384cc5b1fa37f3cd566316b30400_w200.gif"},
        {"nombre": "Luna Llena", "descripcion": "La noche es clara gracias a la luna. (-1 PE)", "imagen": "https://media.discordapp.net/attachments/1023451309774487573/1261890087319375914/download.gif?ex=66949a39&is=669348b9&hm=e74c08668cea3fea446d965bd9a9ff5b97dd9a09d1ceb824a98b31235ca7f26d&=&width=591&height=676"},
        {"nombre": "Luna Nueva", "descripcion": "La noche es oscura, no puede verse con claridad. (-3 PE)", "imagen": "https://media.discordapp.net/attachments/1023451309774487573/1261890087747059742/moon_phase_large.webp?ex=66949a39&is=669348b9&hm=77af57526a8304363cf054ab944bcf6e61a9f92b98afe7e226d18b70d193619b&=&format=webp"},
        {"nombre": "Amanecer", "descripcion": "El sol comienza a aparecer en el horizonte. ", "imagen": "https://media.discordapp.net/attachments/1023451309774487573/1261890451116654663/-Brkls.gif?ex=66949a90&is=66934910&hm=780efe14985b9bb3aef0b75d83fff78e05bbf417117400bfa2a5a462f45a270d&="}
    ]

    # Definir los pesos para cada evento
    pesos = [4, 2, 1, 2, 1, 0, 0, 0, 0]  # Peso 0 para eventos que deben ser aleatorios (Noche, Luna Llena, Luna Nueva, Amanecer)

    # Zona horaria GMT-8
    gmt_minus_8 = pytz.timezone('Etc/GMT+8')

    # Variable global para controlar la aparición de eventos nocturnos
    global noche_aparecida_hoy_mojave
    noche_aparecida_hoy_mojave = False

    # Variable global para controlar el amanecer
    global dia_aparecido_hoy_mojave
    dia_aparecido_hoy_mojave = False

    def es_hora_8pm_gmt_minus_8():
        """Verifica si la hora actual en GMT-8 es 8:00 PM."""
        ahora = datetime.now(gmt_minus_8)
        return ahora.hour == 20 and ahora.minute == 0

    def es_hora_6am_gmt_minus_8():
        """Verifica si la hora actual en GMT-8 es 6:00 AM."""
        ahora = datetime.now(gmt_minus_8)
        return ahora.hour == 6 and ahora.minute == 0
    
    def es_hora_medianoche_gmt_minus_8():
        """Verifica si la hora actual en GMT-8 es medianoche."""
        ahora = datetime.now(gmt_minus_8)
        return ahora.hour == 0 and ahora.minute == 0

    # Configurar el bot con Intents
    intents = discord.Intents.default()
    intents.message_content = True
    bot = commands.Bot(command_prefix='!', intents=intents)

    # Define el ID del canal de Discord donde se enviarán los mensajes
    CHANNEL_ID = ID

    # Variables globales para control de eventos
    global evento_actual_mojave
    evento_actual_mojave = None
    global tiempo_evento_actual_mojave
    tiempo_evento_actual_mojave = 0
    global espera_evento_nuevo_mojave
    espera_evento_nuevo_mojave = False
    global duracion_evento_mojave 
    duracion_evento_mojave = 0
    global mojave_role

    @bot.event
    async def on_ready():
        global mojave_role
        print(f'Bot conectado como {bot.user}')
        enviar_eventos.start()

        # Obtener el objeto del servidor
        guild = discord.utils.get(bot.guilds, id=ID)  

        # Obtener el rol @Mojave
        mojave_role = discord.utils.get(guild.roles, name="Mojave")

    @tasks.loop(seconds=1)
    async def enviar_eventos():
        global evento_actual_mojave, tiempo_evento_actual_mojave, espera_evento_nuevo_mojave, noche_aparecida_hoy_mojave, dia_aparecido_hoy_mojave, duracion_evento_mojave, horas_transcurridas
        
        horas_transcurridas = 0

        max_horas = 13

        inicio = time.time()

        while horas_transcurridas < max_horas:
            time.sleep(3600)  # Espera una hora
            horas_transcurridas = (time.time() - inicio) / 3600

        if es_hora_medianoche_gmt_minus_8():
            noche_aparecida_hoy_mojave = False
            dia_aparecido_hoy_mojave = False

        if es_hora_8pm_gmt_minus_8():
            if not noche_aparecida_hoy_mojave:
                evento_noche = random.choice([evento for evento in eventos if evento["nombre"] in ["Noche", "Luna Llena", "Luna Nueva"]])
                channel = bot.get_channel(CHANNEL_ID)
                embed = discord.Embed(title=evento_noche["nombre"], 
                                    description=evento_noche["descripcion"], 
                                    color=discord.Color.blue())
                if "imagen" in evento_noche:
                    embed.set_image(url=evento_noche["imagen"])
                await channel.send(embed=embed)
                await channel.send(mojave_role.mention)  # Arrobar al rol @Mojave
                
                noche_aparecida_hoy_mojave = True  # Marcar que se ha enviado un evento nocturno hoy
        
        if es_hora_6am_gmt_minus_8():
            if not dia_aparecido_hoy_mojave:
                evento_dia = random.choice([evento for evento in eventos if evento["nombre"] in ["Amanecer"]])
                channel = bot.get_channel(CHANNEL_ID)
                embed = discord.Embed(title=evento_dia["nombre"], 
                                    description=evento_dia["descripcion"], 
                                    color=discord.Color.blue())
                if "imagen" in evento_dia:
                    embed.set_image(url=evento_dia["imagen"])
                await channel.send(embed=embed)
                await channel.send(mojave_role.mention)  # Arrobar al rol @Mojave
                
                dia_aparecido_hoy_mojave = True  # Marcar que ha amanecido hoy

        elif tiempo_evento_actual_mojave > 0:
            tiempo_evento_actual_mojave -= 1
            if tiempo_evento_actual_mojave == 0:
                if evento_actual_mojave and evento_actual_mojave["nombre"] != "nada xd":
                    channel = bot.get_channel(CHANNEL_ID)
                    duracion_evento_horas = duracion_evento // 3600
                    embed = discord.Embed(title=f"La {evento_actual_mojave['nombre']} ha terminado!",    
                                        description=f"El evento duró {duracion_evento_horas} horas.", # Arrobar al rol @Mojave
                                        color=discord.Color.green()) 
                    embed.set_image(url="https://media.discordapp.net/attachments/1023451309774487573/1261895046433603644/disco-elysium-rave.gif?ex=66949ed7&is=66934d57&hm=9392bc5221adb518e5f2916e844b1dd0732803bedc22d79e7ad09d48f5c27cda&=")
                    await channel.send(embed=embed)
                    await channel.send(mojave_role.mention)  # Arrobar al rol @Mojave

                    # Esperar entre 12 y 24 segundos antes de iniciar el próximo evento
                    intervalo_aleatorio = random.randint(12 * 3600, 24 * 3600)
                    await asyncio.sleep(intervalo_aleatorio)
                    espera_evento_nuevo_mojave = False  # Deshabilitar la espera de nuevo evento

                    # Reiniciar variables para permitir el inicio de un nuevo evento
                    evento_actual_mojave = None
                    tiempo_evento_actual_mojave = 0
                    duracion_evento_mojave = 0

        elif not espera_evento_nuevo_mojave and horas_transcurridas <= 12:
            # Generar un evento basado en los pesos (excluyendo eventos especiales)
            evento_aleatorio_mojave = random.choices(eventos[1:], weights=pesos[1:], k=1)[0]
            evento_actual_mojave = evento_aleatorio_mojave

            # Si el evento es "nada xd", no enviar ningún mensaje
            if evento_aleatorio_mojave["nombre"] == "nada xd":
                return

            # Crear un Embed para el evento
            embed = discord.Embed(title=evento_actual_mojave["nombre"], 
                                description=evento_actual_mojave["descripcion"], 
                                color=discord.Color.blue())        	    

            # Agregar la imagen al Embed si está disponible
            if "imagen" in evento_actual_mojave:
                embed.set_image(url=evento_actual_mojave["imagen"])

            # Enviar el Embed al canal de Discord
            channel = bot.get_channel(CHANNEL_ID)
            await channel.send(embed=embed)
            await channel.send(mojave_role.mention)  # Arrobar al rol @Mojave

            # Generar un intervalo de tiempo aleatorio entre 1 y 24 segundos para la duración del evento
            intervalo_evento = random.randint(1 * 3600, 24 * 3600)
            tiempo_evento_actual_mojave = intervalo_evento
            duracion_evento_mojave = intervalo_evento / 3600

            # Imprimir la hora actual en GMT-8 en consola
            ahora_gmt_minus_8 = datetime.now(gmt_minus_8)
            print(f'Hora actual en GMT-8: {ahora_gmt_minus_8.strftime("%Y-%m-%d %H:%M:%S")}')

        # Esperar un segundo antes de verificar nuevamente
        await asyncio.sleep(1)

    # Ejecutar el bot
    bot.run('TOKEN')

def Washington():
    # Definir los eventos y sus pesos
    eventos = [
        {"nombre": "nada xd", "descripcion": "No hay eventos programados."},
        {"nombre": "Neblina", "descripcion": "Una densa niebla se pone, dificultando la visión. (-3 PE)", "imagen": "https://media.discordapp.net/attachments/1023451309774487573/1261889467120357386/giphy.gif?ex=669499a5&is=66934825&hm=66c3a23795fb9cb0a1103a2d7cde457e67c0992449b25413b798965487f71167&="},
        {"nombre": "Tormenta Electrica", "descripcion": "Una gran tormenta electrica te puede hacer la vida imposible. (-3 AG -2 PE daño electrico es triplicado)", "imagen": "https://media.discordapp.net/attachments/1023451309774487573/1261890086883033118/703da922be9694a209dd851c2c4eefe6.gif?ex=66949a39&is=669348b9&hm=3b09708839cc645c51f785f1582e669a8e417df0e722cd4bcffb91893d32f22b&=&width=450&height=676"},
        {"nombre": "Tormenta", "descripcion": "Una fuerte lluvia comienza a caer, dificultando el movimiento. (-2 AG -1 PE)", "imagen": "https://cdn.discordapp.com/attachments/1023451309774487573/1261898210562146344/main-qimg-8a5f94928a220a2bc6ffeb37d1580628-ezgif.com-webp-to-gif-converter.gif?ex=6694a1ca&is=6693504a&hm=3a5fd1aed45f77a6db94b77180ecb3f346a30991fa0cf23989953a4d66ddf800&"},
        {"nombre": "Tormenta Radioactiva", "descripcion": "Esto es la peor de las tormentas que puedes encontrarte, y se recomienda que encuentres refugio lo antes posible si no quieres morir irradiado. (-2 PE -2 AG -2 RE 50☢️ por turno). ||{washington_role.mention}||", "imagen": "https://media.discordapp.net/attachments/1023451309774487573/1261889466335756399/tumblr_nxp6ol3IYB1u8thp6o3_500.gif?ex=669499a5&is=66934825&hm=2acc882a69f3329fba5bf8b7d6d739f139dc0e401e7c3e136a0c5a41911d9deb&="},
        {"nombre": "Noche", "descripcion": "Es la hora de la oscuridad. (-2 PE)", "imagen": "https://i.gifer.com/origin/4b/4b6a384cc5b1fa37f3cd566316b30400_w200.gif"},
        {"nombre": "Luna Llena", "descripcion": "La noche es clara gracias a la luna. (-1 PE)", "imagen": "https://media.discordapp.net/attachments/1023451309774487573/1261890087319375914/download.gif?ex=66949a39&is=669348b9&hm=e74c08668cea3fea446d965bd9a9ff5b97dd9a09d1ceb824a98b31235ca7f26d&=&width=591&height=676"},
        {"nombre": "Luna Nueva", "descripcion": "La noche es oscura, no puede verse con claridad. (-3 PE)", "imagen": "https://media.discordapp.net/attachments/1023451309774487573/1261890087747059742/moon_phase_large.webp?ex=66949a39&is=669348b9&hm=77af57526a8304363cf054ab944bcf6e61a9f92b98afe7e226d18b70d193619b&=&format=webp"},
        {"nombre": "Amanecer", "descripcion": "El sol comienza a aparecer en el horizonte. ", "imagen": "https://media.discordapp.net/attachments/1023451309774487573/1261890451116654663/-Brkls.gif?ex=66949a90&is=66934910&hm=780efe14985b9bb3aef0b75d83fff78e05bbf417117400bfa2a5a462f45a270d&="}
    ]

    # Definir los pesos para cada evento
    pesos = [4, 2, 2, 3, 1, 0, 0, 0, 0]  # Peso 0 para eventos que deben ser aleatorios (Noche, Luna Llena, Luna Nueva, Amanecer)

    # Zona horaria GMT-8
    gmt_minus_5 = pytz.timezone('Etc/GMT+5')

    # Variable global para controlar la aparición de eventos nocturnos
    global noche_aparecida_hoy_washington
    noche_aparecida_hoy_washington = False

    # Variable global para controlar el amanecer
    global dia_aparecido_hoy_washington
    dia_aparecido_hoy_washington = False

    def contar_horas(max_horas=13):
        global inicio, horas_transcurridas
        horas_transcurridas = 0

        while horas_transcurridas < max_horas:
            time.sleep(3600)  # Espera una hora
            horas_transcurridas = (time.time() - inicio) / 3600

    def es_hora_8pm_gmt_minus_5():
        """Verifica si la hora actual en GMT-5 es 8:00 PM."""
        ahora = datetime.now(gmt_minus_5)
        return ahora.hour == 20 and ahora.minute == 0

    def es_hora_6am_gmt_minus_5():
        """Verifica si la hora actual en GMT-5 es 6:00 AM."""
        ahora = datetime.now(gmt_minus_5)
        return ahora.hour == 6 and ahora.minute == 0
    
    def es_hora_medianoche_gmt_minus_5():
        """Verifica si la hora actual en GMT-5 es medianoche."""
        ahora = datetime.now(gmt_minus_5)
        return ahora.hour == 0 and ahora.minute == 0

    # Configurar el bot con Intents
    intents = discord.Intents.default()
    intents.message_content = True
    bot = commands.Bot(command_prefix='!', intents=intents)

    # Define el ID del canal de Discord donde se enviarán los mensajes
    CHANNEL_ID = ID

    # Variables globales para control de eventos
    global evento_actual_washington
    evento_actual_washington = None
    global tiempo_evento_actual_washington
    tiempo_evento_actual_washington = 0
    global espera_evento_nuevo_washington
    espera_evento_nuevo_washington = False
    global duracion_evento_washington
    duracion_evento_washington = 0
    global washington_role

    @bot.event
    async def on_ready():
        global washington_role
        print(f'Bot conectado como {bot.user}')
        enviar_eventos.start()

        # Obtener el objeto del servidor
        guild = discord.utils.get(bot.guilds, id=ID)  

        # Obtener el rol @Washington
        washington_role = discord.utils.get(guild.roles, name="Yermo Capital")

    @tasks.loop(seconds=1)
    async def enviar_eventos():
        global evento_actual_washington, tiempo_evento_actual_washington, espera_evento_nuevo_washington, noche_aparecida_hoy_washington, dia_aparecido_hoy_washington, duracion_evento_washington, horas_transcurridas
        
        horas_transcurridas = 0

        max_horas = 13

        inicio = time.time()

        while horas_transcurridas < max_horas:
            time.sleep(3600)  # Espera una hora
            horas_transcurridas = (time.time() - inicio) / 3600

        if es_hora_medianoche_gmt_minus_5():
            noche_aparecida_hoy_washington = False
            dia_aparecido_hoy_washington = False
        
        if es_hora_8pm_gmt_minus_5():
            if not noche_aparecida_hoy_washington:
                evento_noche_washington = random.choice([evento for evento in eventos if evento["nombre"] in ["Noche", "Luna Llena", "Luna Nueva"]])
                channel = bot.get_channel(CHANNEL_ID)
                embed = discord.Embed(title=evento_noche_washington["nombre"], 
                                    description=evento_noche_washington["descripcion"], 
                                    color=discord.Color.blue())
                if "imagen" in evento_noche_washington:
                    embed.set_image(url=evento_noche_washington["imagen"])
                await channel.send(embed=embed)
                await channel.send(washington_role.mention)  # Arrobar al rol @Washington
                
                noche_aparecida_hoy_washington = True  # Marcar que se ha enviado un evento nocturno hoy
        
        if es_hora_6am_gmt_minus_5():
            if not dia_aparecido_hoy_washington:
                evento_dia_washington = random.choice([evento for evento in eventos if evento["nombre"] in ["Amanecer"]])
                channel = bot.get_channel(CHANNEL_ID)
                embed = discord.Embed(title=evento_dia_washington["nombre"], 
                                    description=evento_dia_washington["descripcion"], 
                                    color=discord.Color.blue())
                if "imagen" in evento_dia_washington:
                    embed.set_image(url=evento_dia_washington["imagen"])
                await channel.send(embed=embed)
                await channel.send(washington_role.mention)  # Arrobar al rol @Washington
                
                dia_aparecido_hoy_washington = True  # Marcar que ha amanecido hoy

        elif tiempo_evento_actual_washington > 0:
            tiempo_evento_actual_washington -= 1
            if tiempo_evento_actual_washington == 0:
                if evento_actual_washington and evento_actual_washington["nombre"] != "nada xd":
                    channel = bot.get_channel(CHANNEL_ID)
                    duracion_evento_horas = duracion_evento // 3600
                    embed = discord.Embed(title=f"La {evento_actual_washington['nombre']} ha terminado!",    
                                        description=f"El evento duró {duracion_evento_horas} horas.", 
                                        color=discord.Color.green()) 
                    embed.set_image(url="https://media.discordapp.net/attachments/1023451309774487573/1261895046433603644/disco-elysium-rave.gif?ex=66949ed7&is=66934d57&hm=9392bc5221adb518e5f2916e844b1dd0732803bedc22d79e7ad09d48f5c27cda&=")
                    await channel.send(embed=embed)
                    await channel.send(washington_role.mention)  # Arrobar al rol @Washington

                    # Esperar entre 12 y 24 segundos antes de iniciar el próximo evento
                    intervalo_aleatorio = random.randint(12 * 3600, 24 * 3600)
                    await asyncio.sleep(intervalo_aleatorio)
                    espera_evento_nuevo_washington = False  # Deshabilitar la espera de nuevo evento

                    # Reiniciar variables para permitir el inicio de un nuevo evento
                    evento_actual_washington = None
                    tiempo_evento_actual_washington = 0
                    duracion_evento_washington = 0

        elif not espera_evento_nuevo_washington and horas_transcurridas >= 12:
            # Generar un evento basado en los pesos (excluyendo eventos especiales)
            evento_aleatorio_washington = random.choices(eventos[1:], weights=pesos[1:], k=1)[0]
            evento_actual_washington = evento_aleatorio_washington

            # Si el evento es "nada xd", no enviar ningún mensaje
            if evento_aleatorio_washington["nombre"] == "nada xd":
                return

            # Crear un Embed para el evento
            embed = discord.Embed(title=evento_actual_washington["nombre"], 
                                description=evento_actual_washington["descripcion"], 
                                color=discord.Color.blue())

            # Agregar la imagen al Embed si está disponible
            if "imagen" in evento_actual_washington:
                embed.set_image(url=evento_actual_washington["imagen"])

            # Enviar el Embed al canal de Discord
            channel = bot.get_channel(CHANNEL_ID)
            await channel.send(embed=embed)
            await channel.send(washington_role.mention)  # Arrobar al rol @Washington

            # Generar un intervalo de tiempo aleatorio entre 1 y 24 segundos para la duración del evento
            intervalo_evento = random.randint(1 * 3600, 24 * 3600)
            tiempo_evento_actual_washington = intervalo_evento
            duracion_evento_washington = intervalo_evento  # Actualizar la duración del evento

            # Imprimir la hora actual en GMT-8 en consola
            ahora_gmt_minus_5 = datetime.now(gmt_minus_5)
            print(f'Hora actual en GMT-5: {ahora_gmt_minus_5.strftime("%Y-%m-%d %H:%M:%S")}')

        # Esperar un segundo antes de verificar nuevamente
        await asyncio.sleep(1)

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
        {"nombre": "Noche", "descripcion": "Es la hora de la oscuridad. (-2 PE)", "imagen": "https://i.gifer.com/origin/4b/4b6a384cc5b1fa37f3cd566316b30400_w200.gif"},
        {"nombre": "Luna Llena", "descripcion": "La noche es clara gracias a la luna. (-1 PE)", "imagen": "https://media.discordapp.net/attachments/1023451309774487573/1261890087319375914/download.gif?ex=66949a39&is=669348b9&hm=e74c08668cea3fea446d965bd9a9ff5b97dd9a09d1ceb824a98b31235ca7f26d&=&width=591&height=676"},
        {"nombre": "Luna Nueva", "descripcion": "La noche es oscura, no puede verse con claridad. (-3 PE)", "imagen": "https://media.discordapp.net/attachments/1023451309774487573/1261890087747059742/moon_phase_large.webp?ex=66949a39&is=669348b9&hm=77af57526a8304363cf054ab944bcf6e61a9f92b98afe7e226d18b70d193619b&=&format=webp"},
        {"nombre": "Amanecer", "descripcion": "El sol comienza a aparecer en el horizonte.", "imagen": "https://media.discordapp.net/attachments/1023451309774487573/1261890451116654663/-Brkls.gif?ex=66949a90&is=66934910&hm=780efe14985b9bb3aef0b75d83fff78e05bbf417117400bfa2a5a462f45a270d&="}
    ]

    # Definir los pesos para cada evento
    pesos = [4, 2, 2, 3, 1, 0, 0, 0, 0]  # Peso 0 para eventos que deben ser aleatorios (Noche, Luna Llena, Luna Nueva, Amanecer)

    # Zona horaria GMT-8
    gmt_minus_5 = pytz.timezone('Etc/GMT+5')

    # Variable global para controlar la aparición de eventos nocturnos
    global noche_aparecida_hoy
    noche_aparecida_hoy = False

    # Variable global para controlar el amanecer
    global dia_aparecido_hoy
    dia_aparecido_hoy = False
    
    def es_hora_8pm_gmt_minus_5():
        """Verifica si la hora actual en GMT-5 es 8:00 PM."""
        ahora = datetime.now(gmt_minus_5)
        return ahora.hour == 20 and ahora.minute == 0

    def es_hora_6am_gmt_minus_5():
        """Verifica si la hora actual en GMT-5 es 6:00 AM."""
        ahora = datetime.now(gmt_minus_5)
        return ahora.hour == 6 and ahora.minute == 0
    
    def es_hora_medianoche_gmt_minus_5():
        """Verifica si la hora actual en GMT-5 es medianoche."""
        ahora = datetime.now(gmt_minus_5)
        return ahora.hour == 0 and ahora.minute == 0

    # Configurar el bot con Intents
    intents = discord.Intents.default()
    intents.message_content = True
    bot = commands.Bot(command_prefix='!', intents=intents)

    # Define el ID del canal de Discord donde se enviarán los mensajes
    CHANNEL_ID = ID

    # Variables globales para control de eventos
    global evento_actual, tiempo_evento_actual, espera_evento_nuevo, duracion_evento
    evento_actual = None
    tiempo_evento_actual = 0
    espera_evento_nuevo = False
    duracion_evento = 0
    global boston_role

    @bot.event
    async def on_ready():
        global boston_role
        print(f'Bot conectado como {bot.user}')
        enviar_eventos.start()

        # Obtener el objeto del servidor
        guild = discord.utils.get(bot.guilds, id=ID)  

        # Obtener el rol @Commonwealth
        boston_role = discord.utils.get(guild.roles, name="Commonwealth")

    @tasks.loop(seconds=1)
    async def enviar_eventos():
        global evento_actual, tiempo_evento_actual, espera_evento_nuevo, noche_aparecida_hoy, dia_aparecido_hoy, duracion_evento, horas_transcurridas
        
        horas_transcurridas = 0

        max_horas = 13

        inicio = time.time()

        while horas_transcurridas < max_horas:
            time.sleep(3600)  # Espera una hora
            horas_transcurridas = (time.time() - inicio) / 3600

        if es_hora_medianoche_gmt_minus_5():
            noche_aparecida_hoy = False
            dia_aparecido_hoy = False
        
        if es_hora_8pm_gmt_minus_5():
            if not noche_aparecida_hoy:
                evento_noche = random.choice([evento for evento in eventos if evento["nombre"] in ["Noche", "Luna Llena", "Luna Nueva"]])
                channel = bot.get_channel(CHANNEL_ID)
                embed = discord.Embed(title=evento_noche["nombre"], 
                                    description=evento_noche["descripcion"], 
                                    color=discord.Color.blue())
                if "imagen" in evento_noche:
                    embed.set_image(url=evento_noche["imagen"])
                await channel.send(embed=embed)
                await channel.send(boston_role.mention)  # Arrobar al rol @Boston
                
                noche_aparecida_hoy = True  # Marcar que se ha enviado un evento nocturno hoy
        
        if es_hora_6am_gmt_minus_5():
            if not dia_aparecido_hoy:
                evento_dia = random.choice([evento for evento in eventos if evento["nombre"] in ["Amanecer"]])
                channel = bot.get_channel(CHANNEL_ID)
                embed = discord.Embed(title=evento_dia["nombre"], 
                                    description=evento_dia["descripcion"], 
                                    color=discord.Color.blue())
                if "imagen" in evento_dia:
                    embed.set_image(url=evento_dia["imagen"])
                await channel.send(embed=embed)
                await channel.send(boston_role.mention)  # Arrobar al rol @Boston
                
                dia_aparecido_hoy = True  # Marcar que ha amanecido hoy

        elif tiempo_evento_actual > 0:
            tiempo_evento_actual -= 1
            if tiempo_evento_actual == 0:
                if evento_actual and evento_actual["nombre"] != "nada xd":
                    channel = bot.get_channel(CHANNEL_ID)
                    duracion_evento_horas = duracion_evento // 3600
                    embed = discord.Embed(title=f"La {evento_actual['nombre']} ha terminado!",    
                                        description=f"El evento duró {duracion_evento_horas} horas.",
                                        color=discord.Color.green()) 
                    embed.set_image(url="https://media.discordapp.net/attachments/1023451309774487573/1261895046433603644/disco-elysium-rave.gif?ex=66949ed7&is=66934d57&hm=9392bc5221adb518e5f2916e844b1dd0732803bedc22d79e7ad09d48f5c27cda&=")
                    await channel.send(embed=embed)
                    await channel.send(boston_role.mention)  # Arrobar al rol @Boston

                    # Esperar entre 12 y 24 horas antes de iniciar el próximo evento
                    intervalo_aleatorio = random.randint(12 * 3600, 24 * 3600)
                    await asyncio.sleep(intervalo_aleatorio)
                    espera_evento_nuevo = False  # Deshabilitar la espera de nuevo evento

                    # Reiniciar variables para permitir el inicio de un nuevo evento
                    evento_actual = None
                    tiempo_evento_actual = 0
                    duracion_evento = 0

        elif not espera_evento_nuevo and horas_transcurridas >= 12:
            # Generar un evento basado en los pesos (excluyendo eventos especiales)
            evento_aleatorio = random.choices(eventos[1:], weights=pesos[1:], k=1)[0]
            evento_actual = evento_aleatorio

            # Si el evento es "nada xd", no enviar ningún mensaje
            if evento_aleatorio["nombre"] == "nada xd":
                return

            # Crear un Embed para el evento
            embed = discord.Embed(title=evento_actual["nombre"], 
                                description=evento_actual["descripcion"], 
                                color=discord.Color.blue())

            # Agregar la imagen al Embed si está disponible
            if "imagen" in evento_actual:
                embed.set_image(url=evento_actual["imagen"])

            # Enviar el Embed al canal de Discord
            channel = bot.get_channel(CHANNEL_ID)
            await channel.send(embed=embed)
            await channel.send(boston_role.mention)  # Arrobar al rol @Boston

            # Generar un intervalo de tiempo aleatorio entre 1 y 24 horas para la duración del evento
            intervalo_evento = random.randint(1 * 3600, 24 * 3600)
            tiempo_evento_actual = intervalo_evento
            duracion_evento = intervalo_evento  # Guardar la duración del evento

            # Imprimir la hora actual en GMT-8 en consola
            ahora_gmt_minus_5 = datetime.now(gmt_minus_5)
            print(f'Hora actual en GMT-5: {ahora_gmt_minus_5.strftime("%Y-%m-%d %H:%M:%S")}')
    
        # Esperar un segundo antes de verificar nuevamente
        await asyncio.sleep(1)

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