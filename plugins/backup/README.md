# CommodorBackup Plugin

A lightweight, hot-reloadable plugin for the [Commodore](https://github.com/shabane/commodore) Telegram bot framework.

This plugin allows authorized administrators to easily generate and download a complete, portable backup of the bot. It compiles your active `prompts.yaml` configuration along with all the active media files referenced within it into a neat `.zip` archive, leaving behind any orphaned or deleted assets.

## Features
- **Dynamic Archiving:** Zips up `prompts.yaml` and active photos, audios, videos, and documents on the fly.
- **Smart Filtering:** Only includes files that are currently used in the active `prompts.yaml`, ignoring old unused files in the `assets/` directory.
- **Secure:** Enforces admin authorization to ensure only designated users can download the backup.
- **Customizable:** Fully declarative, allowing you to configure the success message and backup file caption from your YAML file.

## Installation

To install this plugin into your Commodore instance:

1. Clone this repository into the `plugins/` directory of your Commodore project:
   ```bash
   git clone git@github.com:shabane/commodoreBackup.git plugins/backup
   ```
   *Alternatively, you can clone it elsewhere and symlink it into the `plugins/` directory.*

## Configuration

To activate the plugin, simply define a command mapping in your core `prompts.yaml` file. You can configure the `messages` array for the "loading" state, and the `backup_caption` for the final zip file text.

```yaml
commands:
  - key: /backup
    messages:
      - Generating backup archive... Please wait a moment.
    backup_caption: Here is a backup of your current config and all active media files!
    admins:
      - your_telegram_username
    plugins:
      - backup
```

## Usage
Simply send `/backup` to your bot on Telegram. If you are authorized in the `admins` list, the bot will instantly compile the zip file and reply to you with the document!
