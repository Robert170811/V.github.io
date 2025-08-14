##########################################
#                                        #
#   ██╗   ██╗██████╗  ██████╗ ████████╗  #
#   ██║   ██║██╔══██╗██╔═══██╗╚══██╔══╝  #
#   ██║   ██║██████╔╝██║   ██║   ██║     #
#   ╚██╗ ██╔╝██╔══██╗██║   ██║   ██║     #
#    ╚████╔╝ ██████╔╝╚██████╔╝   ██║     #
#     ╚═══╝  ╚═════╝  ╚═════╝    ╚═╝     #
##########################################
import logging
from telegram import Update, InputFile
from telegram.ext import Application, Updater, ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters, CallbackContext


import requests
import os
BOT_TOKEN = "7263991319:AAH7AJEySii9pu4e0spxr7M56yEAZtUs924"

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text=
        "I'm a bot, please talk to me!\n"
        "Send commands /start")

                                                 
#   ██╗   ██╗ ██████╗ ██╗ ██████╗███████╗          
#   ██║   ██║██╔═══██╗██║██╔════╝██╔════╝          
#   ██║   ██║██║   ██║██║██║     █████╗            
#   ╚██╗ ██╔╝██║   ██║██║██║     ██╔══╝            
#    ╚████╔╝ ╚██████╔╝██║╚██████╗███████╗          
#     ╚═══╝   ╚═════╝ ╚═╝ ╚═════╝╚══════╝          
#                                                  
#                                                                  
#    ██████╗  ███████╗███╗   ██╗███████╗██████╗  █████╗ ████████╗███████╗  
#    ██╔═══╝  ██╔════╝████╗  ██║██╔════╝██╔══██╗██╔══██╗╚══██╔══╝██╔════╝  
#    ██║  ███╗█████╗  ██╔██╗ ██║█████╗  ██████╔╝███████║   ██║   █████╗    
#    ██║   ██║██╔══╝  ██║╚██╗██║██╔══╝  ██╔══██╗██╔══██║   ██║   ██╔══╝    
#    ╚██████╔╝███████╗██║ ╚████║███████╗██║  ██║██║  ██║   ██║   ███████╗  
#     ╚═════╝ ╚══════╝╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝   ╚══════╝  
                             
async def voice_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Write words what you need to voice:')

async def process_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = update.message.text
    chat_id = update.message.chat.id
    
    try:
        # URL encode the text (important for special characters)
        import urllib.parse
        encoded_text = urllib.parse.quote_plus(text)
        
        # Create the Google TTS URL
        tts_url = f"https://translate.google.com/translate_tts?ie=UTF-8&tl=en&q={encoded_text}&client=tw-ob"
        
        # Download the audio file
        response = requests.get(tts_url, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
        if response.status_code == 200:
            # Save the audio file temporarily
            audio_file = f"{chat_id}_voice.mp3"
            with open(audio_file, 'wb') as f:
                f.write(response.content)
            
            # Send the audio file to the user
            with open(audio_file, 'rb') as audio:
                await update.message.reply_voice(voice=InputFile(audio))
            
            # Remove the temporary file
            os.remove(audio_file)
        else:
            await update.message.reply_text("Sorry, I couldn't generate the voice message. Please try again.")
    
    except Exception as e:
        await update.message.reply_text(f"An error occurred: {str(e)}")
#######################################
#                                     #
#   ███╗   ███╗ █████╗ ██╗███╗   ██╗  #
#   ████╗ ████║██╔══██╗██║████╗  ██║  #
#   ██╔████╔██║███████║██║██╔██╗ ██║  #
#   ██║╚██╔╝██║██╔══██║██║██║╚██╗██║  #
#   ██║ ╚═╝ ██║██║  ██║██║██║ ╚████║  #
#   ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝╚═╝  ╚═══╝  #
#                                     #
#######################################

def main():
   
    application = Application.builder().token(BOT_TOKEN).build()

    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("voice", voice_command))
    
    application.add_handler(CommandHandler("search", voice_command))
    
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, process_text))
    
    # Run the bot
    application.run_polling()
  

if __name__ == '__main__':
    main()