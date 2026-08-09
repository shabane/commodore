import os
import sys
import yaml
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

# We need to access main.py from the commodore directory to access `prompts` and `load_prompts`
# Since the bot is executed as `./main.py`, the module is loaded as `__main__`
bot_main = sys.modules.get('__main__')


def is_admin(user_id: int, username: str, prompt: dict) -> bool:
    admins = prompt.get("admins", [])
    return username in admins or str(user_id) in admins


async def handle_message(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE) -> bool:
    state = context.user_data.get('admin_state')
    if not state:
        return False

    text = update.message.text
    attr = state.get('attr') if isinstance(state, dict) else None

    cancel_cmd = bot_main.prompts.get("admin_cancel_command")
    if cancel_cmd and text == cancel_cmd:
        context.user_data['admin_state'] = None
        await update.message.reply_text("Operation cancelled.")
        await show_main_menu(update.message, context)
        return True

    if attr in ["photos", "audios", "documents", "videos"]:
        file_id = None
        ext = ""

        if attr == "photos":
            if update.message.photo:
                file_id = update.message.photo[-1].file_id
                ext = ".jpg"
            else:
                await update.message.reply_text("Please upload a valid photo.")
                return False
        elif attr == "audios":
            if update.message.audio:
                file_id = update.message.audio.file_id
                ext = ".mp3"
            elif update.message.voice:
                file_id = update.message.voice.file_id
                ext = ".ogg"
            else:
                await update.message.reply_text("Please upload a valid audio or voice message.")
                return False
        elif attr == "videos":
            if update.message.video:
                file_id = update.message.video.file_id
                ext = ".mp4"
            elif update.message.video_note:
                file_id = update.message.video_note.file_id
                ext = ".mp4"
            elif update.message.animation:
                file_id = update.message.animation.file_id
                ext = ".mp4"
            else:
                await update.message.reply_text("Please upload a valid video or GIF.")
                return False
        elif attr == "documents":
            if update.message.document:
                file_id = update.message.document.file_id
                ext = os.path.splitext(update.message.document.file_name)[
                    1] if update.message.document.file_name else ""
            else:
                await update.message.reply_text("Please upload a valid document/file.")
                return False

        if file_id:
            try:
                file = await context.bot.get_file(file_id)
                assets_dir = os.environ.get("ASSETS_DIR", "./assets")
                os.makedirs(assets_dir, exist_ok=True)
                path = os.path.join(assets_dir, f"{file_id}{ext}")
                await file.download_to_drive(path)
                text = path
            except Exception as e:
                await update.message.reply_text(f"Error saving file: {e}")
                return False
    else:
        if not text:
            await update.message.reply_text("Please type text instead of uploading a file.")
            return False

    if state == 'waiting_new_cmd':
        commands = bot_main.prompts.get("commands", [])
        commands.append({"key": text})
        idx = len(commands) - 1
        save_and_reload()
        context.user_data['admin_state'] = None
        await update.message.reply_text(f"Command '{text}' created! Select a category below to add content to it:")
        await show_edit_menu(update.message, idx)
        return True

    if isinstance(state, dict) and state.get('action') == 'add_attr':
        idx = state['idx']
        attr = state['attr']
        cmd = bot_main.prompts.get("commands", [])[idx]
        if attr not in cmd:
            cmd[attr] = []
        cmd[attr].append(text)
        save_and_reload()
        context.user_data['admin_state'] = None
        await update.message.reply_text(f"Added to {attr}.")
        await show_attr_menu(update.message, idx, attr)
        return True

    if isinstance(state, dict) and state.get('action') == 'edit_attr':
        idx = state['idx']
        attr = state['attr']
        item_idx = state['itemIdx']
        cmd = bot_main.prompts.get("commands", [])[idx]
        cmd[attr][item_idx] = text
        save_and_reload()
        context.user_data['admin_state'] = None
        await update.message.reply_text(f"Updated {attr}.")
        await show_attr_menu(update.message, idx, attr)
        return True

    return False


