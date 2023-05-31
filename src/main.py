from telegram.ext import (
    Application,
    CommandHandler,
    ConversationHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
)
import os
from dotenv import load_dotenv

from user import NAME,SURNAME,EMAIL,PHONE_NUM,PACKAGE_PLAN,TAX_NUM,ADDRESS,RS_USERNAME,RS_PASSWORD,BUSINESS_ACTIVITY,SUBMIT_INFO
from user import start,name,surname,email,phone_num,package_plan,tax_num,address,rs_password,rs_username,submit_info,final,cancel
from transaction import CALENDAR_DATE,CURRENCY,AMOUNT,FINAL
from transaction import transaction_start,transaction_date,transaction_currency,transaction_amount,transaction_final,add_transaction

load_dotenv()




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
        entry_points=[CommandHandler("transaction", transaction_start),CommandHandler("add_transaction", add_transaction)],
        states={
            CALENDAR_DATE: [MessageHandler(filters.TEXT & ~filters.COMMAND, transaction_date)],
            CURRENCY: [CallbackQueryHandler(transaction_currency)],
            AMOUNT: [MessageHandler(filters.TEXT & ~filters.COMMAND, transaction_amount)],
            FINAL: [CallbackQueryHandler(transaction_final)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    application.add_handler(conv_handler)
    application.add_handler(transaction_conv_handler)

    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()
