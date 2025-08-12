import os
import sys
from pathlib import Path

# Add the project directory to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Nisha.settings')

# Import Django and create application
from django.core.wsgi import get_wsgi_application
from django.contrib.staticfiles.handlers import StaticFilesHandler

# Create WSGI application
application = StaticFilesHandler(get_wsgi_application())

# For Vercel serverless
def handler(request, context):
    return application(request, context)
