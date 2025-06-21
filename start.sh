#!/bin/bash
pip install --upgrade pip
pip install -r requirements.txt
exec gunicorn app:app --bind 0.0.0.0:$PORT --timeout 300