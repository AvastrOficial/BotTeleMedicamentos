from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
import asyncio

TOKEN = input("Introduce el token del bot de Telegram: ")

# Relación entre enfermedades y síntomas
enfermedades_sintomas = {
    "Diabetes": [
        ["Sed excesiva", "Micción frecuente"],
        ["Hambre constante", "Pérdida de peso sin causa aparente"],
        ["Visión borrosa", "Fatiga"],
        ["Heridas que tardan en sanar"]
    ],
    "Enfermedades Renales": [
        ["Fatiga", "Hinchazón en piernas, tobillos o pies"],
        ["Dificultad para concentrarse", "Orina espumosa"],
        ["Náuseas y vómitos", "Pérdida de apetito"]
    ],
    "Hipertensión": [
        ["Dolor de cabeza", "Mareos"],
        ["Visión borrosa", "Zumbido en los oídos"],
        ["Dolor en el pecho", "Dificultad para respirar"],
        ["Sangrado nasal"]
    ],
    "Descalcificación Ósea": [
        ["Dolor de espalda", "Disminución de estatura con el tiempo"],
        ["Postura encorvada", "Fracturas óseas frecuentes o fáciles"]
    ],
    "Dolores Crónicos": [
        ["Dolor persistente por más de 3 meses", "Cansancio o fatiga"],
        ["Alteraciones del sueño", "Dificultad para moverse o realizar actividades cotidianas"],
        ["Ansiedad o depresión relacionada al dolor"]
    ],
    "Enfermedades Cardiovasculares": [
        ["Dolor en el pecho", "Falta de aire"],
        ["Palpitaciones", "Mareos o desmayos"],
        ["Hinchazón en piernas o tobillos", "Fatiga extrema"]
    ]
}

