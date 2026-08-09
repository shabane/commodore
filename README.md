# Commodore

A lightweight, declarative, and plugin-driven Telegram Bot framework built with Python and `python-telegram-bot`.

## Overview
Commodore makes it incredibly easy to build Telegram bots without writing massive `if/else` statement blocks for every command. Instead, you define how your bot behaves using a simple, human-readable `prompts.yaml` configuration file. 

Whenever a user triggers a command, Commodore automatically sends the configured text messages, photos, audios, and documents associated with that command!

## Key Features
* **Declarative Configuration:** Define all bot interactions in `prompts.yaml`. No need to hardcode text or media paths in Python.
* **Media Support:** Easily send multiple texts, photos, videos, audios (including voice messages), and documents per command.
* **Dynamic Plugin System:** Extend your bot's logic using plugins. Plugins are dynamically imported and **hot-reloaded**, meaning you can modify your plugin code while the bot is running without needing to restart it!
* **Global Fallbacks:** Gracefully handle unrecognized commands using a customizable `wrong_command` configuration.
* **Admin Ecosystem:** Integrate seamlessly with the `commodorAdmin` plugin to edit your configuration dynamically from within the chat.

## Getting Started

### 1. Requirements
* Python 3.10+
* `python-telegram-bot` v22+
* `pyyaml`

### 2. Setup
1. Clone the repository.
2. Create a virtual environment and install dependencies:
   ```bash
   python -m venv .env
   source .env/bin/activate
   pip install python-telegram-bot pyyaml
   ```
3. Set your Bot Token as an environment variable:
   ```bash
   export API_KEY="your_bot_token_here"
   ```
4. Run the bot:
   ```bash
   ./main.py
   ```

### 3. Configuration (`prompts.yaml`)
Your `prompts.yaml` file is the heart of the bot. Here is a sample structure:

```yaml
commands:
  - key: /start
    messages:
      - Welcome to my bot!
  - key: /sample
    messages:
      - Here are some files!
    photos:
      - ./assets/sample.jpg
    audios:
      - ./assets/sample.ogg
    plugins:
      - some_plugin_name
```

## Plugin Architecture
Plugins are stored in the `./plugins/` directory. Each plugin must be a folder containing a `main.py` file with an async `run(prompt, update, context)` function. 

You can configure a command in `prompts.yaml` to trigger one or more plugins when the command is sent by the user.

## Available Plugins
You can easily extend Commodore's functionality by dropping existing plugins into your `plugins/` directory.

Here are some official plugins you can use:
* [**CommodorAdmin**](https://github.com/shabane/commodorAdmin) - An interactive Telegram chat dashboard that allows admins to dynamically edit the bot's commands, text messages, and media configurations in real time.
* [**CommodoreHttpPostCall**](https://github.com/shabane/commodoreHttpPostCall) - A utility plugin for seamlessly making HTTP POST requests triggered by bot commands.

---
*Built with ❤️ using the Commodore framework.*
