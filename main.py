import logging
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
)
import os
from dotenv import load_dotenv
from datetime import datetime


load_dotenv()



# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

(
    NAME,
    SURNAME,
    EMAIL,
    PHONE_NUM,
    PACKAGE_PLAN,
    TAX_NUM,
    ADDRESS,
    RS_USERNAME,
    RS_PASSWORD,
    BUSINESS_ACTIVITY,
    SUBMIT_INFO,
) = range(11)


(
    CALENDAR_DATE,
    CURRENCY,
    AMOUNT
) = range(3)



user_info = {}
transaction_info = {}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Starts the conversation and asks the user about their gender."""

    await update.message.reply_text(
        "Please introduce yourself, Write the name in English as indicated in the international passport.",
        reply_markup=ReplyKeyboardRemove(),
    )

    return NAME


async def name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the selected nameand asks for a surname."""
    user = update.message.from_user
    user_info["name"] = update.message.text
    logger.info("Name of %s: %s", user.first_name, update.message.text)
    await update.message.reply_text(
        "Super! \n\n"
        f"{update.message.text}, write the surname in English as indicated in the international passport. \n\n"
        "(/cancel to cancel conversation)",
        reply_markup=ReplyKeyboardRemove(),
    )

    return SURNAME


async def surname(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the photo and asks for a location."""
    user = update.message.from_user
    user_info["surname"] = update.message.text
    logger.info("Surname of %s: %s", user.first_name, update.message.text)
    await update.message.reply_text(
        "Wonderful! \n\n"
        "Please enter your valid email. It will be needed by the tax service to send informational messages.\n\n"
        "(/cancel to cancel conversation)"
    )

    return EMAIL


async def email(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_info["email"] = update.message.text
    await update.message.reply_text(
        "Please introduce yourself \n\n"
        f"{user_info['name']}, Write your Georgian phone number. The format should be: +995XXXXXXXXX\n\n"
        "(/cancel to cancel conversation)"
    )

    return PHONE_NUM


async def phone_num(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_info["phone_num"] = update.message.text
    reply_keyboard = [["$25/Monthly", "$240/Annual", "I'm corporative client"]]

    await update.message.reply_text(
        "Super! \n\n"
        f"{user_info['name']} Choose iolipay service package\n\n"
        "(/cancel to cancel conversation)",
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True),
    )

    return PACKAGE_PLAN


async def package_plan(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_info["package_plan"] = update.message.text
    await update.message.reply_text(
        "Cool! \n\n"
        "Now I will register you in the system of the tax service of Georgia. I will need information about your registration as an individual entrepreneur.\n"
        "Enter the Georgian Tax Identification Number of Individual Entrepreneur. This is a 9-digit code indicated in the IP registration certificate\n\n"
        "(/cancel to cancel conversation)"
    )

    return TAX_NUM


async def tax_num(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_info["tax_num"] = update.message.text
    await update.message.reply_text(
        "Good!\n\n"
        "Now enter the address that was used to register the status of an individual entrepreneur in Georgia\n\n"
        "(/cancel to cancel conversation)"
    )

    return ADDRESS


async def address(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_info["address"] = update.message.text
    await update.message.reply_text(
        "Wonderful. There is very little left.\n"
        "Now you need to find the following information in the received sms from [rs.ge](http://rs.ge/) and enter rs username\n\n"
        "(/cancel to cancel conversation)"
    )

    return RS_USERNAME


async def rs_username(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_info["rs_username"] = update.message.text
    await update.message.reply_text(
        "And also write rs.ge password\n\n" "(/cancel to cancel conversation)"
    )

    return RS_PASSWORD


async def rs_password(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_info["rs_password"] = update.message.text
    await update.message.reply_text(
        "Super!\n And the final question:"
        "Write the type of your business activity.\n\n"
        "(/cancel to cancel conversation)"
    )

    return BUSINESS_ACTIVITY


async def submit_info(update: Update, contet: ContextTypes.DEFAULT_TYPE):
    user_info["business_activity"] = update.message.text
    reply_keyboard = [["Yes", "No"]]
    await update.message.reply_text(
        "Is this correct information? \n\n"
        f"""
            Name: {user_info['name']}   
            Surname: {user_info['surname']}   
            Email: {user_info['email']}   
            Phone Number: {user_info['phone_num']}   
            Package Plan: {user_info['package_plan']}   
            Tax Number: {user_info['tax_num']}   
            Address: {user_info['address']}   
            RS Username: {user_info['rs_username']}   
            RS Password: {user_info['rs_password']}   
            Business Activity: {user_info['business_activity']}   
        """,
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True),
    )

    return SUBMIT_INFO


async def final(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "Yes":
        await update.message.reply_text(
            "Great!\n\n"
            f"{user_info['name']}, your registration has been successfully completed.\n"
            "When the time comes for filing the declaration and tax, I will write to you in this chat. Paying the tax and filing the declaration will take no more than 3 minutes. See you later 🤗\n\n"
        )
    else:
        await update.message.reply_text(
            "If your info isn't correct please /start again"
        )

    return ConversationHandler.END



async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancels and ends the conversation."""
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    await update.message.reply_text(
        "Bye! I hope we can talk again some day. \n\n (/start to start conversation)",
        reply_markup=ReplyKeyboardRemove(),
    )

    return ConversationHandler.END


async def transaction_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(
        "It's time to pay taxes and file returns. This will take three minutes.\n"
        "Fill in the information on the income of the reporting (previous) month, from the 1st day including the last.\n"
        "Please note that you should not include personal transfers, personal deposits or other personal transactions in your monthly income.\n"
        "Please write a date of transaction (format should be YYYY-MM-DD)"
    )

    return CALENDAR_DATE 


async def transaction_date(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    date_string = update.message.text
    try:
        date_object = datetime.strptime(date_string, "%Y-%m-%d")
        transaction_info["date"] = date_object
    except ValueError:
        await update.message.reply_text("You wrote date in wrong format, start again (/transaction)")
        return ConversationHandler.END
    
    keyboard = [
        [
            InlineKeyboardButton("$", callback_data='USD'),
            InlineKeyboardButton("EUR", callback_data='EUR'),
            InlineKeyboardButton("GBP", callback_data='GBP'),
            InlineKeyboardButton("GEL", callback_data='GEL'),
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
 
    await update.message.reply_text("Now choose currency you get your income with\n", reply_markup=reply_markup)

    return CURRENCY 


async def transaction_currency(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    transaction_info['currency'] = query.data
    await query.edit_message_text(f"Enter amount of {transaction_info['currency']} you get")
 
    return AMOUNT 


async def transaction_amount(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    amount = update.message.text
    transaction_info['amount'] = float(amount)

    return ConversationHandler.END



def main() -> None:
    """Run the bot."""
    # Create the Application and pass it your bot's token.
    application = (
        Application.builder()
        .token(os.environ.get('TOKEN'))
        .build()
    )

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, name)],
            SURNAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, surname)],
            EMAIL: [MessageHandler(filters.TEXT & ~filters.COMMAND, email)],
            PHONE_NUM: [MessageHandler(filters.TEXT & ~filters.COMMAND, phone_num)],
            PACKAGE_PLAN: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, package_plan)
            ],
            TAX_NUM: [MessageHandler(filters.TEXT & ~filters.COMMAND, tax_num)],
            ADDRESS: [MessageHandler(filters.TEXT & ~filters.COMMAND, address)],
            RS_USERNAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, rs_username)],
            RS_PASSWORD: [MessageHandler(filters.TEXT & ~filters.COMMAND, rs_password)],
            BUSINESS_ACTIVITY: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, submit_info)
            ],
            SUBMIT_INFO: [MessageHandler(filters.TEXT & ~filters.COMMAND, final)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )


    transaction_conv_handler = ConversationHandler(
        entry_points=[CommandHandler("transaction", transaction_start)],
        states={
            CALENDAR_DATE: [MessageHandler(filters.TEXT & ~filters.COMMAND, transaction_date)],
            CURRENCY: [CallbackQueryHandler(transaction_currency)],
            AMOUNT: [MessageHandler(filters.TEXT & ~filters.COMMAND, transaction_amount)]
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    application.add_handler(conv_handler)
    application.add_handler(transaction_conv_handler)

    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()