async def run(*args, **kwargs):
    update = kwargs.get("update")
    context = kwargs.get("context")
    prompt = kwargs.get("prompt")

    user = update.message.from_user
    if not is_admin(user.id, user.username, prompt):
        await update.message.reply_text("You are not authorized to use this command.")
        return

    # Store prompt config in context for callback use
    context.bot_data['admin_prompt'] = prompt
    await show_main_menu(update.message, context)


async def show_main_menu(message, context):
    if not bot_main:
        await message.reply_text("Error: Cannot import bot main module.")
        return

    commands = bot_main.prompts.get("commands", [])
    keyboard = []

    for i, cmd in enumerate(commands):
        key = cmd.get("key", f"Unknown {i}")
        keyboard.append([InlineKeyboardButton(
            f"Edit: {key}", callback_data=f"admin_edit_{i}")])

    keyboard.append([InlineKeyboardButton(
        "➕ Add New Command", callback_data="admin_add")])

    reply_markup = InlineKeyboardMarkup(keyboard)
    if message.from_user and message.from_user.is_bot:
        try:
            await message.edit_text("Admin Menu: Select a command to edit or add a new one.", reply_markup=reply_markup)
        except Exception:
            await message.reply_text("Admin Menu: Select a command to edit or add a new one.", reply_markup=reply_markup)
    else:
        await message.reply_text("Admin Menu: Select a command to edit or add a new one.", reply_markup=reply_markup)


async def callback(*args, **kwargs):
    update = kwargs.get("update")
    context = kwargs.get("context")

    query = update.callback_query
    if not query or not query.data.startswith("admin_"):
        return

    await query.answer()

    # check auth
    prompt = context.bot_data.get('admin_prompt', {})
    if not is_admin(query.from_user.id, query.from_user.username, prompt):
        await query.edit_message_text("Unauthorized.")
        return

    data = query.data

    if data == "admin_menu":
        await show_main_menu(query.message, context)
        return

    if data.startswith("admin_edit_"):
        idx = int(data.split("_")[-1])
        await show_edit_menu(query.message, idx)
        return

    if data.startswith("admin_del_"):
        idx = int(data.split("_")[-1])
        await delete_command(query.message, idx)
        return

    if data.startswith("admin_attr_"):
        parts = data.split("_")
        idx = int(parts[2])
        attr = parts[3]
        await show_attr_menu(query.message, idx, attr)
        return

    if data.startswith("admin_addattr_"):
        parts = data.split("_")
        idx = int(parts[2])
        attr = parts[3]
        context.user_data['admin_state'] = {
            'action': 'add_attr', 'idx': idx, 'attr': attr}
        cancel_cmd = bot_main.prompts.get("admin_cancel_command")
        if attr in ["photos", "audios", "documents", "videos"]:
            msg = f"Please upload the new {attr[:-1]} file"
        else:
            msg = f"Please type the new {attr}"
        
        if cancel_cmd:
            msg += f" (or type {cancel_cmd} to cancel):"
        else:
            msg += ":"
            
        await query.edit_message_text(msg)
        return

    if data.startswith("admin_delattr_"):
        parts = data.split("_")
        idx = int(parts[2])
        attr = parts[3]
        item_idx = int(parts[4])
        cmd = bot_main.prompts.get("commands", [])[idx]
        if attr in cmd and 0 <= item_idx < len(cmd[attr]):
            del cmd[attr][item_idx]
            save_and_reload()
        await show_attr_menu(query.message, idx, attr)
        return

    if data.startswith("admin_editattr_"):
        parts = data.split("_")
        idx = int(parts[2])
        attr = parts[3]
        item_idx = int(parts[4])
        context.user_data['admin_state'] = {
            'action': 'edit_attr',
            'idx': idx,
            'attr': attr,
            'itemIdx': item_idx}
        cancel_cmd = bot_main.prompts.get("admin_cancel_command")
        if attr in ["photos", "audios", "documents", "videos"]:
            msg = f"Please upload the replacement {attr[:-1]} file"
        else:
            msg = f"Please type the replacement {attr}"
            
        if cancel_cmd:
            msg += f" (or type {cancel_cmd} to cancel):"
        else:
            msg += ":"
            
        await query.edit_message_text(msg)
        return

    if data == "admin_add":
        context.user_data['admin_state'] = 'waiting_new_cmd'
        cancel_cmd = bot_main.prompts.get("admin_cancel_command")
        msg = "Please type the new command key (e.g. /mycmd)"
        if cancel_cmd:
            msg += f"\n(Or type {cancel_cmd} to cancel):"
        else:
            msg += ":"
        await query.edit_message_text(msg)
        return


