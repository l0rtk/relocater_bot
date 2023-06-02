
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ContextTypes,
    ConversationHandler,
)
from dotenv import load_dotenv
from datetime import datetime
import requests


load_dotenv()


(
    CALENDAR_DATE,
    CURRENCY,
    AMOUNT,
    FINAL
) = range(4)


transaction_info = {}
all_transactions = []

def get_currency(date,currency = "USD"):
    req = requests.get(f"https://nbg.gov.ge/gw/api/ct/monetarypolicy/currencies/en/json/?currencies={currency}&date={date}")
    return req.json()


async def transaction_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    global transaction_info 
    global all_transactions

    transaction_info, all_transactions = {}, []

    await update.message.reply_text(
        "It's time to pay taxes and file returns. This will take three minutes.\n"
        "Fill in the information on the income of the reporting (previous) month, from the 1st day including the last.\n"
        "Please note that you should not include personal transfers, personal deposits or other personal transactions in your monthly income.\n"
        "Please write a date of transaction (format should be dd.mm.yyyy)"
    )

    return CALENDAR_DATE 


async def add_transaction(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(
        "Please write a date of transaction (format should be dd.mm.yyyy)"
    )

    return CALENDAR_DATE 



async def transaction_date(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    date_string = update.message.text
    try:
        datetime.strptime(date_string, "%d.%m.%Y")
        transaction_info["date"] = date_string 
    except ValueError:
        await update.message.reply_text("You wrote date in wrong format, start again (/transaction)")
        return ConversationHandler.END
    
    keyboard = [
        [
            InlineKeyboardButton("USD", callback_data='USD'),
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
    if transaction_info['currency'] != 'GEL':
        date = transaction_info['date'].split('.')
        formatted_date = f"{date[2]}-{date[1]}-{date[0]}"

        currency_course = get_currency(formatted_date, transaction_info["currency"])
        transaction_info["currency_course"] = currency_course[0]['currencies'][0]['rateFormated']
        transaction_info["converted_to_gel"] = float(transaction_info['amount']) * float(transaction_info["currency_course"])

    keyboard = [
        [
            InlineKeyboardButton("Yes", callback_data='Yes'),
            InlineKeyboardButton("No", callback_data='No'),
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text("Do you have any other transactions?", reply_markup=reply_markup)

    return FINAL




async def transaction_final(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    reply = query.data 

    global transaction_info
    
    if reply == 'No':
        total = 0
        all_transactions.append(transaction_info)
        for tr in all_transactions:
            if tr['currency'] == 'GEL':
                total += float(tr['amount'])
                await update.effective_message.reply_text(
                    f"Date: {tr['date']}\n"
                    f"Currency: {tr['currency']}\n"
                    f"Amount of {tr['currency']}: {tr['amount']}\n"
                )
            else:
                total += float(tr['converted_to_gel'])
                await update.effective_message.reply_text(
                    f"Date: {tr['date']}\n"
                    f"Currency: {tr['currency']}\n"
                    f"Currency course to Lari: {tr['currency_course']}\n"
                    f"Amount of {tr['currency']}: {tr['amount']}\n"
                    f"Converted to Lari: {tr['converted_to_gel']}\n"
                )

        await update.effective_message.reply_text(
            f"Total is: {str(total)} Lari"
        )
        transaction_info = {}

        return ConversationHandler.END

    elif reply == 'Yes':
        all_transactions.append(transaction_info)
        transaction_info = {}
        await update.effective_message.reply_text("click to add more transaction: /add_transaction")
        return ConversationHandler.END 
    else:
        pass

