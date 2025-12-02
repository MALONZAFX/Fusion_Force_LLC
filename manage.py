#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from dotenv import load_dotenv  # ADD THIS

def main():
    """Run administrative tasks."""
    load_dotenv()  # ADD THIS - Loads .env file
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fusion_force.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed?"
        ) from exc
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()