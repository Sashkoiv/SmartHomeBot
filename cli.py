# coding: utf-8
import click
import os
import sys

MODULE_NAME = 'smarthomebot'

@click.group()
def cli():
    pass


@cli.command()
@click.argument('token')
def daemon(token):
    "Make a bot a system background process"

    if not os.access('/lib/systemd/system', os.W_OK):
        raise AssertionError("Not allowed to write in directory /lib/systemd/system try using sudo")
    else:
        click.echo('Writing to the system folder allowed')

    if not (len(token)==45 and token[9]==':'):
        raise AssertionError("Wrong token symbols count or typo found")
    else:
        click.echo('The token is valid')

    try:
        with open("telebot.service", 'r') as f:
            service_template = f.read()
        f.close()
        click.echo('Template file read successfully')
    except AssertionError:
        raise AssertionError("Template file couldn't be opened")

    service_template = service_template.replace('enter_telegram_bot_token_here', token, 1)

    try:
        with open('/lib/systemd/system/'+ MODULE_NAME + '.service', 'w') as f:
            f.write(service_template)
        f.close()
        click.echo('.service file created successfully')
    except AssertionError:
        raise AssertionError("Can't create .service file")

    click.echo('Now manage your deamon with further commands')


@cli.command()
def start():
    "Start a system background process"
    print ()

@cli.command()
def stop():
    "Stop a system background process"

@cli.command()
def restart():
    "Restart a system background process"

@cli.command()
def status():
    "Status of a system background process"



# @click.option("--count", default=1, help="Number of greetings.")
# @click.option("--name", prompt="Your name", help="The person to greet.")
# def test(count, name):
#     """Simple program that greets NAME for a total of COUNT times."""
#     for _ in range(count):
#         print ("Hello, %s!" % name)
#         click.echo("Hello, %s!" % name)

# @cli.command()
# @click.option("--pompom", '-p', default='trololo', help='my first command')
# def cl(pompom):
#     """trololo"""
#     click.echo("entered %s" % pompom)

if __name__ == '__main__':
    cli()