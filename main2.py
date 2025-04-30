from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

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

   soluciones = {
    "Sed excesiva": {
        "solucion": "La sed excesiva puede estar relacionada con la diabetes o deshidratación. Beber más agua es esencial. Considera una botella de agua reutilizable.",
        "producto": "https://www.amazon.com/dp/B08HZ3V6ZP"  # Enlace a botella de agua
    },
    "Micción frecuente": {
        "solucion": "La micción frecuente puede ser un síntoma de infecciones del tracto urinario. Se recomienda consultar a un médico.",
        "producto": "https://www.amazon.com/dp/B07P8LHGZB"  # Enlace a suplemento para la salud urinaria
    },
    "Hambre constante": {
        "solucion": "La hambre constante podría estar asociada con problemas metabólicos. Considera una dieta balanceada.",
        "producto": "https://www.amazon.com/dp/B089FVG58B"  # Enlace a snacks saludables
    },
    "Pérdida de peso sin causa aparente": {
        "solucion": "La pérdida de peso inexplicada debe ser evaluada por un profesional de la salud. Podría estar asociada a condiciones graves.",
        "producto": "https://www.amazon.com/dp/B00NT1N9PA"  # Enlace a suplemento nutricional
    },
    "Visión borrosa": {
        "solucion": "La visión borrosa podría ser un síntoma de diabetes o problemas oculares. Visita a un oftalmólogo.",
        "producto": "https://www.amazon.com/dp/B07NTZT92B"  # Enlace a gotas para ojos
    },
    "Fatiga": {
        "solucion": "La fatiga extrema podría estar asociada con deficiencias nutricionales. Asegúrate de descansar bien y comer saludablemente.",
        "producto": "https://www.amazon.com/dp/B07N7Q2FNR"  # Enlace a suplemento de vitaminas
    },
    "Heridas que tardan en sanar": {
        "solucion": "Si las heridas tardan en sanar, podría ser un signo de diabetes o deficiencias nutricionales. Consulta con un profesional.",
        "producto": "https://www.amazon.com/dp/B08R9R2P75"  # Enlace a crema cicatrizante
    },
    "Fatiga extrema": {
        "solucion": "La fatiga extrema puede ser señal de anemia o trastornos del sueño. Es recomendable realizar un chequeo médico.",
        "producto": "https://www.amazon.com/dp/B00B5P3FZG"  # Enlace a suplemento energético
    },
    "Hinchazón en piernas, tobillos o pies": {
        "solucion": "La hinchazón puede estar relacionada con problemas circulatorios. Usar medias de compresión puede ayudar.",
        "producto": "https://www.amazon.com/dp/B0851XK89B"  # Enlace a medias de compresión
    },
    "Dificultad para concentrarse": {
        "solucion": "La falta de concentración podría ser un síntoma de ansiedad o falta de sueño. Intenta mejorar tu rutina de descanso.",
        "producto": "https://www.amazon.com/dp/B08ZDQF9TZ"  # Enlace a suplementos para mejorar la concentración
    },
    "Orina espumosa": {
        "solucion": "La orina espumosa puede indicar problemas renales. Es recomendable realizar exámenes médicos para evaluar la función renal.",
        "producto": "https://www.amazon.com/dp/B085M92H93"  # Enlace a suplemento renal
    },
    "Náuseas y vómitos": {
        "solucion": "Las náuseas y los vómitos pueden ser signos de una infección o trastorno gastrointestinal. Mantente hidratado y considera medicamentos antieméticos.",
        "producto": "https://www.amazon.com/dp/B08ZYQHNGX"  # Enlace a medicamento para náuseas
    },
    "Pérdida de apetito": {
        "solucion": "La pérdida de apetito podría estar relacionada con estrés o deficiencias nutricionales. Consulta con un profesional si persiste.",
        "producto": "https://www.amazon.com/dp/B01M8PL4T9"  # Enlace a suplemento para estimular el apetito
    },
    "Dolor de cabeza": {
        "solucion": "El dolor de cabeza puede ser causado por tensión, migrañas o deshidratación. Asegúrate de descansar y beber agua.",
        "producto": "https://www.amazon.com/dp/B07ZK8T2W9"  # Enlace a analgésico para dolor de cabeza
    },
    "Mareos": {
        "solucion": "Los mareos pueden ser provocados por diversas causas, desde deshidratación hasta problemas del oído interno. Es importante consultar a un médico.",
        "producto": "https://www.amazon.com/dp/B0844FVV3D"  # Enlace a suplemento para mareos
    },
    "Dolor en el pecho": {
        "solucion": "El dolor en el pecho puede ser una señal de un problema cardiovascular. Es fundamental buscar atención médica inmediatamente.",
        "producto": "https://www.amazon.com/dp/B07TTZ9X2S"  # Enlace a monitor de presión arterial
    },
    "Dificultad para respirar": {
        "solucion": "La dificultad para respirar puede indicar un problema respiratorio o cardiovascular. Busca atención médica de inmediato.",
        "producto": "https://www.amazon.com/dp/B07V5JZP4X"  # Enlace a inhalador o nebulizador
    },
    "Sangrado nasal": {
        "solucion": "El sangrado nasal puede ser causado por sequedad o irritación en las fosas nasales. Mantén la humedad en el ambiente.",
        "producto": "https://www.amazon.com/dp/B07MJJXHDB"  # Enlace a humidificador
    },
    "Postura encorvada": {
        "solucion": "Una postura encorvada puede ser un signo de debilidad muscular o estrés. Realizar ejercicios de estiramiento y fortalecimiento puede ayudar.",
        "producto": "https://www.amazon.com/dp/B08QY4JZZ7"  # Enlace a cinturón de corrección de postura
    },
    "Fracturas óseas frecuentes": {
        "solucion": "Las fracturas frecuentes pueden ser un signo de osteoporosis. Es importante evaluar la salud ósea con un médico.",
        "producto": "https://www.amazon.com/dp/B07SGZ26VY"  # Enlace a suplemento de calcio
    },
    "Cansancio o fatiga": {
        "solucion": "El cansancio excesivo puede ser causado por estrés, falta de sueño o deficiencias nutricionales. Intenta descansar mejor y mejorar tu dieta.",
        "producto": "https://www.amazon.com/dp/B08T5W8RHV"  # Enlace a suplementos energéticos
    },
    "Alteraciones del sueño": {
        "solucion": "Las alteraciones del sueño pueden ser causadas por estrés o trastornos médicos. Intenta mejorar tu higiene del sueño.",
        "producto": "https://www.amazon.com/dp/B08K2F9D69"  # Enlace a suplemento para mejorar el sueño
    },
    "Dificultad para moverse": {
        "solucion": "La dificultad para moverse puede estar asociada con problemas articulares o musculares. Considera un tratamiento para el dolor o rigidez.",
        "producto": "https://www.amazon.com/dp/B08K7JY2GS"  # Enlace a terapia de calor
    },
    "Ansiedad o depresión": {
        "solucion": "La ansiedad o depresión son trastornos emocionales que deben ser tratados con apoyo profesional. Considera realizar terapia o tomar suplementos para el ánimo.",
        "producto": "https://www.amazon.com/dp/B0851R5RT2"  # Enlace a suplemento para la ansiedad
    },
    "Palpitaciones": {
        "solucion": "Las palpitaciones pueden ser causadas por ansiedad o problemas cardíacos. Si persisten, es importante consultar a un médico.",
        "producto": "https://www.amazon.com/dp/B085RFR8NS"  # Enlace a monitor de frecuencia cardíaca
    },
    "Mareos o desmayos": {
        "solucion": "Los mareos o desmayos pueden estar relacionados con problemas de presión arterial o deshidratación. Es importante consultar con un médico.",
        "producto": "https://www.amazon.com/dp/B08F4J54YS"  # Enlace a monitor de presión arterial
    }
}
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

    else:
        await update.message.reply_text("No entendí tu mensaje. Por favor selecciona una enfermedad o un síntoma.")

# MAIN para arrancar el bot
def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_response))
    print("Bot corriendo...")
    app.run_polling()

if __name__ == "__main__":
    main()
