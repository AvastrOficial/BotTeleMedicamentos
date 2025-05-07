from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
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

# Función que se ejecuta cada vez que un usuario solicita la ayuda
async def ayuda(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            KeyboardButton("Diabetes"),
            KeyboardButton("Enfermedades Renales"),
        ],
        [
            KeyboardButton("Hipertensión"),
            KeyboardButton("Descalcificación Ósea"),
        ],
        [
            KeyboardButton("Dolores Crónicos"),
            KeyboardButton("Enfermedades Cardiovasculares"),
        ],
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    await update.message.reply_text('Selecciona la enfermedad para ver los síntomas comunes', reply_markup=reply_markup)

# Función que devuelve los síntomas según la enfermedad seleccionada
async def enfermedad(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = update.message.text
    if texto in enfermedades_sintomas:
        sintomas = "\n".join([f"- {item}" for sublist in enfermedades_sintomas[texto] for item in sublist])
        await update.message.reply_text(f"Síntomas comunes de {texto}:\n\n{sintomas}")
    else:
        await update.message.reply_text("Lo siento, no tengo información sobre esa enfermedad.")

# Función que recomienda productos para cada síntoma
async def recomendar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = update.message.text
    if texto in soluciones:
        solucion = soluciones[texto]["solucion"]
        producto = soluciones[texto]["producto"]
        await update.message.reply_text(f"Recomendación para el síntoma '{texto}':\n\n{solucion}\n\nPuedes encontrar productos recomendados aquí: {producto}")
    else:
        await update.message.reply_text("Lo siento, no tengo recomendaciones para ese síntoma.")

# Configuración del bot
async def main():
    application = Application.builder().token(TOKEN).build()

    # Comandos
    application.add_handler(CommandHandler("start", ayuda))

    # Mensajes
    application.add_handler(MessageHandler(filters.Text("Diabetes"), enfermedad))
    application.add_handler(MessageHandler(filters.Text("Enfermedades Renales"), enfermedad))
    application.add_handler(MessageHandler(filters.Text("Hipertensión"), enfermedad))
    application.add_handler(MessageHandler(filters.Text("Descalcificación Ósea"), enfermedad))
    application.add_handler(MessageHandler(filters.Text("Dolores Crónicos"), enfermedad))
    application.add_handler(MessageHandler(filters.Text("Enfermedades Cardiovasculares"), enfermedad))
    
    application.add_handler(MessageHandler(filters.Text("Sed excesiva"), recomendar))
    application.add_handler(MessageHandler(filters.Text("Micción frecuente"), recomendar))
    application.add_handler(MessageHandler(filters.Text("Hambre constante"), recomendar))
    application.add_handler(MessageHandler(filters.Text("Pérdida de peso sin causa aparente"), recomendar))

    # Ejecuta el bot
    await application.run_polling()

if __name__ == '__main__':
    try:
        asyncio.run(main())  # Usa asyncio.run si no hay un bucle en ejecución
    except RuntimeError as e:
        if 'This event loop is already running' in str(e):
            # Si el bucle ya está en ejecución, usa await directamente
            loop = asyncio.get_event_loop()
            loop.create_task(main())  # Crea una tarea para ejecutarse en el bucle actual
