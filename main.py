#!/usr/bin/env python3
from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
import os
import yaml
from pathlib import Path
import sys


prompts = None
with open(f'{os.environ.get("PROMPTS_FILE", "./prompts.yaml")}', 'r') as fle:
    prompts = yaml.safe_load(fle)


async def fileSender(prompt: dict, update: Update.message):
    if photos := prompt.get('photos'):
        for photo in photos:
            await update.reply_photo(Path(photo))

    if audios := prompt.get('audios'):
        for audio in audios:
            await update.reply_audio(Path(audio))

    if documents := prompt.get('documents'):
        for document in documents:
            await update.reply_document(Path(document))

    if videos := prompt.get('videos'):
        for video in videos:
            await update.reply_video(Path(video))


async def director(update: Update.message) -> str:
    #TODO: check file existance before using it path!
    #TODO: check if yaml file is correct and exist!
    #TODO: use caption for each files that we sending.
    #TODO: sending messages are duplicated ageain!
    #TODO: use seprate file for some functionalities
    #TODO: we should let this run another module to run and send data to user(importlib)
    is_cmd_match = False
    for prompt in prompts.get('commands'):
        if prompt.get('key') == update.text:
            is_cmd_match = True
            if messages := prompt.get('messages'):
                for message in messages:
                    await update.reply_text(f'{message}')
            await fileSender(prompt, update)

    if not is_cmd_match:
        if prompt := prompts.get('wrong_command'):
            if messages := prompt.get('messages'):
                for message in messages:
                    await update.reply_text(f'{message}')
            await fileSender(prompt, update)
        else:
            print("no wrong/default command set!", flush=True, file=sys.stderr)


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    #TODO: use `on` keyword in YAML, which tell that which of this should take the command
    if update.message:
        await director(update.message)
    elif update.business_message:
        await director(update.business_message)
    else:
        print("No supported message!", flush=True, file=sys.stderr)


def main() -> None:
    application = Application.builder().token(os.environ.get("API_KEY")).build()

    application.add_handler(MessageHandler(filters.TEXT, echo))

    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    print("starting...", flush=True)
    main()
