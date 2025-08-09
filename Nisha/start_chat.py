#!/usr/bin/env python3
import os
import sys
import django
from django.core.management import execute_from_command_line
from daphne.cli import CommandLineInterface

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Nisha.settings')
django.setup()

if __name__ == '__main__':
    # Start Daphne server
    import subprocess
    subprocess.run(['python3', '-c', '''
import os
import django
from daphne.cli import CommandLineInterface

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Nisha.settings")
django.setup()

cli = CommandLineInterface()
cli.run(["-p", "8000", "Nisha.asgi:application"])
''']) 