# Diccionario de soluciones (Definido FUERA de la función)
soluciones = {
    "Sed excesiva": {
        "solucion": "La sed excesiva puede estar relacionada con la diabetes o deshidratación. Beber más agua es esencial. Considera una botella de agua reutilizable.",
        "producto": "https://www.amazon.com/s?k=reusable+water+bottle"
    },
    "Micción frecuente": {
        "solucion": "La micción frecuente puede ser un síntoma de infecciones del tracto urinario. Se recomienda consultar a un médico.",
        "producto": "https://www.amazon.com/s?k=urinary+tract+health+supplement"
    },
    "Hambre constante": {
        "solucion": "La hambre constante podría estar asociada con problemas metabólicos. Considera una dieta balanceada.",
        "producto": "https://www.amazon.com/s?k=healthy+snacks"
    },
    "Pérdida de peso sin causa aparente": {
        "solucion": "La pérdida de peso inexplicada debe ser evaluada por un profesional de la salud. Podría estar asociada a condiciones graves.",
        "producto": "https://www.amazon.com/s?k=nutritional+supplement+for+weight+gain"
    },
    "Visión borrosa": {
        "solucion": "La visión borrosa podría ser un síntoma de diabetes o problemas oculares. Visita a un oftalmólogo.",
        "producto": "https://www.amazon.com/s?k=eye+drops"
    },
    "Fatiga": {
        "solucion": "La fatiga extrema podría estar asociada con deficiencias nutricionales. Asegúrate de descansar bien y comer saludablemente.",
        "producto": "https://www.amazon.com/s?k=vitamin+supplements"
    },
    "Heridas que tardan en sanar": {
        "solucion": "Si las heridas tardan en sanar, podría ser un signo de diabetes o deficiencias nutricionales. Consulta con un profesional.",
        "producto": "https://www.amazon.com/s?k=wound+healing+ointment"
    },
    "Fatiga extrema": {
        "solucion": "La fatiga extrema puede ser señal de anemia o trastornos del sueño. Es recomendable realizar un chequeo médico.",
        "producto": "https://www.amazon.com/s?k=energy+supplement"
    },
    "Hinchazón en piernas, tobillos o pies": {
        "solucion": "La hinchazón puede estar relacionada con problemas circulatorios. Usar medias de compresión puede ayudar.",
        "producto": "https://www.amazon.com/s?k=compression+socks"
    },
    "Dificultad para concentrarse": {
        "solucion": "La falta de concentración podría ser un síntoma de ansiedad o falta de sueño. Intenta mejorar tu rutina de descanso.",
        "producto": "https://www.amazon.com/s?k=brain+supplement"
    },
    "Orina espumosa": {
        "solucion": "La orina espumosa puede indicar problemas renales. Es recomendable realizar exámenes médicos para evaluar la función renal.",
        "producto": "https://www.amazon.com/s?k=kidney+support+supplement"
    },
    "Náuseas y vómitos": {
        "solucion": "Las náuseas y los vómitos pueden ser signos de una infección o trastorno gastrointestinal. Mantente hidratado y considera medicamentos antieméticos.",
        "producto": "https://www.amazon.com/s?k=anti+nausea+medicine"
    },
    "Pérdida de apetito": {
        "solucion": "La pérdida de apetito podría estar relacionada con estrés o deficiencias nutricionales. Consulta con un profesional si persiste.",
        "producto": "https://www.amazon.com/s?k=appetite+stimulant+supplement"
    },
    "Dolor de cabeza": {
        "solucion": "El dolor de cabeza puede ser causado por tensión, migrañas o deshidratación. Asegúrate de descansar y beber agua.",
        "producto": "https://www.amazon.com/s?k=headache+relief+medicine"
    },
    "Mareos": {
        "solucion": "Los mareos pueden ser provocados por diversas causas, desde deshidratación hasta problemas del oído interno. Es importante consultar a un médico.",
        "producto": "https://www.amazon.com/s?k=dizziness+relief+supplement"
    },
    "Dolor en el pecho": {
        "solucion": "El dolor en el pecho puede ser una señal de un problema cardiovascular. Es fundamental buscar atención médica inmediatamente.",
        "producto": "https://www.amazon.com/s?k=blood+pressure+monitor"
    },
    "Dificultad para respirar": {
        "solucion": "La dificultad para respirar puede indicar un problema respiratorio o cardiovascular. Busca atención médica de inmediato.",
        "producto": "https://www.amazon.com/s?k=nebulizer+inhaler"
    },
    "Sangrado nasal": {
        "solucion": "El sangrado nasal puede ser causado por sequedad o irritación en las fosas nasales. Mantén la humedad en el ambiente.",
        "producto": "https://www.amazon.com/s?k=humidifier"
    },
    "Postura encorvada": {
        "solucion": "Una postura encorvada puede ser un signo de debilidad muscular o estrés. Realizar ejercicios de estiramiento y fortalecimiento puede ayudar.",
        "producto": "https://www.amazon.com/s?k=posture+corrector"
    },
    "Fracturas óseas frecuentes": {
        "solucion": "Las fracturas frecuentes pueden ser un signo de osteoporosis. Es importante evaluar la salud ósea con un médico.",
        "producto": "https://www.amazon.com/s?k=calcium+supplement"
    },
    "Cansancio o fatiga": {
        "solucion": "El cansancio excesivo puede ser causado por estrés, falta de sueño o deficiencias nutricionales. Intenta descansar mejor y mejorar tu dieta.",
        "producto": "https://www.amazon.com/s?k=energy+vitamins"
    },
    "Alteraciones del sueño": {
        "solucion": "Las alteraciones del sueño pueden ser causadas por estrés o trastornos médicos. Intenta mejorar tu higiene del sueño.",
        "producto": "https://www.amazon.com/s?k=sleep+supplement"
    },
    "Dificultad para moverse": {
        "solucion": "La dificultad para moverse puede estar asociada con problemas articulares o musculares. Considera un tratamiento para el dolor o rigidez.",
        "producto": "https://www.amazon.com/s?k=heat+therapy+pad"
    },
    "Ansiedad o depresión": {
        "solucion": "La ansiedad o depresión son trastornos emocionales que deben ser tratados con apoyo profesional. Considera realizar terapia o tomar suplementos para el ánimo.",
        "producto": "https://www.amazon.com/s?k=anxiety+relief+supplement"
    },
    "Palpitaciones": {
        "solucion": "Las palpitaciones pueden ser causadas por ansiedad o problemas cardíacos. Si persisten, es importante consultar a un médico.",
        "producto": "https://www.amazon.com/s?k=heart+rate+monitor"
    },
    "Mareos o desmayos": {
        "solucion": "Los mareos o desmayos pueden estar relacionados con problemas de presión arterial o deshidratación. Es importante consultar con un médico.",
        "producto": "https://www.amazon.com/s?k=blood+pressure+monitor"
    }
}


