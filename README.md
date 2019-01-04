# SmartHomeBot
This is the implementation of my vision of smart home bot

<!-- [![Download Month](https://img.shields.io/pypi/v/pyTelegramBotAPI.svg)](https://pypi.python.org/pypi/pyTelegramBotAPI) -->
[![Build Status](https://travis-ci.org/Sashkoiv/SmartHomeBot.svg?branch=master)](https://travis-ci.org/Sashkoiv/SmartHomeBot)

# System process
Use telebot.service as an example of how to run the bot as a system process.
Commands you may need:
```sh
cd /lib/systemd/system
```
```sh
sudo nano telebot.service
```
```sh
systemctl daemon-reload
```
```sh
sudo systemctl restart telebot
```
```sh
systemctl status telebot.service
```

# Tips

* [systemctl howto](https://www.digitalocean.com/community/tutorials/how-to-use-systemctl-to-manage-systemd-services-and-units)
* [markdown howto](https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet)

# Used resources
* [pyTelegramBotAPI](https://github.com/eternnoir/pyTelegramBotAPI)
* [Adafruit Python DHT Sensor Library](https://github.com/adafruit/Adafruit_Python_DHT)
