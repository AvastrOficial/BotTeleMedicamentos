from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = input("Introduce el token del bot de Telegram: ")

# Relación entre enfermedades y síntomas
enfermedades_sintomas = {
    "Diabetes": [["Insomnio", "Mareo"], ["Baja glucosa", "Dolor de cabeza"]],
    "Enfermedades Renales": [["Dolor de cabeza", "Deshidratación"], ["Baja glucosa", "Dolores Crónicos"]],
    "Hipertensión": [["Mareo", "Dolor de cabeza"], ["Visión borrosa", "Dolor de articulaciones"]],
    "Descalcificación Ósea": [["Dolores Crónicos", "Deshidratación"], ["Mareo", "Visión borrosa"]],
    "Dolores Crónicos": [["Dolor de cabeza", "Dolor de articulaciones"], ["Mareo", "Deshidratación"]],
    "Enfermedades Cardiovasculares": [["Dolor de cabeza", "Mareo"], ["Dolores Crónicos", "Visión borrosa"]],
}

# Teclado para enfermedades
keyboard_enfermedades = [
    ["Diabetes", "Enfermedades Renales"],
    ["Hipertensión", "Descalcificación Ósea"],
    ["Dolores Crónicos", "Enfermedades Cardiovasculares"]
]

# Teclado para síntomas
keyboard_problemas = [
    ["Insomnio", "Mareo"], 
    ["Visión borrosa", "Dolor de cabeza"], 
    ["Baja glucosa", "Dolor de articulaciones", "Deshidratación"]
]

# Generar botones de enfermedades con paginación
def generar_botones_enfermedades():
    enfermedades = list(enfermedades_sintomas.keys())
    botones = []
    # Organiza las enfermedades en grupos de 4
    for i in range(0, len(enfermedades), 2):  # Se muestran de 2 en 2
        fila = enfermedades[i:i+2]
        botones.append(fila)
    return botones

# Generar botones de síntomas según la enfermedad seleccionada
def generar_botones_sintomas(enfermedad_seleccionada):
    sintomas = enfermedades_sintomas[enfermedad_seleccionada]
    botones_sintomas = []
    # Organiza los síntomas en grupos de 2
    for fila in sintomas:
        botones_sintomas.append(fila)
    return botones_sintomas

# Función principal del bot
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Generar teclado de enfermedades
    botones_enfermedades = generar_botones_enfermedades()
    markup = ReplyKeyboardMarkup(botones_enfermedades, one_time_keyboard=True, resize_keyboard=True)
    await update.message.reply_text("Selecciona tu enfermedad:", reply_markup=markup)

# Función para manejar las respuestas de los usuarios
async def handle_response(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    
    if text in enfermedades_sintomas:
        # Si el texto es una enfermedad, se muestran los síntomas relacionados
        botones_sintomas = generar_botones_sintomas(text)
        markup = ReplyKeyboardMarkup(botones_sintomas, one_time_keyboard=True, resize_keyboard=True)
        await update.message.reply_text(f"Selecciona un síntoma para {text}:", reply_markup=markup)

    elif text in ["Insomnio", "Mareo", "Dolor de cabeza", "Baja glucosa", "Dolor de articulaciones", "Deshidratación", "Visión borrosa", "Dolores Crónicos"]:
        # Mostrar soluciones dependiendo del síntoma
        soluciones = {
            "Insomnio": (
                "Medicamentos sugeridos para Insomnio:\n"
                "- Melatonina 3mg (1 hora antes de dormir)\n"
                "- Difenhidramina (uso ocasional)\n"
                "- Valeriana (alternativa natural)\n\n"
                "Compra aquí: https://www.farmalisto.com.mx/insomnio"
            ),
            "Mareo": (
                "Medicamentos sugeridos para Mareo:\n"
                "- Dimenhidrinato 50mg (cada 8h si es necesario)\n"
                "- Meclizina (ideal para vértigo leve)\n\n"
                "Compra aquí: https://www.farmalisto.com.mx/mareo"
            ),
            "Dolor de cabeza": (
                "Medicamentos sugeridos:\n"
                "- Paracetamol 500mg (cada 6h si el dolor persiste)\n"
                "- Ibuprofeno (si hay inflamación o tensión muscular)\n\n"
                "Compra aquí: https://www.farmalisto.com.mx/dolor-de-cabeza"
            ),
            "Baja glucosa": (
                "Sugerencia:\n"
                "- Toma jugo de naranja o come caramelos\n"
                "- Glucosa en tabletas (si disponible)\n\n"
                "Compra aquí: https://www.farmalisto.com.mx/glucosa"
            ),
            "Dolor de articulaciones": (
                "Medicamentos sugeridos:\n"
                "- Ibuprofeno 400mg (cada 8h)\n"
                "- Naproxeno (alternativa si persiste)\n"
                "- Gel antiinflamatorio (uso local)\n\n"
                "Compra aquí: https://www.farmalisto.com.mx/articulaciones"
            ),
            "Deshidratación": (
                "Recomendaciones:\n"
                "- Beber suero oral o agua con electrolitos\n"
                "- Vida Suero Oral (cada 6h)\n\n"
                "Compra aquí: https://www.farmalisto.com.mx/suero-oral"
            ),
            "Visión borrosa": (
                "Recomendación:\n"
                "- Acude a un oftalmólogo para diagnóstico\n"
                "- Evita automedicación sin receta\n\n"
                "Consulta opciones: https://www.farmalisto.com.mx"
            ),
            "Dolores Crónicos": (
                "Medicamentos sugeridos para Dolores Crónicos:\n"
                "- Naproxeno 500mg (cada 12h)\n"
                "- Paracetamol (en combinación con otros fármacos)\n\n"
                "Compra aquí: https://www.farmalisto.com.mx/dolores-cronicos"
            ),
        }
        
        # Responder con la solución para el síntoma seleccionado
        if text in soluciones:
            await update.message.reply_text(soluciones[text])

    else:
        await update.message.reply_text("Por favor selecciona una opción válida.")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_response))
    print("Bot iniciado.")
    app.run_polling()

if __name__ == "__main__":
    main()
