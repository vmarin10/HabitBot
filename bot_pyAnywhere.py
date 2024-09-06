import logging
import nest_asyncio
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Configurar el logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

# Definir el comando /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('¡Hola! Soy tu bot de Telegram.')

# Definir el comando /help
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Usa /start para comenzar.')

async def main() -> None:
    # Leer el token desde el archivo token.txt
    with open('token.txt', 'r') as file:
        token = file.read().strip()

    # Crear la aplicación y pasarle el token
    application = ApplicationBuilder().token(token).build()

    # Añadir manejadores de comandos
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))

    # Iniciar el bot
    application.run_polling()

if __name__ == '__main__':
    nest_asyncio.apply()
    asyncio.run(main())
