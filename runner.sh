#!/usr/bin/env sh

ls $PROMPTS_FILE | entr -n -r python3 ./main.py
