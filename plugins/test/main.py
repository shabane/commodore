# This plugin is just to show you how things are work
async def run(*args, **kwargs):
    update = kwargs.get("update")
    prompts = kwargs.get("prompt")
    print("telegram message instance: ", update)
    print('====')
    print("called prompt: ", prompts)
    await update.reply_text('Hello, Test Plugin!')
    