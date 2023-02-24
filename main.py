from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from bot_commands import *
from bot_conversation import *


app = ApplicationBuilder().token("6074794536:AAHRIBLQJXRGGBs1txKMXkQMCRxM99MSM3o").build()

app.add_handler(CommandHandler("help", help_command))
app.add_handler(CommandHandler("hello", hello_command))
app.add_handler(conv_handler)
app.add_handler(CommandHandler("new_year", days_to_new_year))
app.add_handler(CommandHandler("phrase", random_phrase))

print(emoji.emojize("Server has been started :red_heart:", variant="emoji_type"))

app.run_polling()

print('Server has been stopped!')