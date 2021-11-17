import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from datetime import datetime
import gspread

# Logging for potential error handling
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

sa = gspread.service_account(filename="service_account.json")

try:
    sheet = sa.open("Orders")

    malaySheet = sheet.worksheet("Malay")
    mamakSheet = sheet.worksheet("Mamak")
    beverageSheet = sheet.worksheet("Beverage")
    koreanSheet = sheet.worksheet("Korean")
    japaneseSheet = sheet.worksheet("Japanese")

    print(f"Successfully connected to {sheet.title} Google Sheets")
except ConnectionError:
    print("ERROR: Google Sheets Connection Error")


def start(update: Update, context: CallbackContext) -> None:
    """The default message that takes place when user sends a message"""
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Hi {user.mention_markdown_v2()}\! Send me a command to get started\! Use /help to check them out\.',
    )


def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('List of commands:\n/order - Order dishes\n/menu - See menu\n')


def order_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /order is issued."""
    user = update.effective_user.username

    try:
        item = context.args[0]
        room = context.args[1]

        orderInfo = [int(item), room, user, str(datetime.now().strftime('%H:%M:%S')),
                     str(datetime.now().strftime('%d/%m/%y'))]

        if 1 <= int(item) <= 13:
            malaySheet.append_row(orderInfo)
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=f"Order successful! Item No. {item} will be sent to {room} for {user} from the Malay Stall"
            )
        elif 14 <= int(item) <= 32:
            mamakSheet.append_row(orderInfo)
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=f"Order successful! Item No. {item} will be sent to {room} for {user} from the Mamak Stall"
            )
        elif 33 <= int(item) <= 47:
            beverageSheet.append_row(orderInfo)
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=f"Order successful! Item No. {item} will be sent to {room} for {user} from the Beverage Stall"
            )
        elif 48 <= int(item) <= 62:
            koreanSheet.append_row(orderInfo)
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=f"Order successful! Item No. {item} will be sent to {room} for {user} from the Korean Stall"
            )
        elif 63 <= int(item) <= 87:
            japaneseSheet.append_row(orderInfo)
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=f"Order successful! Item No. {item} will be sent to {room} for {user} from the Japanese Stall"
            )
        else:
            update.message.reply_text("Incorrect Order Number! Please Try Again")

    except:
        update.message.reply_text(
            f'What would you like to order?\nUse /order [Order ID] [Delivery(Room No.)] to make an order\neg. /order '
            f'29 J3B10')


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

    # on non-commands
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, start))

    # Start the Bot
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
