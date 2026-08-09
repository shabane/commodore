import os
import sys
import zipfile
import tempfile

async def run(prompt: dict, update, context):
    # 1. Verify Authorization
    user_id = update.effective_user.id
    username = update.effective_user.username
    admins = prompt.get("admins", [])
    
    if str(user_id) not in admins and username not in admins:
        return
    
    # 2. Get active config from core memory
    bot_main = sys.modules.get('__main__')
    all_prompts = getattr(bot_main, 'prompts', {})
    
    active_files = set()
    prompts_file = os.environ.get("PROMPTS_FILE", "./prompts.yaml")
    
    # Always include the YAML config itself
    active_files.add(prompts_file)
    
    # Extract all media file paths currently configured
    if 'commands' in all_prompts:
        for cmd in all_prompts['commands']:
            for attr in ['photos', 'audios', 'videos', 'documents']:
                if attr in cmd:
                    for f_path in cmd[attr]:
                        active_files.add(f_path)
                        
    # 3. Create a temporary zip file
    try:
        temp_dir = tempfile.mkdtemp()
        zip_path = os.path.join(temp_dir, 'commodore_backup.zip')
        
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for file_path in active_files:
                if os.path.exists(file_path):
                    # Preserve the relative folder structure (e.g., assets/...)
                    arcname = os.path.relpath(file_path, start='.')
                    zipf.write(file_path, arcname)
                    
        # 4. Send the zip file back to the admin
        caption = prompt.get("backup_caption", "Backup complete!")
        with open(zip_path, 'rb') as f:
            await update.message.reply_document(
                document=f,
                filename="commodore_backup.zip",
                caption=caption
            )
            
    except Exception as e:
        await update.message.reply_text(f"Error generating backup: {e}")
    finally:
        # 5. Cleanup the temporary zip file
        if 'zip_path' in locals() and os.path.exists(zip_path):
            os.remove(zip_path)
        if 'temp_dir' in locals() and os.path.exists(temp_dir):
            os.rmdir(temp_dir)
