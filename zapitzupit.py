#!/usr/bin/env python3

import os
import re
import json
import telebot
import requests
import pytesseract
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv('API_KEY')
number_regex = "\s*\(?(\d{2}|\d{0})\)?[-. ]?(\d?\s?\d{4}|\d{4})[-. ]?(\d{4})[-. ]?\s*"

# Configure bot
try:
    bot = telebot.TeleBot(API_KEY)
except Exception as err:
    print("Error connecting to Telegram Bot")
    print(f"Error: {err}")


@bot.message_handler(commands=['start'])
def send_welcome(message):
    print("New user: " + message.from_user.username)
    bot.send_message(
        message.chat.id, text="Olá, bem vindo ao ZapitZupit!\nPara começar, digite /ajuda ou acesse o Menu abaixo para listar os comandos.")
    # bot.send_message(message.chat.id, text="Para usar, simplesmente digite o numero de celular com DDD ou tire uma foto do numero e seu link será gerado :)")
    # bot.send_message(message.chat.id, text="Digite /help para mais informações.")


@bot.message_handler(commands=['help'])
def send_welcome(message):
    bot.send_message(message.chat.id, text="Para usar, simplesmente digite o numero de telefone contendo DDD + 9 numeros e aguarde seu link ser gerado. Por enquanto, somente suporta numeros brasileiros com DDI +55 :)")
    bot.send_message(message.chat.id, text="Exemplos:")
    bot.send_message(
        message.chat.id, text="11 9 12345678\n(11)912345678\n11 91234-5678\n11912345678")


# Handles all text messages that contains the commands '/fone'.
@bot.message_handler(commands=['fone'])
def handle_start_help(message):
    bot.reply_to(message, "Certo! Agora insira o numero com DDD:")


# Handle all text messages that constains ONLY a phone number
@bot.message_handler(regexp="^" + number_regex + "$")
def handle_start_help(message):
    print(
        f"Number sent by user {str(message.from_user.username)}: {str(message.text)}")
    bot.reply_to(message, "Número identificado")
    link = "Aqui está seu link!\nhttps://wa.me/55" + \
        str(message.text).replace(
            "-", "").replace("(", "").replace(")", "").replace(" ", "")
    bot.send_message(message.chat.id, text=link)


# Handles all text messages that contains a phone number. Example '011924192392'.
@bot.message_handler(regexp=number_regex)
def handle_start_help(message):
    rgx = re.compile(number_regex)
    numbers = rgx.findall(message.text)
    number = ''
    for i in range(len(numbers)):
        for n in numbers[i]:
            number = number + n
        print("Number sent by user " +
              str(message.from_user.username) + ": " + str(number))
        link = "Aqui está seu link!\nhttps://wa.me/55" + \
            str(number).replace("-", "").replace("(",
                                                 "").replace(")", "").replace(" ", "")
        bot.send_message(message.chat.id, text=link)


# Handles all text messages that have an image or photo to recognize a number.
@bot.message_handler(content_types=['photo'])
def handle_start_help(message):
    print("Image sent by user " + str(message.from_user.username) +
          ": " + str(message.photo[1].file_id))
    file_id_url = f"https://api.telegram.org/bot{API_KEY}/getFile?file_id={str(message.photo[1].file_id)}"
    response = requests.get(file_id_url)
    file_path = json.loads(response.content)["result"]['file_path']
    file_url = f"https://api.telegram.org/file/bot{API_KEY}/{str(file_path)}"
    response = requests.get(file_url)
    img_name = f"{venv_path}/img/image_{str(message.from_user.username)}_{message.photo[1].file_id}.jpg"
    with open(img_name, "wb") as f:
        f.write(response.content)
    try:
        pytesseract.pytesseract.tesseract_cmd = r'/bin/tesseract'
        numbers = str(pytesseract.image_to_string(img_name))
    except:
        print("Couldn't open image or read text.")
        bot.send_message(
            message.chat.id, text="Desculpe o inconveniente, eu tive um problema no recebimento da sua foto.")
        bot.send_message(
            message.chat.id, text="Poderia digitar o numero ou tentar novamente mais tarde?")
        return
    rgx = re.compile(number_regex)
    numbers = rgx.findall(numbers)
    if len(numbers) == 0:
        print("Numero")
        bot.send_message(
            message.chat.id, text="Desculpe, não consegui identificar um número de celular na sua foto.")
        bot.send_message(
            message.chat.id, text="Tente novamente ou digite /help para tentar de outra forma.")
        return
    else:
        bot.reply_to(message, "Numero detectado na imagem")
    number = ''
    for i in range(len(numbers)):
        for n in numbers[i]:
            number = number + n
        print("Number sent by user " +
              str(message.from_user.username) + ": " + str(number))
        link = "Aqui está seu link!\nhttps://wa.me/55" + \
            str(number).replace("-", "").replace("(",
                                                 "").replace(")", "").replace(" ", "")
        bot.send_message(message.chat.id, text=link)


# Handles all other text messages
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    print("Invalid number from: " + message.from_user.username)
    bot.send_message(
        message.chat.id, "Desculpe, não consegui identificar um número de celular na sua mensagem. Tente novamente ou digite /help para mais informações.")


# Connect bot to Telegram and start it
try:
    bot.infinity_polling()
except:
    print("Connection problem with Infinity Pooling.")
