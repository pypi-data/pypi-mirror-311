#!/usr/bin/env bash

title running...
python -m venv venv  && . venv/Scripts/activate && pip install -r requirements.txt && python convert_ui.py