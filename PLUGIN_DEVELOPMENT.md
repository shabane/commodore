# Developing Plugins for Commodore

Commodore features a dynamic, hot-reloading plugin architecture. This means you can extend the bot's capabilities with Python scripts that are injected at runtime whenever a user triggers a specific command.

The best part? You can edit your plugin's code while the bot is running, and Commodore will automatically reload the newest version of your code the next time the plugin is triggered. No restarts required!

---

## 1. Directory Structure

All plugins must be stored inside the `plugins/` directory in the root of your Commodore bot. 

Each plugin is its own folder. Inside that folder, there **must** be a `main.py` file.

```text
commodore/
├── main.py
├── prompts.yaml
└── plugins/
    └── my_awesome_plugin/
        └── main.py
```

---

## 2. The `main.py` Requirements

Your plugin's `main.py` file is the entry point. Commodore looks for exactly one thing when it loads your plugin: an asynchronous function named `run`.

### The `run` Function Signature

```python
async def run(prompt: dict, update, context):
    """
    Entry point for the plugin.
    
    :param prompt: A dictionary containing the command's configuration from prompts.yaml.
    :param update: The python-telegram-bot Update object.
    :param context: The python-telegram-bot ContextTypes.DEFAULT_TYPE object.
    """
    pass
```

### Example: A Simple "Hello World" Plugin

Let's create a plugin that replies to the user, checks if they are an admin, and echoes back the configuration block from the YAML.

**`plugins/hello_world/main.py`**
```python
async def run(prompt: dict, update, context):
    # 1. Access the user's message text
    user_message = update.message.text
    
    # 2. Access the user's details
    username = update.message.from_user.username
    
    # 3. Read data passed from prompts.yaml
    admins = prompt.get("admins", [])
    
    # 4. Perform logic
    if username in admins:
        reply_text = f"Hello Admin @{username}! You said: {user_message}"
    else:
        reply_text = f"Hello @{username}! You are not an admin."
        
    # 5. Send a message back to the chat
    await update.message.reply_text(reply_text)
```

---

## 3. Registering Your Plugin

Once your plugin is written, you need to tell Commodore when to run it. You do this in `prompts.yaml`. 

To trigger the plugin, simply add its folder name to the `plugins` list of any command:

**`prompts.yaml`**
```yaml
commands:
  - key: /hello
    messages:
      - I am running the plugin now!
    plugins:
      - hello_world
    admins:
      - my_telegram_username
```

Now, whenever a user sends `/hello`, Commodore will:
1. Send the text "I am running the plugin now!".
2. Dynamically load `plugins/hello_world/main.py`.
3. Execute the `run` function, passing in the `/hello` configuration block.

---

## 4. Advanced: Accessing Commodore Core Memory

Because Commodore reloads your plugin dynamically using `importlib.reload()`, your plugin runs in an isolated namespace on each call.

If you need to access variables from the main Commodore bot (for example, reading the entire `prompts.yaml` dictionary in memory, or triggering a core reload), you can import the `__main__` module:

```python
import sys

async def run(prompt: dict, update, context):
    # Get a reference to the running commodore/main.py script
    bot_main = sys.modules.get('__main__')
    
    # Access the global prompts dictionary in memory
    all_prompts = bot_main.prompts
    
    # Example: Print all configured commands
    if 'commands' in all_prompts:
        for cmd in all_prompts['commands']:
            print(f"Loaded command: {cmd['key']}")
            
    await update.message.reply_text("Check your console!")
```

## 5. Best Practices
* **Don't block the event loop:** Make sure any network calls (like HTTP requests) or file I/O operations inside your plugin are asynchronous, or use thread pools if you have to use synchronous libraries.
* **Catch exceptions:** If your plugin crashes, it might halt the command execution. Wrap risky code in `try/except` blocks and log the errors.
* **Keep state in `context.user_data`:** If you are building multi-step conversations (like the Admin dashboard), use `context.user_data` or `context.chat_data` provided by `python-telegram-bot` to store temporary state between user messages.
