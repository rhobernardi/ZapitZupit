#!/usr/bin/env python3

import os
import re
import json
import telebot
import requests
import pytesseract
from log import log
from dotenv import load_dotenv
from logging import DEBUG, INFO, WARNING, ERROR
from ImageReaderAI import read_image, enhance_image


load_dotenv()
API_KEY = os.getenv('API_KEY')
# venv_path = os.getenv('VENV_PATH')
pytesseract.pytesseract.tesseract_cmd = r'/bin/tesseract'
number_regex = "\s*\(?(\d{2}|\d{0})\)?[-. ]?(\d?\s?\d{4}|\d{4})[-. ]?(\d{4})[-. ]?\s*"
# number_regex = "\s*(\+?\d{2})?[-. ]?\(?(\d{2})\)?[-. ]?(\d{5}|\d{1}[-. ]?\d{4})[-. ]?(\d{4})[-. ]?\s*"


# Configure bot with API key
try:
    log("Connecting bot...", funcname="main")
    bot = telebot.TeleBot(API_KEY)
    log("OK", funcname="main")
except Exception as err:
    log("Error connecting to Telegram Bot", type=ERROR, funcname="main")


# Initial message
@bot.message_handler(commands=['start'])
def send_welcome(message):
    log(f"@{message.from_user.username}: Command pressed: {message.text}", funcname=send_welcome.__name__)
    # log(f"New user: @{message.from_user.username}")
    bot.send_message(
        message.chat.id, text="Olá, bem vindo ao ZapitZupit!\nPara começar, digite /help ou acesse o Menu abaixo para listar os comandos.")
    return


# Help messages
@bot.message_handler(commands=['help'])
def handle_command(message):
    log(f"@{message.from_user.username}: Command pressed: {message.text}", funcname=handle_command.__name__)
    bot.send_message(message.chat.id, text="Para usar, simplesmente digite o numero de telefone contendo DDD + 9 numeros e aguarde seu link ser gerado. Por enquanto, somente suporta numeros brasileiros com DDI +55 :)")
    bot.send_message(message.chat.id, text="Exemplos:")
    bot.send_message(
        message.chat.id, text="11 9 12345678\n(11)912345678\n11 91234-5678\n11912345678\n...")
    bot.send_message(message.chat.id, text="Também é possível enviar imagens contendo o número desejado, certifique-se de que esteja bem visível e com DDD!")
    return


# Handles all text messages that contains the commands '/fone'.
@bot.message_handler(commands=['fone'])
def handle_command(message):
    log(f"@{message.from_user.username}: Command pressed: {message.text}", funcname=handle_command.__name__)
    bot.reply_to(message, "Certo! Agora insira o numero com DDD:")
    return


# Handles all text messages that contains the commands '/imagem'.
@bot.message_handler(commands=['imagem'])
def handle_command(message):
    log(f"@{message.from_user.username}: Command pressed: {message.text}", funcname=handle_command.__name__)
    bot.reply_to(message, "Certo! Tire uma foto do número ou insira uma imagem (certifique-se que os números estejam bem visíveis e com DDD):")
    return


# Handle all text messages that constains ONLY a phone number
@bot.message_handler(regexp=f"^{number_regex}$")
def handle_number(message):
    log(f"@{message.from_user.username}: Number identified: {str(message.text)}", funcname=handle_number.__name__)
    bot.reply_to(message, "Número identificado")
    link = "Aqui está seu link!\nhttps://wa.me/55" + \
            str(message.text).replace("-", "").replace("(", "").replace(")", "").replace(" ", "")
    bot.send_message(message.chat.id, text=link)
    return


# Handles all text messages that contains a phone number. Also returns more than one number.
@bot.message_handler(regexp=number_regex)
def handle_numbers(message):
    log(f"@{message.from_user.username}: One or more numbers identified: {str(message.text)}", funcname=handle_numbers.__name__)
    rgx = re.compile(number_regex)
    numbers = rgx.findall(message.text)
    phone_number = ''
    for i in range(len(numbers)):
        for n in numbers[i]:
            phone_number = phone_number + n
        log(f"@{message.from_user.username}: Number sent by user: [{i+1}/{len(numbers)}] {str(phone_number)}", funcname=handle_numbers.__name__)
        link = "Aqui está seu link!\nhttps://wa.me/55" + \
                str(phone_number).replace("-", "").replace("(", "").replace(")", "").replace(" ", "")
        bot.send_message(message.chat.id, text=link)
        phone_number = ""
    return


