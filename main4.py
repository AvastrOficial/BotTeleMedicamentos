from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
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
    # (Añadir el resto de las soluciones aquí como se definió en tu código original)
}

# Variable para guardar los datos del recordatorio
recordatorios = {}

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
        
        # Botón para configurar recordatorio
        recordatorio_button = InlineKeyboardButton("Configurar Recordatorio", callback_data=f"recordatorio_{text}")
        markup = InlineKeyboardMarkup([[recordatorio_button]])
        
        await update.message.reply_text(mensaje, reply_markup=markup)

    else:
        await update.message.reply_text("No entendí tu mensaje. Por favor selecciona una enfermedad o un síntoma.")

# Función para establecer la hora y enviar el recordatorio
async def configurar_recordatorio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Extraemos la información del callback
    callback_data = update.callback_query.data
    _, sintoma = callback_data.split("_")
    
    # Pedimos al usuario elegir entre "Despertino" o "Matutino"
    await update.callback_query.answer()
    markup = InlineKeyboardMarkup([ 
        [InlineKeyboardButton("Despertino", callback_data=f"despertino_{sintoma}")],
        [InlineKeyboardButton("Matutino", callback_data=f"matutino_{sintoma}")]
    ])
    await update.callback_query.message.reply_text("¿Cuándo quieres el recordatorio? Elige entre 'Despertino' o 'Matutino'.", reply_markup=markup)

# Función para configurar la hora según la elección (Despertino o Matutino)
async def elegir_hora(update: Update, context: ContextTypes.DEFAULT_TYPE):
    callback_data = update.callback_query.data
    _, sintoma, momento = callback_data.split("_")
    
    # Guardamos el momento de elección (despertino o matutino)
    recordatorios[update.callback_query.from_user.id] = {
        "sintoma": sintoma,
        "hora": None,
        "momento": momento
    }
    
    # Definir las horas según el momento elegido
    if momento == "despertino":
        horas = ["6:00 PM", "7:00 PM", "8:00 PM"]
    elif momento == "matutino":
        horas = ["7:00 AM", "8:00 AM", "9:00 AM"]
    
    # Creamos los botones para elegir una de las horas
    botones_horas = [InlineKeyboardButton(hora, callback_data=f"hora_{sintoma}_{momento}_{hora}") for hora in horas]
    markup = InlineKeyboardMarkup([botones_horas])
    
    await update.callback_query.answer()
    await update.callback_query.message.reply_text(f"Selecciona la hora para el recordatorio para el síntoma '{sintoma}':", reply_markup=markup)

# Función para confirmar y programar el recordatorio
async def confirmar_recordatorio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    callback_data = update.callback_query.data
    _, sintoma, momento, hora = callback_data.split("_")

    # Guardamos la hora del recordatorio
    recordatorios[update.callback_query.from_user.id]["hora"] = hora

    # Enviar mensaje de confirmación
    await update.callback_query.answer()
    await update.callback_query.message.reply_text(f"Recordatorio configurado para el síntoma '{sintoma}' a las {hora} {momento}.")

# Main
def main():
    application = Application.builder().token(TOKEN).build()

    # Comandos
    application.add_handler(CommandHandler("start", start))

    # Mensajes
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_response))

    # Callbacks
    application.add_handler(MessageHandler(filters.Regex("recordatorio_.*"), configurar_recordatorio))
    application.add_handler(MessageHandler(filters.Regex("hora_.*"), confirmar_recordatorio))

    application.run_polling()

if __name__ == "__main__":
    main()