# Comando /start -> muestra lista de enfermedades
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = []
    for enfermedad in enfermedades_sintomas.keys():
        keyboard.append([InlineKeyboardButton(enfermedad, callback_data=f"enfermedad_{enfermedad}")])
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Selecciona una enfermedad:", reply_markup=reply_markup)

# Manejar selección de enfermedad -> muestra síntomas
async def manejar_enfermedad(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    enfermedad = query.data.split("_")[1]
    sintomas = enfermedades_sintomas.get(enfermedad, [])

    keyboard = []
    for fila in sintomas:
        row = [InlineKeyboardButton(sintoma, callback_data=f"sintoma_{sintoma}") for sintoma in fila]
        keyboard.append(row)

    await query.edit_message_text(
        text=f"Selecciona un síntoma relacionado con *{enfermedad}*:",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode='Markdown'
    )

# Manejar selección de síntoma -> muestra botón "Configurar Recordatorio"
async def manejar_sintoma(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    sintoma = query.data.split("_", 1)[1]

    keyboard = [
        [InlineKeyboardButton("Configurar Recordatorio", callback_data=f"recordatorio_{sintoma}")]
    ]
    await query.edit_message_text(
        text=f"Has seleccionado el síntoma: *{sintoma}*",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode='Markdown'
    )

# Diccionario global para almacenar los recordatorios de cada usuario
recordatorios = {}

# 1️⃣ Configurar recordatorio -> muestra opciones de tiempo
async def configurar_recordatorio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    sintoma = query.data.split("_", 1)[1]  # Obtenemos solo el síntoma

    keyboard = [
        [InlineKeyboardButton("Cada 1 min", callback_data=f"hora|{sintoma}|1")],
        [InlineKeyboardButton("Cada 2 min", callback_data=f"hora|{sintoma}|2")],
        [InlineKeyboardButton("Cada 5 min", callback_data=f"hora|{sintoma}|5")],
    ]
    await query.edit_message_text(
        text=f"Configura el recordatorio para *{sintoma}*",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode='Markdown'
    )

# 2️⃣ Elegir hora -> guarda recordatorio
async def elegir_hora(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    _, sintoma, minutos = query.data.split("|")  # Split seguro usando |
    user_id = query.from_user.id

    tiempo = int(minutos)
    
    # Guarda el recordatorio en el diccionario global
    recordatorios[user_id] = {"sintoma": sintoma, "intervalo": tiempo}

    await query.edit_message_text(
        text=f"✅ Recordatorio configurado para *{sintoma}* cada {tiempo} minutos.",
        parse_mode='Markdown'
    )

    # Opcional: Iniciar recordatorio (simple demostración)
    asyncio.create_task(enviar_recordatorio(update, context, user_id))

# 3️⃣ Enviar recordatorio repetidamente (opcional, demostración)
async def enviar_recordatorio(update: Update, context: ContextTypes.DEFAULT_TYPE, user_id):
    data = recordatorios.get(user_id)
    if not data:
        return

    intervalo = data["intervalo"]
    sintoma = data["sintoma"]

    while True:
        await context.bot.send_message(
            chat_id=user_id,
            text=f"🔔 Recordatorio de síntoma: *{sintoma}*",
            parse_mode='Markdown'
        )
        await asyncio.sleep(intervalo * 60)

# Configuración del bot
app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(manejar_enfermedad, pattern=r'^enfermedad_'))
app.add_handler(CallbackQueryHandler(manejar_sintoma, pattern=r'^sintoma_'))
app.add_handler(CallbackQueryHandler(configurar_recordatorio, pattern=r'^recordatorio_'))
app.add_handler(CallbackQueryHandler(elegir_hora, pattern=r'^hora_'))

# Ejecutar el bot
print("🤖 Bot iniciado...")
app.run_polling()
