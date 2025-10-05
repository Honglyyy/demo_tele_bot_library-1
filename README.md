***Prerequisites

Before running the bot, make sure you have:

Python 3.8+ installed.

A Microsoft SQL Server instance.

A Telegram bot created via BotFather
.

1.Installation

Clone the repository

git clone <your-repo-url>
cd <your-repo-folder>


2.Install dependencies

pip install python-telegram-bot python-dotenv pyodbc


MSSQL Driver
Make sure you have the appropriate MSSQL ODBC driver installed for your operating system:

Windows: ODBC Driver 18 for SQL Server

Linux/macOS: Use msodbcsql18 package via your package manager.

3.Configuration

Create a .env file in the project root:

TELEGRAM_API_KEY=your_telegram_api_key
MSSQL_CONNECTION_STRING=Driver={ODBC Driver 18 for SQL Server};Server=your_server;Database=your_db;UID=your_user;PWD=your_password;


Replace your_telegram_api_key, your_server, your_db, your_user, and your_password with your actual credentials.

Usage
python bot.py


The bot will start and listen for incoming messages on Telegram.

Notes

Ensure your database server allows remote connections if not running locally.

Keep your .env file private. Do not commit it to version control.

License

This project is licensed under the MIT License.
