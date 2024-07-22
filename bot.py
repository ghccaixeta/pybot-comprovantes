import os, telebot, requests, json, shutil
from dotenv import load_dotenv
from telebot import types
from comprovantes import extractComprovante
from rpa import extractRpa

load_dotenv()

telegramToken = os.getenv('TELEGRAM_TOKEN')

bot = telebot.TeleBot(telegramToken)

def checkTelegramFile(fileId, fileName):
    res = requests.get(f'https://api.telegram.org/bot{telegramToken}/getFile?file_id={fileId}')

    if res.status_code == 200:
        response = json.loads(res.text)
        filePath = response['result']['file_path']
        
        return downloadTelegramFile(filePath, fileName)
    
    return False

def downloadTelegramFile(filePath, fileName):
    res = requests.get(f'https://api.telegram.org/file/bot{telegramToken}/{filePath}')

    if res.status_code == 200:
        with open(f"./pdf/{fileName}", "wb") as file:
            file.write(res.content)
            return True
    return False

# Handles all sent documents and audio files
@bot.message_handler(content_types=['document', 'audio'])
def handle_docs_audio(message):
    if message.document.mime_type == 'application/pdf':
        if message.document.file_name == 'comprovantes.pdf':
            bot.send_message(message.chat.id, text='Verificando arquivo. Aguarde...')
            checkFileOk = checkTelegramFile(message.document.file_id, message.document.file_name)
            bot.send_message(message.chat.id, text='Processando arquivo. Aguarde...')
            resultOfExtract = extractComprovante()
            if resultOfExtract:
                shutil.make_archive('./assets/comprovantes', 'zip', './assets/comprovantes')
                doc = open('./assets/comprovantes.zip', 'rb')
                bot.send_document(message.chat.id, doc)
        elif message.document.file_name == 'rpa.pdf':
            bot.send_message(message.chat.id, text='Verificando arquivo. Aguarde...')
            checkFileOk = checkTelegramFile(message.document.file_id, message.document.file_name)
            bot.send_message(message.chat.id, text='Processando arquivo. Aguarde...')
            resultOfExtract = extractRpa()
            if resultOfExtract:
                shutil.make_archive('./assets/rpa', 'zip', './assets/rpa')
                doc = open('./assets/rpa.zip', 'rb')
                bot.send_document(message.chat.id, doc)
        else:
            bot.send_message(message.chat.id, text='Documento inválido')


bot.infinity_polling()