#!/usr/bin/env bash

#celery worker -A system -l info && celery -A system beat -l info -S django

# development
celery -A system worker --beat --scheduler django --loglevel=info