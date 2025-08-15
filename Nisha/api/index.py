#!/usr/bin/env python
"""
Vercel serverless function entry point for Nisha Django app
"""
import os
import sys
from pathlib import Path

# Get the current directory
current_dir = Path(__file__).parent

# Add the Nisha subdirectory to Python path
nisha_path = current_dir.parent / 'Nisha'
sys.path.insert(0, str(nisha_path))

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Nisha.settings')

# Configure Django
import django
django.setup()

# Import Django and WSGI application
from django.core.wsgi import get_wsgi_application

# Create WSGI application
application = get_wsgi_application()

# Vercel handler
def handler(request, context):
    return application(request, context)
