import logging
import subprocess
from telegram import Update, ParseMode
from telegram.ext import Updater, CommandHandler, CallbackContext
import asyncio
from aiohttp import web

# Configure logging
logging.basicConfig(
    filename='logs.txt',  # Log output file
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

LOGGER = logging.getLogger(__name__)

# Function to handle the /logs command
def logs_command(update: Update, context: CallbackContext) -> None:
    try:
        with open('logs.txt', 'r') as log_file:
            logs = log_file.read()

        # Send logs in code block format
        update.message.reply_text(f'```logs\n{logs}\n```', parse_mode='MarkdownV2')

    except FileNotFoundError:
        update.message.reply_text('No logs found.')

# Function to handle the start command
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Hello! To Use contact @yukiLOGS')

# Function to handle the /sh command and execute shell commands
def shell(update: Update, context: CallbackContext):
    message = update.effective_message
    cmd = message.text.split(" ", 1)
    
    if len(cmd) == 1:
        message.reply_text("No command to execute was given.")
        return
    
    cmd = cmd[1]
    process = subprocess.Popen(
        cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True
    )
    stdout, stderr = process.communicate()
    
    reply = ""
    stderr = stderr.decode()
    stdout = stdout.decode()
    
    if stdout:
        reply += f"*Stdout*\n`{stdout}`\n"
        LOGGER.info(f"Shell - {cmd} - {stdout}")
    
    if stderr:
        reply += f"*Stderr*\n`{stderr}`\n"
        LOGGER.error(f"Shell - {cmd} - {stderr}")
    
    # Check if the reply length is too long
    if len(reply) > 3000:
        with open("shell_output.txt", "w") as file:
            file.write(reply)
        
        with open("shell_output.txt", "rb") as doc:
            context.bot.send_document(
                document=doc,
                filename=doc.name,
                reply_to_message_id=message.message_id,
                chat_id=message.chat_id,
            )
    else:
        message.reply_text(reply, parse_mode=ParseMode.MARKDOWN)

async def web_server():
    # Sample async web server setup
    async def handle(request):
        return web.Response(text="Web server is running!")

    app = web.Application()
    app.add_routes([web.get('/', handle)])
    return app

async def start_web_server():
    # Start the web server on port 8000
    app = await web_server()
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", 8000)
    await site.start()

def main():
    # Replace '7863196804:AAHLuwSibBQf4denufOtuflKDinvzHgRfDw' with your actual bot token
    updater = Updater("7863196804:AAHLuwSibBQf4denufOtuflKDinvzHgRfDw", use_context=True)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Add handlers for commands
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("logs", logs_command))
    dispatcher.add_handler(CommandHandler("sh", shell))

    # Start the Bot
    updater.start_polling()

    # Start the web server asynchronously
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start_web_server())

    # Keep the bot running
    updater.idle()

if __name__ == '__main__':
    main()