import json
import schedule
import time
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Configura tu token de Telegram aquí
TELEGRAM_TOKEN = '7430232048:AAGplwh3W5C6l3ztaC1qR984gG6z9XNa0RQ'

# Cargar hábitos desde el archivo JSON
def load_habits():
    try:
        with open('habits.json', 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

# Guardar hábitos en el archivo JSON
def save_habits(habits):
    with open('habits.json', 'w') as file:
        json.dump(habits, file, indent=4)

# Añadir un hábito nuevo
def add_habit(habit_name):
    habits = load_habits()
    habits.append({
        "name": habit_name,
        "completed": False
    })
    save_habits(habits)

# Marcar un hábito como completado
def complete_habit(habit_name):
    habits = load_habits()
    for habit in habits:
        if habit["name"] == habit_name:
            habit["completed"] = True
            break
    save_habits(habits)

# Verificar estado de los hábitos
def check_habits():
    habits = load_habits()
    for habit in habits:
        if not habit["completed"]:
            print(f"¡No has completado el hábito: {habit['name']}!")
        else:
            print(f"Hábito completado: {habit['name']}")
    # Resetear el estado de completado diariamente
    reset_habits()

# Resetear los hábitos
def reset_habits():
    habits = load_habits()
    for habit in habits:
        habit["completed"] = False
    save_habits(habits)

# Comando de inicio del bot
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("¡Hola! Soy tu bot de seguimiento de hábitos. Usa /add para añadir un hábito.")

# Comando para añadir un hábito desde Telegram
async def add(update: Update, context: ContextTypes.DEFAULT_TYPE):
    habit_name = ' '.join(context.args)
    if habit_name:
        add_habit(habit_name)
        await update.message.reply_text(f"Hábito '{habit_name}' añadido.")
    else:
        await update.message.reply_text("Por favor, proporciona el nombre del hábito con /add nombre_hábito.")

# Comando para ver los hábitos
async def view(update: Update, context: ContextTypes.DEFAULT_TYPE):
    habits = load_habits()
    message = "Tus hábitos:\n" + "\n".join([f"- {habit['name']}: {'Completado' if habit['completed'] else 'No completado'}" for habit in habits])
    await update.message.reply_text(message)

# Inicializar y correr el bot
async def main():
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    # Añadir handlers de comandos
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("add", add))
    application.add_handler(CommandHandler("view", view))

    # Comienza el polling del bot
    await application.run_polling()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except RuntimeError as e:
        if str(e) == 'This event loop is already running':
            # Si el event loop ya está corriendo, ejecuta main en el loop actual
            loop = asyncio.get_event_loop()
            loop.run_until_complete(main())
        else:
            raise
