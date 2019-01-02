#!/usr/bin/python

import telebot
import sys
import os
import smbus
import Adafruit_DHT
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

if "API_TOKEN" in os.environ:
  if len(os.environ['API_TOKEN']) == 45:
    API_TOKEN = os.environ['API_TOKEN']
else:
  print ('Telegram API Token is not set')
  raise AssertionError("Please configure API_TOKEN as environment variables")

address = 0x48
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


# # Handle all other messages with content_type 'text' (content_types defaults to ['text'])
# @bot.message_handler(func=lambda message: True)
# def echo_message(message):
#     bot.send_message(message.chat.id, 'Use command from the list:\n/telemetry for telemetry \n/temperature to get temperature \n/humidity to get humidity')

# Inline keyboard
def gen_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 3
    markup.add(InlineKeyboardButton("Telemetry", callback_data="telemetry"),
        InlineKeyboardButton("Temperature", callback_data="temperature"),
        InlineKeyboardButton("Humidity", callback_data="humidity"))
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
    bot.send_message(message.chat.id, "Please chose what to get", reply_markup=gen_markup())

# Requesting loop
bot.polling()

