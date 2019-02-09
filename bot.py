#!/usr/bin/python

import telebot
import sys
import os
import smbus
import time
import Adafruit_DHT
from picamera import PiCamera
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from telebot import types

if "API_TOKEN" in os.environ:
  if len(os.environ['API_TOKEN']) == 45:
    API_TOKEN = os.environ['API_TOKEN']
else:
  print ('Telegram API Token is not set')
  raise AssertionError("Please configure API_TOKEN as environment variables")

address = 0x4f
pin = 4

bot = telebot.TeleBot(API_TOKEN)

def getTempLM75(address):
    bus = smbus.SMBus(1)
    raw = bus.read_word_data(address, 0) & 0xFFFF
    raw = ((raw << 8) & 0xFF00) + (raw >> 8)
    temperature = (raw / 32.0) / 8.0
    print ('{0:0.2f}'.format(temperature))
    return temperature


# Request all telemetry
@bot.message_handler(commands=['telemetry'])
def telemetry(message):
    humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, pin)

    print ('LM75A temperature is {0:5.2f} *C \nDHT temperature is {1:5.2f} *C \nDHT humidity is {2:5.2f}%'.format(getTempLM75(address), temperature, humidity))
    bot.send_message(message.chat.id,'LM75A temp is {0:5.2f} *C \nDHT temp is {1:5.2f} *C \nDHT hum is {2:5.2f}%'.format(getTempLM75(address), temperature, humidity))

# Request temperature from LM75A
@bot.message_handler(commands=['temperature'])
def temp(message):
    humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, pin)
    bot.send_message(message.chat.id,'LM75A temperature is {0:5.2f} *C \nDHT11 temperature is {1:5.2f} *C'.format(getTempLM75(address),temperature))

# Request temperature from LM75A
@bot.message_handler(commands=['humidity'])
def hum(message):
    humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, pin)
    bot.send_message(message.chat.id,'DHT11 humidity is {0:5.2f} %'.format(humidity))

# Request bot status
@bot.message_handler(commands=['status'])
def hum(message):
    stat_mes = os.system('cat |systemctl status telebot.service')
    bot.send_message(message.chat.id, stat_mes)

# Request bot status
@bot.message_handler(commands=['restart'])
def hum(message):
    stat_mes = os.system('python cli.py restart')
    bot.send_message(message.chat.id, stat_mes)

# Request a photo
@bot.message_handler(commands=['picture'])
def picture(message):
    camera = PiCamera()
    camera.resolution = (1024, 768)
    # camera.resolution = (1920, 1080)
    # camera.resolution = (1366, 768)
    camera.start_preview()
    bot.send_message(message.chat.id, "start preview")
    time.sleep(3)
    cam_stat = camera.capture('/home/pi/security-photo.jpg')
    bot.send_message(message.chat.id, "photo captured with status {}".format(cam_stat))
    camera.stop_preview()
    bot.send_message(message.chat.id, "stop preview")
    photo = open('/home/pi/security-photo.jpg', 'rb')
    bot.send_photo(message.chat.id, photo)
    bot.send_message(message.chat.id, "photo sent")
    bot.send_photo(message.chat.id, "FILEID")
    time.sleep(5)


# # Handle all other messages with content_type 'text' (content_types defaults to ['text'])
# @bot.message_handler(func=lambda message: True)
# def echo_message(message):
#     bot.send_message(message.chat.id, 'Use command from the list:\n/telemetry for telemetry \n/temperature to get temperature \n/humidity to get humidity')

# Inline keyboard
def inline_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 3
    markup.add(InlineKeyboardButton("Telemetry", callback_data="telemetry"),
        InlineKeyboardButton("Temperature", callback_data="temperature"),
        InlineKeyboardButton("Humidity", callback_data="humidity"))
    return markup


def block_markup(message):
    '''
    # Using the ReplyKeyboardMarkup class
    # It's constructor can take the following optional arguments:
    # - resize_keyboard: True/False (default False)
    # - one_time_keyboard: True/False (default False)
    # - selective: True/False (default False)
    # - row_width: integer (default 3)
    # row_width is used in combination with the add() function.
    # It defines how many buttons are fit on each row before continuing on the next row.
    '''
    markup = types.ReplyKeyboardMarkup(row_width=1)
    r0c0 = types.KeyboardButton('/telemetry')
    r0c1 = types.KeyboardButton('/temperature')
    r0c2 = types.KeyboardButton('/humidity')
    r1c0 = types.KeyboardButton('/picture')
    r2c0 = types.KeyboardButton('/status')
    r2c1 = types.KeyboardButton('/restart')

    markup.row(r0c0, r0c1, r0c2)
    markup.row(r1c0)
    markup.row(r2c0, r2c1)
    bot.send_message(message.chat.id, "Choose one letter:", reply_markup=markup)

    return markup

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "telemetry":
        humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, pin)
        bot.answer_callback_query(call.id, 'LM75A {0:5.2f}*C \nDHT {1:5.2f}*C & {2:5.2f}%'.format(getTempLM75(address), temperature, humidity))
    elif call.data == "temperature":
        humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, pin)
        # bot.send_message(call.id,'DHT11 humidity is {0:5.2f} %'.format(temperature))
        bot.answer_callback_query(call.id, 'DHT11 temperature is {0:5.2f} *C'.format(temperature))
    if call.data == "humidity":
        humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, pin)
        bot.answer_callback_query(call.id, 'DHT11 humidity is {0:5.2f} %'.format(humidity))

@bot.message_handler(func=lambda message: True)
def message_handler(message):
    block_markup(message)
    bot.send_message(message.chat.id, "Please chose what to get", reply_markup=inline_markup())

# Requesting loop
bot.polling()

