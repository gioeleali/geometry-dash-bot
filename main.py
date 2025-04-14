import logging
import os
from telegram import Bot, Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler, MessageHandler,
    ContextTypes, filters
)
from fpdf import FPDF

# Logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Bot token da ENV
TOKEN = os.getenv("BOT_TOKEN")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton(text="Crea PDF", callback_data="start")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        'Ciao!\nPremi sotto per iniziare un nuovo rapporto.',
        reply_markup=reply_markup
    )


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "start":
        context.user_data.clear()
        await query.message.edit_text(
            "Inserisci l'oggetto da inserire:",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton(text="◀️", callback_data="back")]]
            )
        )

    elif data == "qty":
        await query.message.edit_text(
            "Inserisci la quantità:",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton(text="◀️", callback_data="back")]]
            )
        )

    elif data == "y":
        obj = context.user_data.get("obj", "N/A")
        qty = context.user_data.get("qty", "N/A")

        pdf = FPDF()
        pdf.add_page()
        pdf.set_font('Arial', 'B', 16)
        pdf.cell(40, 10, 'Oggetto: ' + obj)
        pdf.ln()
        pdf.cell(40, 10, 'Quantità: ' + qty)
        pdf.output('rapporto.pdf', 'F')

        with open('rapporto.pdf', 'rb') as f:
            await query.message.reply_document(document=f, caption="Ecco il PDF")

    elif data == "another":
        await query.message.edit_text(
            "Inserisci il nuovo oggetto:",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton(text="◀️", callback_data="back")]]
            )
        )

    elif data == "back":
        await query.message.edit_text("Operazione annullata. /start per ripartire")


async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if "obj" not in context.user_data:
        context.user_data["obj"] = text
        await update.message.reply_text(
            "Oggetto salvato. Ora inserisci la quantità:",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton(text="◀️", callback_data="back")]]
            )
        )
    elif "qty" not in context.user_data:
        context.user_data["qty"] = text
        await update.message.reply_text(
            "Quantità salvata. Creare il PDF?",
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton(text="✅ Sì", callback_data="y"),
                    InlineKeyboardButton(text="➕ Altro oggetto", callback_data="another")
                ],
                [InlineKeyboardButton(text="◀️", callback_data="back")]
            ])
        )
    else:
        await update.message.reply_text("Usa /start per iniziare un nuovo report.")


async def count(update: Update, context: ContextTypes.DEFAULT_TYPE):
    bot: Bot = context.bot
    updates = await bot.get_updates(offset=-1)
    users = {u.message.from_user.id for u in updates if u.message}
    await update.message.reply_text(
        f"Numero di utenti: *{len(users)}*", parse_mode='Markdown'
    )


# App
app = Application.builder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("count", count))
app.add_handler(CallbackQueryHandler(button))
app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_text))

print("Bot in esecuzione...")
app.run_polling()
