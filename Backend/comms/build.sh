#!/usr/bin/bash

pip install -r reqirements.txt
python3.9 manage.py collectstatic --noinput
