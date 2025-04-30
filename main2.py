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

# Diccionario de soluciones (Definido FUERA de la función)
soluciones = {
    "Sed excesiva": {
        "solucion": "La sed excesiva puede estar relacionada con la diabetes o deshidratación. Beber más agua es esencial.",
        "producto": "https://www.amazon.com/dp/B08HZ3V6ZP"
    },
    "Micción frecuente": {
        "solucion": "La micción frecuente puede ser un síntoma de infecciones del tracto urinario. Se recomienda consultar a un médico.",
        "producto": "https://www.amazon.com/dp/B07P8LHGZB"
    },
    "Hambre constante": {
        "solucion": "El hambre constante podría estar asociada con problemas metabólicos. Considera una dieta balanceada.",
        "producto": "https://www.amazon.com/dp/B089FVG58B"
    },
    "Pérdida de peso sin causa aparente": {
        "solucion": "La pérdida de peso inexplicada debe ser evaluada por un profesional de la salud.",
        "producto": "https://www.amazon.com/dp/B00NT1N9PA"
    },
    "Visión borrosa": {
        "solucion": "La visión borrosa podría ser un síntoma de diabetes o problemas oculares.",
        "producto": "https://www.amazon.com/dp/B07NTZT92B"
    },
    "Fatiga": {
        "solucion": "La fatiga extrema podría estar asociada con deficiencias nutricionales.",
        "producto": "https://www.amazon.com/dp/B07N7Q2FNR"
    },
    "Heridas que tardan en sanar": {
        "solucion": "Si las heridas tardan en sanar, podría ser un signo de diabetes o deficiencias nutricionales.",
        "producto": "https://www.amazon.com/dp/B08R9R2P75"
    },
    "Dolor de cabeza": {
        "solucion": "El dolor de cabeza puede ser causado por tensión, migrañas o deshidratación.",
        "producto": "https://www.amazon.com/dp/B07ZK8T2W9"
    },
    "Mareos": {
        "solucion": "Los mareos pueden ser provocados por diversas causas. Es importante consultar a un médico.",
        "producto": "https://www.amazon.com/dp/B0844FVV3D"
    },
    "Dolor en el pecho": {
        "solucion": "El dolor en el pecho puede ser una señal de un problema cardiovascular. Busca atención médica.",
        "producto": "https://www.amazon.com/dp/B07TTZ9X2S"
    },
    "Dificultad para respirar": {
        "solucion": "La dificultad para respirar puede indicar un problema respiratorio o cardiovascular.",
        "producto": "https://www.amazon.com/dp/B07V5JZP4X"
    }
    # Puedes agregar más si quieres aquí
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
