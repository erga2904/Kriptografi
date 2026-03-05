"""
Vercel serverless entry point.
"""
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app

app = create_app()

# Vercel requires either 'app' (WSGI) or handler function
# Flask app is WSGI compliant, so just export it
