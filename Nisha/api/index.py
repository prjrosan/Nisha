#!/usr/bin/env python
"""
Vercel serverless function entry point for Nisha Django app
"""
import os
import sys
from pathlib import Path

# Get the current directory and add the Nisha subdirectory to Python path
current_dir = Path(__file__).parent
nisha_dir = current_dir.parent / 'Nisha'
sys.path.insert(0, str(nisha_dir))

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Nisha.settings')

# Import Django
import django
django.setup()

# Import WSGI application
from django.core.wsgi import get_wsgi_application
from django.contrib.staticfiles.handlers import StaticFilesHandler

# Create WSGI application
application = get_wsgi_application()

# Wrap with StaticFilesHandler for production
application = StaticFilesHandler(application)

# Vercel handler
def handler(request, context):
    return application(request, context)