async def show_edit_menu(message, idx):
    cmd = bot_main.prompts.get("commands", [])[idx]
    key = cmd.get("key", "Unknown")

    text = f"Editing Command: {key}\n\n"
    text += f"💬 Messages: {len(cmd.get('messages', []))}\n"
    text += f"📷 Photos: {len(cmd.get('photos', []))}\n"
    text += f"🎵 Audios: {len(cmd.get('audios', []))}\n"
    text += f"📄 Documents: {len(cmd.get('documents', []))}\n"
    text += f"🎥 Videos: {len(cmd.get('videos', []))}\n"
    text += f"🔌 Plugins: {len(cmd.get('plugins', []))}\n"

    keyboard = [
        [
            InlineKeyboardButton("💬 Messages", callback_data=f"admin_attr_{idx}_messages"),
            InlineKeyboardButton("📷 Photos", callback_data=f"admin_attr_{idx}_photos")
        ],
        [
            InlineKeyboardButton("🎵 Audios", callback_data=f"admin_attr_{idx}_audios"),
            InlineKeyboardButton("📄 Documents", callback_data=f"admin_attr_{idx}_documents")
        ],
        [
            InlineKeyboardButton("🎥 Videos", callback_data=f"admin_attr_{idx}_videos"),
            InlineKeyboardButton("🔌 Plugins", callback_data=f"admin_attr_{idx}_plugins")
        ],
        [InlineKeyboardButton("❌ Delete Command", callback_data=f"admin_del_{idx}")],
        [InlineKeyboardButton("🔙 Back to Menu", callback_data="admin_menu")]
    ]

    if message.from_user and message.from_user.is_bot:
        try:
            await message.edit_text(text, reply_markup=InlineKeyboardMarkup(keyboard))
        except Exception:
            await message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard))
    else:
        await message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard))


async def show_attr_menu(message, idx, attr):
    cmd = bot_main.prompts.get("commands", [])[idx]
    key = cmd.get("key", "Unknown")
    items = cmd.get(attr, [])

    text = f"Command: {key}\nManaging: {attr}\n\n"
    keyboard = []

    for i, item in enumerate(items):
        preview = item[:20] + "..." if len(item) > 20 else item
        keyboard.append([InlineKeyboardButton("❌",
                                              callback_data=f"admin_delattr_{idx}_{attr}_{i}"),
                         InlineKeyboardButton(f"✏️ {preview}",
                         callback_data=f"admin_editattr_{idx}_{attr}_{i}")])

    keyboard.append([InlineKeyboardButton("➕ Add New",
                                          callback_data=f"admin_addattr_{idx}_{attr}")])
    keyboard.append([InlineKeyboardButton(
        "🔙 Back to Command", callback_data=f"admin_edit_{idx}")])

    if message.from_user and message.from_user.is_bot:
        try:
            await message.edit_text(text, reply_markup=InlineKeyboardMarkup(keyboard))
        except Exception:
            await message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard))
    else:
        await message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard))


async def delete_command(message, idx):
    cmds = bot_main.prompts.get("commands", [])
    if 0 <= idx < len(cmds):
        del cmds[idx]
        save_and_reload()
        # Since we modified the message, we can just show the main menu instead
        # of sending a new text
        await show_main_menu(message, None)


def save_and_reload():
    prompts_file = os.environ.get("PROMPTS_FILE", "./prompts.yaml")
    # if it's run from commodorAdmin, PROMPTS_FILE might not be set right unless passed.
    # We will assume PROMPTS_FILE is passed correctly to the python process.
    if not os.path.isabs(prompts_file):
        prompts_file = os.path.join(
            os.path.abspath(
                os.path.dirname(
                    bot_main.__file__)),
            prompts_file)

    with open(prompts_file, 'w') as f:
        yaml.dump(
            bot_main.prompts,
            f,
            default_flow_style=False,
            sort_keys=False)
    bot_main.load_prompts()
