import logging
import re
from db_connection import create_user

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext,
)

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

FIRST_NAME, LAST_NAME, CITY, MAIL, PHONE = range(5)

sessions_data = []


def start(update: Update, _: CallbackContext) -> int:
    sessions_data.append({
        'id': update.message.chat.id,
        'details': {
            'first_name': '',
            'last_name': '',
            'city': '',
            'mail': '',
            'phone': ''
        }
    })

    update.message.reply_text(
        "היי, ברוכים הבאים לצ'אט ההתנדבות של מצעד הגבורה!"
        '\n'
        "אנו שמחים שבחרתם להתנדב ולתרום מזמנכם למטרה נעלה זו."
        '\n'
        "כדי להתחיל אנו זקוקים למספר פרטים."

        '\n\n'
        'שם פרטי:',
    )

    return FIRST_NAME


def validate_name(full_name):
    if len(full_name) < 2:
        return False
    return True


def first_name(update: Update, _: CallbackContext) -> int:
    user = update.message.from_user
    logger.info("first name of %s: %s", user.first_name, update.message.text)
    if not validate_name(update.message.text):
        update.message.reply_text('השם הפרטי קצר מדי או מכיל ספרות. נסה שוב:')
        return FIRST_NAME

    for item in sessions_data:
        if item['id'] == update.message.chat.id:
            item['details']['first_name'] = update.message.text

    update.message.reply_text('שם משפחה:')
    return LAST_NAME


def last_name(update: Update, _: CallbackContext) -> int:
    user = update.message.from_user
    logger.info("last name of %s: %s", user.first_name, update.message.text)
    if not validate_name(update.message.text):
        update.message.reply_text('שם המשפחה קצר מדי או מכיל ספרות. נסה שוב:')
        return last_name

    for item in sessions_data:
        if item['id'] == update.message.chat.id:
            item['details']['last_name'] = update.message.text

    update.message.reply_text('עיר מגורים:')
    return CITY


def validate_address(user_address):
    if len(user_address) < 2:
        return False
    return True


def city(update: Update, _: CallbackContext) -> int:
    user = update.message.from_user
    logger.info("city of %s: %s", user.first_name, update.message.text)

    if not validate_address(update.message.text):
        update.message.reply_text('עיר מגורים:')
        return CITY

    for item in sessions_data:
        if item['id'] == update.message.chat.id:
            item['details']['city'] = update.message.text

    update.message.reply_text('מייל:')
    return MAIL


def validate_mail(mail):
    regex = '^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'
    match = re.search(regex, mail)
    if not match:
        return False
    return True


def mail(update: Update, _: CallbackContext) -> int:
    user = update.message.from_user
    logger.info("mail of %s: %s", user.first_name, update.message.text)

    if not validate_mail(update.message.text):
        update.message.reply_text('המייל אינו תקין. נסה שוב:')
        return MAIL

    for item in sessions_data:
        if item['id'] == update.message.chat.id:
            item['details']['mail'] = update.message.text
    update.message.reply_text('מספר טלפון לחזרה:')
    return PHONE


def validate_phone(phone_number):
    pa = r"^0(?:[234689]|5[0-689]|7[246789])(?![01])(\d{7})$"
    match = re.search(pa, phone_number)
    if not match:
        return False
    return True


def phone(update: Update, _: CallbackContext) -> int:
    not_validate = True
    user = update.message.from_user
    logger.info("phone of %s: %s", user.first_name, update.message.text)
    if not validate_phone(update.message.text):
        update.message.reply_text('נא הכנס מספר טלפון תקין המכיל 10 ספרות')
        return PHONE

    for item in sessions_data:
        if item['id'] == update.message.chat.id:
            item['details']['phone'] = update.message.text
            create_user(item['details'])

    update.message.reply_text('ההרשמה בוצעה בהצלחה. ניצור איתך קשר בהקדם!')
    print(sessions_data)

    return ConversationHandler.END


def cancel(update: Update, _: CallbackContext) -> int:
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text(
        'ההרשמה בוטלה!', reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END


def main() -> None:
    # Create the Updater and pass it your bot's token.
    updater = Updater('1600467511:AAF-u0Y3cehZOnO3R_CxDxw8_6AkWSzsQCc')

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            FIRST_NAME: [MessageHandler(Filters.text & ~Filters.command, first_name)],
            LAST_NAME: [MessageHandler(Filters.text & ~Filters.command, last_name)],
            CITY: [MessageHandler(Filters.text & ~Filters.command, city)],
            MAIL: [MessageHandler(Filters.text & ~Filters.command, mail)],
            PHONE: [MessageHandler(Filters.text & ~Filters.command, phone)]
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    dispatcher.add_handler(conv_handler)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
