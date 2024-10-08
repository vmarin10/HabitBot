import logging
import nest_asyncio
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

# Configurar el logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

habits = []

# Definir el comando /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('¡Hola! Soy tu bot de hábitos. Usa /add_habit para añadir un hábito.')

# Definir el comando /help
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Usa /add_habit para añadir un hábito.')

# Definir el comando /add_habit
async def add_habit(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    habit = ' '.join(context.args)
    habits.append(habit)
    await update.message.reply_text(f'Hábito añadido: {habit}')

# Función para enviar notificaciones
async def send_notification(context: ContextTypes.DEFAULT_TYPE) -> None:
    for habit in habits:
        await context.bot.send_message(chat_id=context.job.context, text=f'Recordatorio: {habit}')

async def main() -> None:
    # Leer el token desde el archivo token.txt
    with open('token.txt', 'r') as file:
        token = file.read().strip()

    # Crear la aplicación y pasarle el token
    application = ApplicationBuilder().token(token).build()

    # Añadir manejadores de comandos
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("add_habit", add_habit))

    # Configurar el scheduler
    scheduler = AsyncIOScheduler()
    scheduler.add_job(send_notification, CronTrigger(hour=10, minute=0), context=application.bot)
    scheduler.start()

    # Iniciar el bot
    application.run_polling()

if __name__ == '__main__':
    nest_asyncio.apply()
    asyncio.run(main())
