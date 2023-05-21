import logging
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

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
) = range(10)

user_info = {}


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
        f"{update.message.text}, write the surname in English as indicated in the international passport.",
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
        "Please enter your valid email. It will be needed by the tax service to send informational messages."
    )

    return EMAIL


async def email(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_info["email"] = update.message.text
    await update.message.reply_text(
        "Please introduce yourself \n\n"
        f"{user_info['name']}, Write your Georgian phone number. The format should be: +995XXXXXXXXX"
    )

    return PHONE_NUM 


async def phone_num(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_info["phone_num"] = update.message.text
    reply_keyboard = [["$25/Monthly", "$240/Annual", "I’m corporative client"]]

    await update.message.reply_text(
        "Super! \n\n" f"{user_info['name']} Choose iolipay service package",
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True),
    )

    return PACKAGE_PLAN


async def package_plan(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_info["package_plan"] = update.message.text
    await update.message.reply_text(
        "Cool! \n\n"
        "Now I will register you in the system of the tax service of Georgia. I will need information about your registration as an individual entrepreneur.\n"
        "Enter the Georgian Tax Identification Number of Individual Entrepreneur. This is a 9-digit code indicated in the IP registration certificate"
    )

    return TAX_NUM


async def tax_num(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_info["tax_num"] = update.message.text
    await update.message.reply_text(
        "Good!\n\n"
        "Now enter the address that was used to register the status of an individual entrepreneur in Georgia"
    )

    return ADDRESS


async def address(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_info["address"] = update.message.text
    await update.message.reply_text(
        "Wonderful. There is very little left.\n"
        "Now you need to find the following information in the received sms from [rs.ge](http://rs.ge/) and enter rs username"
    )

    return RS_USERNAME


async def rs_username(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_info["rs_username"] = update.message.text
    await update.message.reply_text("And also write rs.ge password")

    return RS_PASSWORD


async def rs_password(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_info["rs_password"] = update.message.text
    await update.message.reply_text(
        "Super!\n And the final question:" "Write the type of your business activity."
    )

    return BUSINESS_ACTIVITY


async def final(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_info["business_activity"] = update.message.text
    await update.message.reply_text(
        "Great!\n\n"
        "Name, your registration has been successfully completed.\n"
        "When the time comes for filing the declaration and tax, I will write to you in this chat. Paying the tax and filing the declaration will take no more than 3 minutes. See you later 🤗"
    )

    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancels and ends the conversation."""
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    await update.message.reply_text(
        f"{user_info}"
        # "Bye! I hope we can talk again some day.", reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END


def main() -> None:
    """Run the bot."""
    # Create the Application and pass it your bot's token.
    application = (
        Application.builder()
        .token("6218070919:AAHstt8R7Up10t5S2RtkWXWJEnJ2g889C8o")
        .build()
    )

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            NAME: [MessageHandler(filters.TEXT, name)],
            SURNAME: [MessageHandler(filters.TEXT, surname)],
            EMAIL: [MessageHandler(filters.TEXT, email)],
            PHONE_NUM: [MessageHandler(filters.TEXT, phone_num)],
            PACKAGE_PLAN: [MessageHandler(filters.TEXT, package_plan)],
            TAX_NUM: [MessageHandler(filters.TEXT, tax_num)],
            ADDRESS: [MessageHandler(filters.TEXT, address)],
            RS_USERNAME: [MessageHandler(filters.TEXT, rs_username)],
            RS_PASSWORD: [MessageHandler(filters.TEXT, rs_password)],
            BUSINESS_ACTIVITY: [MessageHandler(filters.TEXT, final)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    application.add_handler(conv_handler)

    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()
