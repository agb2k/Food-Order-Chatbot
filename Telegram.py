# Importing the relevent libraries
import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from datetime import datetime
import gspread

# Logging for potential error handling
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Checks if connection to Google Sheets API is possible
try:
    # Connecting to google sheets api
    serviceAccount = gspread.service_account(filename="service_account.json")

    # Connecting to google sheet
    sheet = serviceAccount.open("Orders")

    # Selecting worksheets
    malaySheet = sheet.worksheet("Malay")
    mamakSheet = sheet.worksheet("Mamak")
    beverageSheet = sheet.worksheet("Beverage")
    koreanSheet = sheet.worksheet("Korean")
    japaneseSheet = sheet.worksheet("Japanese")
    commentSheet = sheet.worksheet("Comments")

    print(f"Successfully connected to {sheet.title} Google Sheets")
#     Error handling
except ConnectionError:
    print("ERROR: Google Sheets Connection Error")


# The default message that takes place when user sends a message
def start(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Hi {user.mention_markdown_v2()}\! Send me a command to get started\! Use /help to check them out\.',
    )


# Send a message when the command /help is issued.
def help_command(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(
        'List of commands:\n/order - Order dishes\n/menu - See menu\n/contact - Get help from someone\n/comment - '
        'Give us your constructive criticism')


# Bot sends a message when the command /menu is issued.
def menu_command(update: Update, context: CallbackContext) -> None:
    context.bot.sendDocument(update.effective_chat.id,
                             document=open("FreeLoadersMenu.pdf", 'rb'), caption=f'Here\'s our menu!')


# Bot sends a message when the command /contact is issued.
def contact_command(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Chatbot Creator - abhinav.basil@gmail.com\nCampus Services - '
                              'campus.services@nottingham.edu.my')


# Bot sends a message when the command /comment is issued
def comment_command(update: Update, context: CallbackContext) -> None:
    # Turns messages into string
    comment = str(' '.join(context.args))

    # /comment command logic to add to google sheets
    if comment:
        try:
            commentSheet.append_row([comment])
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text=f"Your comment has been submitted. Thank you!")
        except:
            update.message.reply_text("ERROR: Issue Appending")
    else:
        update.message.reply_text(
            "Submit your anonymous comment by using the command, /comment, followed by your comment.\neg. /comment "
            "The creator of this bot is awesome!")


# Bot sends a message when the command /order is issued
def order_command(update: Update, context: CallbackContext) -> None:
    # Telegram user
    user = update.effective_user.username

    # Adds the corresponding detail to the sheets
    # Takes place if /order xx xx is entered
    try:
        item = context.args[0]
        room = context.args[1]

        # Array to
        orderInfo = [int(item), room, user, str(datetime.now().strftime('%H:%M:%S')),
                     str(datetime.now().strftime('%d/%m/%y'))]

        # Selecting which sheet to add the details into
        if 1 <= int(item) <= 13:
            malaySheet.append_row(orderInfo)
        elif 14 <= int(item) <= 32:
            mamakSheet.append_row(orderInfo)
        elif 33 <= int(item) <= 47:
            beverageSheet.append_row(orderInfo)
        elif 48 <= int(item) <= 62:
            koreanSheet.append_row(orderInfo)
        elif 63 <= int(item) <= 87:
            japaneseSheet.append_row(orderInfo)

        # Error handling
        if 1 > int(item) > 87:
            update.message.reply_text("Incorrect Order Number! Please Try Again")
        else:
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=f"Order successful! Item No. {item} will be sent to {room} for {user}"
            )

    #Takes place if just /order is entered
    except:
        update.message.reply_text(
            f'What would you like to order?\nUse /order [Order ID] [Delivery(Room No.)] to make an order\neg. /order '
            f'29 J3B10')


# Starts the telegram bot
def main() -> None:
    # Create the Updater and pass it your bot's token.
    # This should be a secret but it's left open for demo/testing purposes
    updater = Updater("2120331172:AAFbAfLx8V-deJIcyIfd_OJ6NbM1pBqrRAI")

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Different commands
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("order", order_command))
    dispatcher.add_handler(CommandHandler("menu", menu_command))
    dispatcher.add_handler(CommandHandler("contact", contact_command))
    dispatcher.add_handler(CommandHandler("comment", comment_command))

    # Non-commands
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, start))

    # Start the Bot
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
