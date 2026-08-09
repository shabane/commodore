#!/usr/bin/env python3
from telegram.ext import CallbackQueryHandler
from telegram import Update
from telegram.ext import Application, ContextTypes, MessageHandler, filters
import os
import yaml
import sys
import importlib


prompts = None


def load_prompts():
    global prompts
    with open(f'{os.environ.get("PROMPTS_FILE", "./prompts.yaml")}', 'r') as fle:
        prompts = yaml.safe_load(fle)


load_prompts()


async def fileSender(prompt: dict, update: Update):
    if photos := prompt.get('photos'):
        for photo in photos:
            try:
                with open(photo, 'rb') as f:
                    await update.reply_photo(f)
            except Exception as e:
                print(f"Error sending photo {photo}: {e}")

    if audios := prompt.get('audios'):
        for audio in audios:
            try:
                with open(audio, 'rb') as f:
                    await update.reply_audio(f)
            except Exception as e:
                print(f"Error sending audio {audio}: {e}")

    if documents := prompt.get('documents'):
        for document in documents:
            try:
                with open(document, 'rb') as f:
                    await update.reply_document(f)
            except Exception as e:
                print(f"Error sending document {document}: {e}")

    if videos := prompt.get('videos'):
        for video in videos:
            try:
                with open(video, 'rb') as f:
                    await update.reply_video(f)
            except Exception as e:
                print(f"Error sending video {video}: {e}")


async def pluginRunner(
        prompt: dict,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE):
    if plugins := prompt.get('plugins'):
        for plugin in plugins:
            if os.path.exists(f'./plugins/{plugin}/main.py'):
                lib = importlib.import_module(f'plugins.{plugin}.main')
                # allow hot reloading plugins
                importlib.reload(lib)
                if hasattr(lib, 'run'):
                    await lib.run(prompt=prompt, update=update, context=context)
                else:
                    # TODO: this should be a better error handling.
                    print("plugin is not right")
            else:
                # TODO: use the better error handling method.
                print("plugin file does not exist")


async def director(
        message,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE) -> str:
    # TODO: check file existance before using it path!
    # TODO: check if yaml file is correct and exist!
    # TODO: use caption for each files that we sending.
    # TODO: sending messages are duplicated ageain!
    # TODO: use seprate file for some functionalities
    # TODO: we should let this run another module to run and send data to
    # user(importlib)
    is_cmd_match = False
    for prompt in prompts.get('commands', []):
        if prompt.get('key') == message.text:
            is_cmd_match = True
            if messages := prompt.get('messages'):
                for msg in messages:
                    await message.reply_text(f'{msg}')

            await fileSender(prompt, message)
            await pluginRunner(prompt, update, context)

    if not is_cmd_match:
        if prompt := prompts.get('wrong_command'):
            if messages := prompt.get('messages'):
                for msg in messages:
                    await message.reply_text(f'{msg}')
            await fileSender(prompt, message)
            await pluginRunner(prompt, update, context)
        else:
            print("no wrong/default command set!", flush=True, file=sys.stderr)


async def handle_message_plugin(update: Update,
                                context: ContextTypes.DEFAULT_TYPE) -> bool:
    if os.path.exists('./plugins'):
        for plugin in os.listdir('./plugins'):
            if os.path.isdir(
                    f'./plugins/{plugin}') and os.path.exists(f'./plugins/{plugin}/main.py'):
                lib = importlib.import_module(f'plugins.{plugin}.main')
                importlib.reload(lib)
                if hasattr(lib, 'handle_message'):
                    if await lib.handle_message(update=update, context=context):
                        return True
    return False


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if await handle_message_plugin(update, context):
        return
    # TODO: use `on` keyword in YAML, which tell that which of this should
    # take the command
    if update.message:
        await director(update.message, update, context)
    elif update.business_message:
        await director(update.business_message, update, context)
    else:
        print("No supported message!", flush=True, file=sys.stderr)


async def handle_callback(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE) -> None:
    if os.path.exists('./plugins'):
        for plugin in os.listdir('./plugins'):
            if os.path.isdir(
                    f'./plugins/{plugin}') and os.path.exists(f'./plugins/{plugin}/main.py'):
                lib = importlib.import_module(f'plugins.{plugin}.main')
                importlib.reload(lib)
                if hasattr(lib, 'callback'):
                    await lib.callback(update=update, context=context)


def main() -> None:
    application = Application.builder().token(os.environ.get("API_KEY")).build()

    application.add_handler(MessageHandler(filters.ALL, echo))
    application.add_handler(CallbackQueryHandler(handle_callback))

    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    print("starting...", flush=True)
    main()
