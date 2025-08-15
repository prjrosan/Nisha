#!/usr/bin/env python
"""
Vercel serverless function entry point for Nisha Django app
"""
import os
import sys

# Add the Nisha subdirectory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'Nisha'))

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Nisha.settings')

# Import Django and WSGI application
from django.core.wsgi import get_wsgi_application
from django.contrib.staticfiles.handlers import StaticFilesHandler

# Create WSGI application
application = get_wsgi_application()

# Wrap with StaticFilesHandler for production
application = StaticFilesHandler(application)

# Vercel handler
def handler(request, context):
    return application(request, context)
