#!/usr/bin/env python3

import click # type: ignore
import subprocess
import sys
import os
import glob
from magi_cli.spells import commands_list, aliases, SANCTUM_PATH

@click.group()
@click.pass_context
def cli(ctx):
    """A Python CLI for casting spells."""
    pass

for command in commands_list:
    cli.add_command(command)

# Non-click functions

def execute_bash_file(filename):
    subprocess.run(["bash", filename], check=True)

# Updated execute_python_file function to accept args
def execute_python_file(filename, args):
    subprocess.run([sys.executable, filename, *args], check=True)

def execute_spell_file(spell_file):
    tome_path = os.path.join(SANCTUM_PATH, '.tome')
    spell_file_path = spell_file if '.tome' in spell_file else os.path.join(tome_path, spell_file)

    if not spell_file_path.endswith('.spell'):
        spell_file_path += '.spell'
    
    if not os.path.exists(spell_file_path):
        click.echo(f"Could not find {spell_file}.spell in .tome directory. Checking current directory for .tome directory...")
        spell_file_path = os.path.join(".tome", spell_file)
        if not os.path.exists(spell_file_path):
            click.echo(f"Could not find {spell_file}.spell in current directory or .tome directory.")
            return
        elif not spell_file_path.endswith('.spell'):
            spell_file_path += '.spell'

    with open(spell_file_path, 'r') as file:
        lines = file.readlines()

    for line in lines:
        stripped_line = line.strip()
        if stripped_line.startswith("#"):
            continue
        subprocess.run(stripped_line, shell=True)

# Click functions

@click.command()
@click.argument('input', nargs=-1)
def cast(input, **kwargs):
    input = list(input)  # Convert input into a list to separate command and arguments

    # Use SANCTUM_PATH for the .tome directory
    tome_path = os.path.join(SANCTUM_PATH, '.tome')

    if not input:
        # Display available commands and spells if no input is provided
        print("Available commands:")
        for name, command in cli.commands.items():
            print(f"- {name}: {command.help}")

        print("\nAvailable spells recorded in your tome:")
        for file in glob.glob(f"{tome_path}/*.spell"):
            print(f"- {os.path.basename(file)}")

    elif input[0] in aliases:
        command = aliases[input[0]]
        ctx = click.get_current_context()
        if len(input) > 1:
            ctx.invoke(command, args=input[1:])
        else:
            if 'alias' in kwargs:
                ctx.invoke(command, alias=kwargs['alias'])
            else:
                ctx.invoke(command)
    elif input[0] in cli.commands:
        ctx = click.get_current_context()
        command = cli.commands[input[0]]
        if len(input) > 1:
            # Ensure the arguments are passed correctly
            ctx.invoke(command, args=input[1:])
        else:
            if 'alias' in kwargs:
                ctx.invoke(command, alias=kwargs['alias'])
            else:
                ctx.invoke(command)

    else:
        # Check if the input is a file and execute accordingly
        file_path = os.path.join(tome_path, input[0])
        if os.path.isfile(file_path) or os.path.isfile(input[0]):
            target_file = file_path if os.path.isfile(file_path) else input[0]
            if target_file.endswith(".py"):
                execute_python_file(target_file, input[1:])
            elif target_file.endswith(".spell"):
                execute_spell_file(target_file.replace(".spell", ""))
            elif target_file.endswith(".sh"):
                execute_bash_file(target_file)
        else:
            print(f"Error: Command or file '{input[0]}' not found.")

def main():
    cast()

if __name__ == "__main__":
    main()