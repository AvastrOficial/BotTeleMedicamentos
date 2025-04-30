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
        ["Dificultad para concentrarse", "Orina espumosa o cambios en la frecuencia urinaria"],
        ["Náuseas y vómitos", "Pérdida de apetito"]
    ],
    "Hipertensión": [
        ["Dolor de cabeza", "Mareos"],
        ["Visión borrosa", "Zumbido en los oídos"],
        ["Dolor en el pecho", "Dificultad para respirar"],
        ["Sangrado nasal", "En casos severos"]
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

# Teclado para enfermedades
keyboard_enfermedades = [
    ["Diabetes", "Enfermedades Renales"],
    ["Hipertensión", "Descalcificación Ósea"],
    ["Dolores Crónicos", "Enfermedades Cardiovasculares"]
]

# Teclado para síntomas
keyboard_problemas = [
    ["Sed excesiva", "Micción frecuente"],
    ["Hambre constante", "Pérdida de peso sin causa aparente"],
    ["Visión borrosa", "Fatiga"],
    ["Heridas que tardan en sanar"]
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

    elif text in ["Sed excesiva", "Micción frecuente", "Hambre constante", "Pérdida de peso sin causa aparente", "Visión borrosa", "Fatiga", "Heridas que tardan en sanar", "Fatiga extrema", "Hinchazón en piernas, tobillos o pies", "Dificultad para concentrarse", "Orina espumosa", "Náuseas y vómitos", "Pérdida de apetito", "Dolor de cabeza", "Mareos", "Dolor en el pecho", "Dificultad para respirar", "Sangrado nasal", "Postura encorvada", "Fracturas óseas frecuentes", "Cansancio o fatiga", "Alteraciones del sueño", "Dificultad para moverse", "Ansiedad o depresión", "Palpitaciones", "Mareos o desmayos"]:
        # Mostrar soluciones dependiendo del síntoma
        soluciones = {
            "Sed excesiva": (
                "Mantén una hidratación adecuada.\n"
                "Recomendación: Beber entre 1.5 y 2 litros de agua al día.\n"
                "Consulta más detalles: https://www.amazon.com/s?k=botellas+de+agua"
            ),
            "Micción frecuente": (
                "Controla los niveles de glucosa en sangre.\n"
                "Consulta con un endocrinólogo para ajustes en tratamiento.\n"
                "Compra aquí: https://www.amazon.com/s?k=glucometro"
            ),
            "Hambre constante": (
                "Come en porciones pequeñas y frecuentes.\n"
                "Consulta con un nutricionista para mejorar tu dieta.\n"
                "Compra aquí: https://www.amazon.com/s?k=snacks+saludables"
            ),
            "Pérdida de peso sin causa aparente": (
                "Consulta con un endocrinólogo para ajustes en tratamiento.\n"
                "Realiza exámenes para verificar tu salud general.\n"
                "Compra aquí: https://www.amazon.com/s?k=examenes+de+salud"
            ),
            "Visión borrosa": (
                "Controla niveles de glucosa.\n"
                "Consulta al oftalmólogo si los problemas persisten.\n"
                "Compra aquí: https://www.amazon.com/s?k=lentes+para+diabetes"
            ),
            "Fatiga": (
                "Mantén niveles estables de glucosa y descanso.\n"
                "Consulta con un médico para verificar otras causas.\n"
                "Compra aquí: https://www.amazon.com/s?k=supplements+for+fatigue"
            ),
            "Heridas que tardan en sanar": (
                "Consulta a un médico para un control adecuado de glucosa.\n"
                "Mantén una higiene adecuada en las heridas.\n"
                "Compra aquí: https://www.amazon.com/s?k=productos+para+heridas"
            ),
            "Fatiga extrema": (
                "Lleva una dieta balanceada y consulta a un médico.\n"
                "Descansa adecuadamente para mejorar tu energía.\n"
                "Compra aquí: https://www.amazon.com/s?k=vitaminas+para+fatiga"
            ),
            "Hinchazón en piernas, tobillos o pies": (
                "Usa diuréticos y eleva las piernas.\n"
                "Consulta con un médico para tratamiento adecuado.\n"
                "Compra aquí: https://www.amazon.com/s?k=medias+de+compresion"
            ),
            "Dificultad para concentrarse": (
                "Seguir tratamiento médico y descansar lo necesario.\n"
                "Consulta con un neurólogo si la dificultad persiste.\n"
                "Compra aquí: https://www.amazon.com/s?k=suplementos+para+concentracion"
            ),
            "Orina espumosa": (
                "Realizar pruebas de función renal.\n"
                "Consulta con un médico para tratamiento adecuado.\n"
                "Compra aquí: https://www.amazon.com/s?k=examenes+de+funcion+renal"
            ),
            "Náuseas y vómitos": (
                "Consulta al médico para control de electrolitos.\n"
                "Mantén una dieta suave mientras te recuperas.\n"
                "Compra aquí: https://www.amazon.com/s?k=suero+oral"
            ),
            "Pérdida de apetito": (
                "Come porciones pequeñas y equilibradas.\n"
                "Consulta con un nutricionista para plan de alimentación.\n"
                "Compra aquí: https://www.amazon.com/s?k=suplementos+nutricionales"
            ),
            # Agrega las demás soluciones siguiendo el mismo formato
        }

        respuesta = soluciones.get(text, "No se encontró una solución para este síntoma.")
        await update.message.reply_text(respuesta)
        
def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_response))
    print("Bot iniciado.")
    app.run_polling()

if __name__ == "__main__":
    main()
