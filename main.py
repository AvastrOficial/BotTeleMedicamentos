from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = input("Introduce el token del bot de Telegram: ")

keyboard_enfermedades = [["Diabetes", "Enfermedades Renales"], ["Hipertensión", "Otros"]]
keyboard_problemas = [["Insomnio", "Mareo"], ["Visión borrosa", "Dolor de cabeza"], ["Baja glucosa", "Dolor de articulaciones", "Deshidratación"]]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reply_keyboard = [["Sí", "No"]]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, resize_keyboard=True)
    await update.message.reply_text("¿Tienes una enfermedad crónico o degenerativa?", reply_markup=markup)

async def handle_response(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if text == "Sí":
        markup = ReplyKeyboardMarkup(keyboard_enfermedades, one_time_keyboard=True, resize_keyboard=True)
        await update.message.reply_text("Selecciona tu enfermedad:", reply_markup=markup)
    elif text == "No":
        await update.message.reply_text("Gracias por tu respuesta. ¡Cuídate!")
    elif text == "Diabetes":
        await update.message.reply_text(
            "Medicamentos sugeridos para Diabetes:\n"
            "- Metformina 850mg (1 o 2 veces al día según peso > 70kg)\n"
            "- Insulina NPH o Glargina (según indicación médica)\n"
            "- Glibenclamida (solo si no hay riesgo de hipoglucemia)\n\n"
            "Compra aquí: https://www.farmalisto.com.mx/diabetes"
        )
    elif text == "Enfermedades Renales":
        await update.message.reply_text(
            "Medicamentos sugeridos para Enfermedades Renales:\n"
            "- Furosemida 40mg (1 cada 12h si retención de líquidos)\n"
            "- Captopril 25mg (si hay presión alta)\n"
            "- Eritropoyetina (en casos avanzados de insuficiencia renal)\n\n"
            "Compra aquí: https://www.farmalisto.com.mx/medicamentos/uso-renal"
        )
    elif text == "Hipertensión":
        await update.message.reply_text(
            "Medicamentos sugeridos para Hipertensión:\n"
            "- Enalapril 10mg (1 diaria, aumentar si presión > 140/90)\n"
            "- Losartán 50mg (mejor si peso > 80kg)\n"
            "- Hidroclorotiazida (en combinación si hay retención)\n\n"
            "Compra aquí: https://www.farmalisto.com.mx/hipertension"
        )
    elif text == "Otros":
        markup = ReplyKeyboardMarkup(keyboard_problemas, one_time_keyboard=True, resize_keyboard=True)
        await update.message.reply_text("¿Qué problema tienes?", reply_markup=markup)
    else:
        problemas = {
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
            "Visión borrosa": (
                "Recomendación:\n"
                "- Acude a un oftalmólogo para diagnóstico\n"
                "- Evita automedicación sin receta\n\n"
                "Consulta opciones: https://www.farmalisto.com.mx"
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
            )
        }

        if text in problemas:
            await update.message.reply_text(problemas[text])

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_response))
    print("Bot iniciado.")
    app.run_polling()

if __name__ == "__main__":
    main()
