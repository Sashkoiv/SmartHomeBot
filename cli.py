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

    if os.system('sudo systemctl daemon-reload'):
        raise AssertionError("Can't reload daemons")
    else:
        click.echo('Daemons are reloaded')

    if os.system('sudo systemctl enable ' + MODULE_NAME):
        raise AssertionError("Can't enable system process")
    else:
        click.echo('Daemon enabled')

    if os.system('sudo systemctl start ' + MODULE_NAME):
        raise AssertionError("Can't start system process")
    else:
        click.echo('Daemon started')

    os.system('sudo systemctl status ' + MODULE_NAME)

@cli.command()
def stop():
    "Stop a system background process"

    if os.system('sudo systemctl stop ' + MODULE_NAME):
        raise AssertionError("Can't start system process")
    else:
        click.echo('Daemon stopped')

    os.system('sudo systemctl status ' + MODULE_NAME)

@cli.command()
def restart():
    "Restart a system background process"

    if os.system('sudo systemctl daemon-reload'):
        raise AssertionError("Can't start system process")
    else:
        click.echo('Daemon reloaded')

    if os.system('sudo systemctl restart ' + MODULE_NAME):
        raise AssertionError("Can't start system process")
    else:
        click.echo('Daemon restarted')

    os.system('sudo systemctl status ' + MODULE_NAME)

@cli.command()
def status():
    "Status of a system background process"
    os.system('sudo systemctl status ' + MODULE_NAME)


if __name__ == '__main__':
    cli()