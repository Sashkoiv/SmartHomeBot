# SmartHomeBot
This is the implementation of my vision of smart home bot

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