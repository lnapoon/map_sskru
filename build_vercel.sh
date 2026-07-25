#!/bin/bash
# Vercel build script - install dependencies and run migrations
pip install -r requirements.txt
python manage.py migrate --noinput
