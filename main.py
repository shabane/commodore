from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message:
        await update.message.reply_text(f"not business, ha? {update.message.text}")
    elif update.business_message:
        await update.business_message.reply_text(update.business_message.text)


def main() -> None:
    application = Application.builder().token("7898989405:AAH_WGE1nfJ09DLY1-DyGHaxL3CMud1hln4").build()

    application.add_handler(MessageHandler(filters.TEXT, echo))

    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
