# CommodorAdmin Plugin

A powerful, interactive dashboard plugin for the **Commodore** Telegram bot framework. 

This plugin allows authorized administrators to dynamically add, edit, and delete bot commands and their associated text/media responses directly from within the Telegram chat environment—no coding or file editing required!

## Features
* **In-Chat Configuration Editing:** Add or modify commands on the fly. Changes are saved back to the core `prompts.yaml` file automatically.
* **Full CRUD Operations:** Support for adding, deleting, and editing text messages, photos, audios (including voice notes), videos (including GIFs/Video Notes), and documents for any command.
* **Strict Media Validation:** Uploads are heavily validated. You cannot accidentally save a GIF to an audio file list!
* **Dynamic Cancellation:** Supports aborting ongoing edits seamlessly using a configurable cancel command (e.g., `/cancel`).
* **Environment-Aware Storage:** Saves uploaded media safely to a configurable assets directory.

## Installation & Setup

1. Copy or symlink this directory into the `plugins/` directory of your Commodore core bot folder under the name `admin`.
   ```bash
   ln -s /path/to/commodorAdmin /path/to/commodore/plugins/admin
   ```
2. In your Commodore core `prompts.yaml`, ensure you have an admin command defined that loads this plugin, and lists your authorized username(s) or ID(s):
   ```yaml
   commands:
     - key: /admin
       admins:
         - your_telegram_username
       plugins:
         - admin
   ```
3. Configure your assets directory (optional). By default, media uploaded via the chat will be saved to `./assets`. You can override this by exporting an environment variable before starting the Commodore bot:
   ```bash
   export ASSETS_DIR="/path/to/custom/assets/folder"
   ```

## Usage
Simply send `/admin` to your bot. If your username is authorized, you will be greeted with an interactive inline keyboard.

From the menu, you can:
- **Select a command** to view its current attributes.
- **Add new texts or media files** by clicking the relevant `[+]` button and uploading the file/text directly in the chat.
- **Edit or delete** existing texts and files.
- **Create entirely new commands** by clicking the "Add Command" button.

### Cancelling Operations
If you are prompted to type text or upload a file and you wish to abort the operation, you can type your configured `admin_cancel_command` (which defaults to `/cancel` if you set it in your `prompts.yaml`).

## Architecture Notes
Because this operates as a plugin within the Commodore framework, the `main.py` file exports an async `run(prompt, update, context)` function. The Commodore core uses `importlib.reload()` when invoking plugins, which means you can edit the code of this plugin and the bot will instantly use the newest version the next time the command is triggered.
