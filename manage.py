#!/usr/bin/env python
"""Django's command-line utility for administrative tasks with built-in .env support."""
import os
import sys

def load_env_file():
    """Load .env file with built-in fallback parser to prevent missing module errors."""
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        env_path = os.path.join(os.path.dirname(__file__), '.env')
        if os.path.exists(env_path):
            with open(env_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        k, v = line.split('=', 1)
                        os.environ.setdefault(k.strip(), v.strip())

def main():
    load_env_file()
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sskru_map.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate your virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()
