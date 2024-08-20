import spacy
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler

TOKEN = '7187563467:AAEUaoziTIVBRq4wz6dRJIZJfG4bBiRAIAc'
BOT_USERNAME = '@I_Liverpool_Chatbot'

async def state0_handler(update, context):
    """use SpaCy to handle state0"""
    nlp = spacy.load('en_core_web_sm')
    doc = nlp(update.message.text)
    reply = ''
    if reply:
        update.message.reply_text(reply)
    return 'STATE0'


#Commands
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Hello, I am a Liverpool Chatbot. Send /help for more info.')
    return 'STATE0'
    
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('I am Liverpool bot! Please type something so I can respond!')
    return

async def cancel_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Thank you for chatting with Liverpool Chatbot! I will be off the!')
    return ConversationHandler.END


# Responses - this function handles responses of the bot

def handle_response(text: str) -> str:
    processed: str = text.lower() #this ensures that text is in lowercase

    if 'hello' in processed:
        return 'Hey there!'
    if 'who are the liverpool players' in processed:
        return 'The top five Liverpool players are: Mohammed Salah, Luiz Diaz, Alisson, Virgil van Dijik, Diogo jota'
    if 'what are liverpool next fixtures' in processed:
        return 'The next liverpool fixtures are: Brentford(H), Manchester United(A), Forest(H)'
    if 'where is liverpool stadium' in processed:
        return 'Liverpool stadium is called Anfield. The stadium is in Liverpool,England'
    if 'how many trophies does liverpool have' in processed:
        return 'Liverpool have won 51 major club trophies'

    return 'i do not understand what you wrote, Please write again....'


#this function checks if the message was sent from a groupchat or privatechat
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text

    print(f'User ({update.message.chat.id}) in {message_type}: "{text}"')
     #this statement is used for debugging. It will log messages coming to the bot

    if message_type == 'group':
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME, '').strip()
            response: str = handle_response(new_text)
        else:
            response: str = handle_response(text)
    else:
        response: str = handle_response(text)


    print('Bot:', response)
    await update.message.reply_text(response)


#this function is used for loggin errors

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')

#this puts the Application altogether
if __name__ == '__main__':
    print('Starting bot....')
    app = Application.builder().token(TOKEN).build()


    #Commands
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('cancel', cancel_command))
 

    # Messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    # Error handling
    app.add_error_handler(error)

    # Polls the bot
    print('Polling...')
    app.run_polling(poll_interval=5)
