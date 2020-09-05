from telegram import Bot
from telegram import Update
from telegram import InlineKeyboardButton
from telegram import InlineKeyboardMarkup
from telegram.ext import CallbackContext
from telegram.ext import Updater
from telegram.ext import MessageHandler
from telegram.ext import CommandHandler
from telegram.ext import Filters
from telegram.ext import CallbackQueryHandler

import string
import random

PASS_LEN = 8
EXIT_BUTTON = "exit_button"
GENERATE_PASS_AGAIN_BUTTON = "generate_pass_again_button"

def logger(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print("Error :: {}".format(e))
            raise e
    return inner

def isDigit(input):
    res = True
    try:
        digit = int(input)
        if digit <= 0:
            raise ValueError
    except ValueError:
        res = False
    return res


def generate_password(length):
    chars = string.ascii_letters + string.punctuation + string.digits
    return ''.join(random.choice(chars) for x in range(int(length)))


@logger
def generate_password_handler(update: Update, context: CallbackContext):
    try:
        global PASS_LEN
        if update.message.text is None:
            user_input = PASS_LEN
        else:
            user_input = context.args[0]
        if isDigit(user_input):
            PASS_LEN = user_input
            password = generate_password(user_input)
            if(int(user_input) >= 8):
                update.message.reply_text("There is your password : {0} \nKeep it on secret, bro \U0001F64A".format(password), reply_markup=get_inline_keybord())
            else:
                update.message.reply_text("There is your password : {0}\nIt`s not strong enough - add at least 8 charactes ".format(password))
        else:
            update.message.reply_text("No.. input is not a  non-negative integer \U0001F631 \nTry again)")
    except Exception:
        update.message.reply_text("Invalid command format \U0001F601 \nE.g :: /generate 2")

def get_inline_keybord():
    keybord = [
        [
            InlineKeyboardButton(text= "This pass is OK 💫", callback_data = EXIT_BUTTON),
            InlineKeyboardButton(text= "Another one ⚒", callback_data = GENERATE_PASS_AGAIN_BUTTON)
        ]
    ]
    return InlineKeyboardMarkup(keybord)


def keybord_callback_handller(update: Update, context: CallbackContext):
    query = update.callback_query
    data = query.data
    if data == EXIT_BUTTON:
        current_text = update.effective_message.text
        query.edit_message_text(
            text = current_text
        )
    elif data == GENERATE_PASS_AGAIN_BUTTON:
        query.message.reply_text("Maybe this one would be great? \n" + generate_password(PASS_LEN), reply_markup = get_inline_keybord())

def info_handler(update: Update, context:CallbackContext):
    update.message.reply_text("Created by Oleh Andrus for those who always not well at password generation. Like me \U0001F440")

def message_handler(update: Update, context:CallbackContext):
    update.message.reply_text("Welcome to the PGB - password generator bot. \n Take a look to the command menu! \n Good luck \U0001F49A")

def main():
    
    _bot = Bot(token="There should be your token generated at BotFather")
    
    updater = Updater(
        bot=_bot,
        use_context=True
    )

    updater.dispatcher.add_handler(CommandHandler(command="generate", callback=generate_password_handler, pass_args=True))
    updater.dispatcher.add_handler(CommandHandler(command="info", callback=info_handler))
    updater.dispatcher.add_handler(CallbackQueryHandler(callback= keybord_callback_handller, pass_chat_data=True))
    updater.dispatcher.add_handler(MessageHandler(filters = Filters.text, callback=message_handler))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()