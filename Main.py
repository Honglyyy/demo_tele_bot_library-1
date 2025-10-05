import os
from dotenv import load_dotenv
import pyodbc
from telegram import Update
from telegram.ext import (
    Application, CommandHandler, MessageHandler,
    ContextTypes, filters, ConversationHandler
)

load_dotenv()

CONNECTION_STRING = os.getenv('CON_STR')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')

ASK_EMAIL, ASK_PASSWORD = range(2)

#Database connection
def get_con():
    con = pyodbc.connect(CONNECTION_STRING)
    return con

#check if email exist in the db
#cursor is a control struc to execute the sql comm and fetch rows
def check_email(email: str)-> bool:
    conn = get_con()
    cursor = conn.cursor()
    #Select 1 means find if the col exist or not
    cursor.execute('SELECT 1 FROM users WHERE email = ?', (email,))
    exist = cursor.fetchone() is not None
    conn.close()
    return exist
#save user and ask your password if the email doesnt exist and create a new account
def save_user(telegram_id:str, email: str, password: str):
    conn = get_con()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Users (TelegramId,Email, Pass) VALUES (?, ?,?)",(telegram_id,email, password))
    conn.commit()
    conn.close()

# /start command
async def start_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    await update.message.reply_text(f"Hello {user.first_name}! Use /register to login.")

# /register command
async def register_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("Please enter your email address!!!")
    return ASK_EMAIL


async def get_email(update: Update, context: ContextTypes.DEFAULT_TYPE)-> int:
    email = update.message.text.strip()
    if(check_email(email)):
        await update.message.reply_text("Email already registered!!\n Enter new email!!")
        return ASK_EMAIL

    context.user_data['email'] = email
    await update.message.reply_text("Great now please enter your password!!!")
    return ASK_PASSWORD

async def get_password(update: Update, context: ContextTypes.DEFAULT_TYPE)-> int:
    password = update.message.text.strip()
    context.user_data["password"] = password
    email = context.user_data.get("email")
    telegram_id = update.effective_user.id
    save_user(telegram_id,email, password)

    await update.message.reply_text(f"Registration complete \nEmail: {email}\nPassword: {password}")
    context.user_data.clear()

    return ConversationHandler.END

# Main
def main():
    print("Starting the bot....!!")
    app = Application.builder().token(TELEGRAM_TOKEN).build()

    registration_handler = ConversationHandler(
        entry_points=[CommandHandler('register', register_cmd)],
        states={
            ASK_EMAIL: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_email)],
            ASK_PASSWORD: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_password)],
        },
        fallbacks=[]
    )

    app.add_handler(CommandHandler('start', start_cmd))
    app.add_handler(registration_handler)
    print("Polling Telegram Bot...")
    app.run_polling()

if __name__ == '__main__':
   main()
