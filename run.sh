#!/bin/bash

echo "Starting the bot..."
token=$(gpg -d --quiet token.gpg)
python3 src/bot.py "$token"
$SHELL