# Handles all text messages that have an image or photo to recognize a number.
@bot.message_handler(content_types=['photo'])
def handle_image(message):
    bot.send_message(message.chat.id, text="Imagem detectada! Analisando..")
    log(f"@{message.from_user.username}: Image ID sent by user: {str(message.photo[1].file_id)}", funcname=handle_image.__name__)
    # Assemble URLs to download the image sent by user
    image_id_url = f"https://api.telegram.org/bot{API_KEY}/getFile?file_id={str(message.photo[1].file_id)}"
    response = requests.get(image_id_url)
    remote_file_path = json.loads(response.content)["result"]['file_path']
    image_url = f"https://api.telegram.org/file/bot{API_KEY}/{str(remote_file_path)}"
    # Requests the image from telegram server
    response = requests.get(image_url)
    local_image_path = f"./img/image_{str(message.from_user.username)}_{message.photo[1].file_id}.jpg"
    with open(local_image_path, "wb") as f:
        f.write(response.content)
    try: # try to read text in image
        numbers = str(pytesseract.image_to_string(local_image_path))
    except:
        log(f"@{message.from_user.username}: Couldn't open image or read text.", funcname=handle_image.__name__, type=ERROR)
        bot.send_message(
            message.chat.id, text="Desculpe o inconveniente, eu tive um problema no recebimento da sua foto.")
        bot.send_message(
            message.chat.id, text="Poderia digitar o número ou tentar novamente mais tarde?")
        return
    rgx = re.compile(number_regex)
    numbers = rgx.findall(numbers)
    # Check if phone numbers were found
    if len(numbers) == 0:
        bot.send_message(message.chat.id, text="Só um minuto. Vou tentar melhorar a qualidade da imagem.")
        log(f"@{message.from_user.username}: Problem to read text in image. Trying to improve quality...", funcname=handle_image.__name__)
        new_image = enhance_image(local_image_path)
        numbers = str(pytesseract.image_to_string(new_image))
        numbers = rgx.findall(numbers)
        # Check again if numbers were found in better quality
        if len(numbers) == 0:
            log(f"@{message.from_user.username}: Phone number could not be identified in image.", funcname=handle_image.__name__, type=ERROR)
            bot.send_message(
                message.chat.id, text="Desculpe, não consegui identificar um número de celular na sua foto.")
            bot.send_message(
                message.chat.id, text="Tente novamente ou digite /help para tentar de outra forma.")
            return
        else:
            bot.reply_to(message, "Número detectado na imagem")
            log(f"@{message.from_user.username}: One or more numbers identified in image after image enchancement", funcname=handle_image.__name__)
    else:
        bot.reply_to(message, "Número detectado na imagem")
        log(f"@{message.from_user.username}: One or more numbers identified in image", funcname=handle_image.__name__)
    phone_number = ''
    for i in range(len(numbers)):
        for n in numbers[i]:
            phone_number = phone_number + n
        log(f"@{message.from_user.username}: Number sent by user: [{i+1}/{len(numbers)}] {str(phone_number)}", funcname=handle_image.__name__)
        link = "Aqui está seu link!\nhttps://wa.me/55" + \
                str(phone_number).replace("-", "").replace("(", "").replace(")", "").replace(" ", "")
        bot.send_message(message.chat.id, text=link)
        phone_number = ""
    return


# Handles all other text messages
@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
    log(f"@{message.from_user.username}: No numbers detected in user's message: \"{message.text}\"", funcname=handle_all_messages.__name__)
    bot.send_message(
        message.chat.id, "Desculpe, não consegui identificar um número de celular na sua mensagem. Tente novamente ou digite /help para mais informações.")
    return


# Connect bot to Telegram and start it
try:
    log("Running...", funcname="main")
    bot.infinity_polling()
    log("Bot stopped", funcname="main")
except:
    log("Connection problem with Infinity Pooling.", type=ERROR, funcname="main")
