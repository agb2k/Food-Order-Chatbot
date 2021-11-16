import requests
import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context.

def start(update: Update, context: CallbackContext) -> None:
    """Echo the user message."""
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Hi {user.mention_markdown_v2()}\! Send me a command to get started\!',
    )


def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('/order - Order dishes\n/menu - See menu\n')


def order_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /order is issued."""
    update.message.reply_text('What would you like to order?')

    orderInfo = {
        "data":
            {
                "Item": "29",
                "Delivery": "Yes",
                "Telegram ID": "agb2k"
            }
    }

    if 14 <= int(orderInfo["data"]["Item"]) <= 32:
        sheetId = 20527

    r = requests.post(f"https://api.apispreadsheets.com/data/{sheetId}/", headers={}, json=orderInfo)

    if r.status_code == 201:
        update.message.reply_text('Order successful!')
    else:
        update.message.reply_text("ERROR!")


def menu_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /menu is issued."""
    context.bot.sendDocument(update.effective_chat.id, document=open("FreeLoadersMenu.pdf", 'rb'),
                             caption=f'Here\'s our menu!')


def main() -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater("2120331172:AAFbAfLx8V-deJIcyIfd_OJ6NbM1pBqrRAI")

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("order", order_command))
    dispatcher.add_handler(CommandHandler("menu", menu_command))

    # on non command i.e message - echo the message on Telegram
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, start))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
