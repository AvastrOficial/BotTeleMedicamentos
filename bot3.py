from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler
from datetime import datetime, timedelta
import pytz

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

# Diccionario de soluciones
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

# Variables para el tratamiento
tratamiento_info = {}

# Generar botones de enfermedades
def generar_botones_enfermedades():
    enfermedades = list(enfermedades_sintomas.keys())
    botones = []
    for i in range(0, len(enfermedades), 2):
        fila = enfermedades[i:i+2]
        botones.append(fila)
    return botones

# Generar botones de síntomas según la enfermedad seleccionada
def generar_botones_sintomas(enfermedad_seleccionada):
    sintomas = enfermedades_sintomas[enfermedad_seleccionada]
    return sintomas

# Selector de hora para el medicamento
async def seleccionar_hora(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Preguntar por la hora para el medicamento
    await update.message.reply_text("¿A qué hora quieres tomar el medicamento? (Formato: HH:MM)")

# Función para manejar la hora seleccionada
async def manejar_hora(update: Update, context: ContextTypes.DEFAULT_TYPE):
    hora_str = update.message.text.strip()
    try:
        hora = datetime.strptime(hora_str, "%H:%M")
        tz = pytz.timezone("America/Mexico_City")  # Cambia esto según tu zona horaria
        hora_local = tz.localize(hora)

        tratamiento_info["hora"] = hora_local
        await update.message.reply_text(f"Has seleccionado la hora {hora_local.strftime('%H:%M')} para tomar tu medicamento.")
        
        # Preguntar por la duración del tratamiento
        await update.message.reply_text("¿Cuántos días durará el tratamiento?")

    except ValueError:
        await update.message.reply_text("Formato de hora incorrecto. Por favor ingresa la hora en formato HH:MM.")

# Función para manejar la duración del tratamiento
async def manejar_duracion(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        dias = int(update.message.text.strip())
        if dias <= 0:
            raise ValueError

        tratamiento_info["duracion"] = dias
        tratamiento_info["fin"] = tratamiento_info["hora"] + timedelta(days=dias)

        # Preguntar por el número de dosis por día
        await update.message.reply_text("¿Cuántas dosis tomarás por día?")

    except ValueError:
        await update.message.reply_text("Por favor, ingresa un número válido para la duración del tratamiento (en días).")

# Función para manejar el número de dosis
async def manejar_dosis(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        dosis = int(update.message.text.strip())
        if dosis <= 0:
            raise ValueError

        tratamiento_info["dosis"] = dosis
        tratamiento_info["total_dosis"] = tratamiento_info["duracion"] * dosis

        # Mostrar la información del tratamiento
        mensaje = (
            f"Duración del tratamiento: {tratamiento_info['duracion']} días\n"
            f"Hora de tomar el medicamento: {tratamiento_info['hora'].strftime('%H:%M')}\n"
            f"Número de dosis por día: {tratamiento_info['dosis']}\n"
            f"Total de dosis: {tratamiento_info['total_dosis']}\n"
            f"Fecha de inicio: {tratamiento_info['hora'].strftime('%Y-%m-%d')}\n"
            f"Fecha de fin: {tratamiento_info['fin'].strftime('%Y-%m-%d')}\n"
        )
        await update.message.reply_text(mensaje)

        # Programar recordatorio
        await recordatorio(update, context)

    except ValueError:
        await update.message.reply_text("Por favor, ingresa un número válido para las dosis por día.")

# Función para enviar un recordatorio automático
async def recordatorio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    hora_recordatorio = tratamiento_info["hora"]
    segundos_para_recordatorio = (hora_recordatorio - datetime.now(pytz.timezone("America/Mexico_City"))).total_seconds()

    if segundos_para_recordatorio > 0:
        context.job_queue.run_once(
            enviar_recordatorio,
            segundos_para_recordatorio,
            context=update.message.chat_id
        )
        await update.message.reply_text(f"Te recordaré a las {hora_recordatorio.strftime('%H:%M')} para tomar tu medicamento.")

# Función para enviar el recordatorio
async def enviar_recordatorio(context: ContextTypes.DEFAULT_TYPE):
    chat_id = context.job.context
    await context.bot.send_message(chat_id, "Es hora de tomar tu medicamento.")

# Comando /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    botones_enfermedades = generar_botones_enfermedades()
    markup = ReplyKeyboardMarkup(botones_enfermedades, one_time_keyboard=True, resize_keyboard=True)
    await update.message.reply_text("Selecciona tu enfermedad:", reply_markup=markup)

# Manejar respuestas
async def handle_response(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text in enfermedades_sintomas:
        botones_sintomas = generar_botones_sintomas(text)
        markup = ReplyKeyboardMarkup(botones_sintomas, one_time_keyboard=True, resize_keyboard=True)
        await update.message.reply_text(f"Selecciona un síntoma para {text}:", reply_markup=markup)

    elif text in soluciones:
        respuesta = soluciones[text]
        mensaje = f"{respuesta['solucion']}\nProducto recomendado: {respuesta['producto']}"
        await update.message.reply_text(mensaje)

    elif text in tratamiento_info:
        await seleccionar_hora(update, context)

    else:
        await update.message.reply_text("No entendí tu mensaje. Por favor selecciona una enfermedad o un síntoma.")

# MAIN para arrancar el bot
def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_response))
    app.add_handler(MessageHandler(filters.TEXT, manejar_hora))
    app.add_handler(MessageHandler(filters.TEXT, manejar_duracion))
    app.add_handler(MessageHandler(filters.TEXT, manejar_dosis))

    print("Bot corriendo...")
    app.run_polling()

if __name__ == "__main__":
    main()
