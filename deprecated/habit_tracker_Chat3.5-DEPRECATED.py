import asyncio
from telegram.ext import Application, CommandHandler
import logging

# Token del bot (asegúrate de tener el tuyo aquí)
TELEGRAM_TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'

# Configuración de logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Función de inicio para el bot
async def start(update, context):
    await update.message.reply_text('¡Hola! Soy tu bot de hábitos.')

# Función de ayuda para el bot
async def help_command(update, context):
    await update.message.reply_text('Aquí están los comandos disponibles:\n/start - Inicia el bot\n/help - Muestra esta ayuda')

# Función para añadir un hábito (ejemplo)
async def add_habit(update, context):
    habit = ' '.join(context.args)
    if habit:
        await update.message.reply_text(f'Hábito añadido: {habit}')
    else:
        await update.message.reply_text('Por favor, proporciona el hábito a añadir.')

# Función principal para ejecutar el bot
async def main():
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    # Añadir manejadores de comandos
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('help', help_command))
    application.add_handler(CommandHandler('add_habit', add_habit))

    # Iniciar polling del bot
    await application.run_polling()

# Crear una función para ejecutar el bucle de eventos
def run_bot():
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main())
    except Exception as e:
        logger.error(f"An error occurred: {e}")
    finally:
        loop.close()

# Manejo de errores
if __name__ == '__main__':
    run_bot()
