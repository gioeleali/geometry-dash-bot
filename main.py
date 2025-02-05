from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, MessageHandler, CommandHandler, ContextTypes, filters, CallbackQueryHandler, CallbackContext
import logging
import requests
from webserver import keep_alive
import os
from datetime import datetime

TOKEN = 'YOUR TOKEN'
GDB_API_URL = 'https://gdbrowser.com/api/'

logging.basicConfig(
  format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
  level=logging.INFO)
logger = logging.getLogger(__name__)

player_id = ""


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
  global player_id
  user = update.effective_user
  user_id = user.id
  if not os.path.exists(f'users/{user_id}.txt'):
    with open(f'users/{user_id}.txt', 'w') as f:
      f.write('1')
  else:
    with open(f'users/{user_id}.txt', 'r+') as f:
      count = int(f.read().strip()) + 1
      f.seek(0)
      f.write(str(count))
  message_text = update.message.text
  if message_text == "/start":
    response_message = f"*Hi {update.effective_user.first_name}!*\nSend me the username of the player to get *Geometry Dash* stats for.\n\n*API courtesy of gdbrowser.com*\n\nFor any advice [contact me](https://t.me/gioeleali)."
    await update.message.reply_text(text=response_message,
                                    disable_web_page_preview=True,
                                    parse_mode='Markdown')
  else:
    player_id = message_text
    response = requests.get(GDB_API_URL + 'profile/' + str(player_id))
    if (response):
      data = response.json()
      keyboard = []
      if data['youtube'] != None:
        keyboard.append(
          InlineKeyboardButton(
            text="▶️YouTube",
            url=f"https://youtube.com/channel/{data['youtube']}"))
      if data['twitter'] != None:
        keyboard.append(
          InlineKeyboardButton(text="🐦Twitter",
                               url=f"https://twitter.com/{data['twitter']}"))
      if data['twitch'] != None:
        keyboard.append(
          InlineKeyboardButton(text="💬Twitch",
                               url=f"https://twitch.tv/{data['twitch']}"))
      if keyboard:
        rows = [keyboard]
      else:
        rows = []
      refresh = [
        InlineKeyboardButton(text="Refresh🔄", callback_data="refresh"),
        InlineKeyboardButton(text="↪", callback_data="2")
      ]
      rows.append(refresh)
      reply_markup = InlineKeyboardMarkup(rows)
      response_message = f"*▣ {data['username']}*\n_Player ID:_ ```{data['playerID']}```\n_Account ID:_ ```{data['accountID']}```\n⭐Stars: *{data['stars']}*\n🪙Secret Coins: *{data['coins']}*\n🔘User Coins: *{data['userCoins']}*\n💎Diamonds: *{data['diamonds']}*\n😈Demons: *{data['demons']}*\n🛠️Creator Points: *{data['cp']}*"
      await update.message.reply_text(text=response_message,
                                      disable_web_page_preview=True,
                                      parse_mode='Markdown',
                                      reply_markup=reply_markup)
    else:
      await update.message.reply_text(text=f"⚠️*Error! Player not found!*",
                                      parse_mode='Markdown')


async def button(update: Update, context: CallbackContext):
  obj = datetime.now()
  d = obj.strftime("%d-%m-%Y")
  h = obj.strftime("%H:%M:%S")
  global player_id
  query = update.callback_query
  await query.answer()
  if query.data == "refresh":
    response = requests.get(GDB_API_URL + 'profile/' + str(player_id))
    data = response.json()
    keyboard = []
    if data['youtube'] != None:
      keyboard.append(
        InlineKeyboardButton(
          text="▶️YouTube",
          url=f"https://youtube.com/channel/{data['youtube']}"))
    if data['twitter'] != None:
      keyboard.append(
        InlineKeyboardButton(text="🐦Twitter",
                             url=f"https://twitter.com/{data['twitter']}"))
    if data['twitch'] != None:
      keyboard.append(
        InlineKeyboardButton(text="💬Twitch",
                             url=f"https://twitch.tv/{data['twitch']}"))
    if keyboard:
      rows = [keyboard]
    else:
      rows = []
    refresh = [
      InlineKeyboardButton(text="Refresh🔄", callback_data="refresh"),
      InlineKeyboardButton(text="↪", callback_data="2")
    ]
    rows.append(refresh)
    reply_markup = InlineKeyboardMarkup(rows)
    response_message = f"*▣ {data['username']}*\n_Player ID:_ ```{data['playerID']}```\n_Account ID:_ ```{data['accountID']}```\n⭐Stars: *{data['stars']}*\n🪙Secret Coins: *{data['coins']}*\n🔘User Coins: *{data['userCoins']}*\n💎Diamonds: *{data['diamonds']}*\n😈Demons: *{data['demons']}*\n🛠️Creator Points: *{data['cp']}*\n\n_Updated {d} at {h}_"
    await query.edit_message_text(text=response_message,
                                  disable_web_page_preview=True,
                                  parse_mode='Markdown',
                                  reply_markup=reply_markup)
  elif query.data == "refresh2":
    response = requests.get(GDB_API_URL + 'profile/' + str(player_id))
    data = response.json()
    keyboard = []
    if data['youtube'] != None:
      keyboard.append(
        InlineKeyboardButton(
          text="▶️YouTube",
          url=f"https://youtube.com/channel/{data['youtube']}"))
    if data['twitter'] != None:
      keyboard.append(
        InlineKeyboardButton(text="🐦Twitter",
                             url=f"https://twitter.com/{data['twitter']}"))
    if data['twitch'] != None:
      keyboard.append(
        InlineKeyboardButton(text="💬Twitch",
                             url=f"https://twitch.tv/{data['twitch']}"))
    if keyboard:
      rows = [keyboard]
    else:
      rows = []
    refresh = [
      InlineKeyboardButton(text="Refresh🔄", callback_data="refresh2"),
      InlineKeyboardButton(text="↩", callback_data="1")
    ]
    rows.append(refresh)
    reply_markup = InlineKeyboardMarkup(rows)
    if (data['glow'] == True):
      glow = "Yes"
    else:
      glow = "No"
    response_message = f"\n\nIcon nº*{data['icon']}*\nShip nº*{data['ship']}*\nBall nº*{data['ball']}*\nUfo nº*{data['ufo']}*\nWave nº*{data['wave']}*\nRobot nº*{data['robot']}*\nSpider nº*{data['spider']}*\nDeath Effect nº*{data['deathEffect']}*\nColor 1 nº*{data['col1']}*\nColor 2 nº*{data['col2']}*\nGlow: *{glow}*\n\n_Updated {d} at {h}_"
    await query.edit_message_text(text=response_message,
                                  disable_web_page_preview=True,
                                  parse_mode='Markdown',
                                  reply_markup=reply_markup)
  elif query.data == "1":
    response = requests.get(GDB_API_URL + 'profile/' + str(player_id))
    data = response.json()
    keyboard = []
    if data['youtube'] != None:
      keyboard.append(
        InlineKeyboardButton(
          text="▶️YouTube",
          url=f"https://youtube.com/channel/{data['youtube']}"))
    if data['twitter'] != None:
      keyboard.append(
        InlineKeyboardButton(text="🐦Twitter",
                             url=f"https://twitter.com/{data['twitter']}"))
    if data['twitch'] != None:
      keyboard.append(
        InlineKeyboardButton(text="💬Twitch",
                             url=f"https://twitch.tv/{data['twitch']}"))
    if keyboard:
      rows = [keyboard]
    else:
      rows = []
    refresh = [
      InlineKeyboardButton(text="Refresh🔄", callback_data="refresh"),
      InlineKeyboardButton(text="↪", callback_data="2")
    ]
    rows.append(refresh)
    reply_markup = InlineKeyboardMarkup(rows)
    response_message = f"*▣ {data['username']}*\n_Player ID:_ ```{data['playerID']}```\n_Account ID:_ ```{data['accountID']}```\n⭐Stars: *{data['stars']}*\n🪙Secret Coins: *{data['coins']}*\n🔘User Coins: *{data['userCoins']}*\n💎Diamonds: *{data['diamonds']}*\n😈Demons: *{data['demons']}*\n🛠️Creator Points: *{data['cp']}*"
    await query.edit_message_text(text=response_message,
                                  disable_web_page_preview=True,
                                  parse_mode='Markdown',
                                  reply_markup=reply_markup)
  elif query.data == "2":
    response = requests.get(GDB_API_URL + 'profile/' + str(player_id))
    data = response.json()
    keyboard = []
    if data['youtube'] != None:
      keyboard.append(
        InlineKeyboardButton(
          text="▶️YouTube",
          url=f"https://youtube.com/channel/{data['youtube']}"))
    if data['twitter'] != None:
      keyboard.append(
        InlineKeyboardButton(text="🐦Twitter",
                             url=f"https://twitter.com/{data['twitter']}"))
    if data['twitch'] != None:
      keyboard.append(
        InlineKeyboardButton(text="💬Twitch",
                             url=f"https://twitch.tv/{data['twitch']}"))
    if keyboard:
      rows = [keyboard]
    else:
      rows = []
    refresh = [
      InlineKeyboardButton(text="Refresh🔄", callback_data="refresh2"),
      InlineKeyboardButton(text="↩", callback_data="1")
    ]
    rows.append(refresh)
    reply_markup = InlineKeyboardMarkup(rows)
    if (data['glow'] == True):
      glow = "Yes"
    else:
      glow = "No"
    response_message = f"\n\nIcon nº*{data['icon']}*\nShip nº*{data['ship']}*\nBall nº*{data['ball']}*\nUfo nº*{data['ufo']}*\nWave nº*{data['wave']}*\nRobot nº*{data['robot']}*\nSpider nº*{data['spider']}*\nDeath Effect nº*{data['deathEffect']}*\nColor 1 nº*{data['col1']}*\nColor 2 nº*{data['col2']}*\nGlow: *{glow}*"
    await query.edit_message_text(text=response_message,
                                  disable_web_page_preview=True,
                                  parse_mode='Markdown',
                                  reply_markup=reply_markup)


async def users(update: Update, context: ContextTypes.DEFAULT_TYPE):
  user = update.effective_user
  if user.id != 158042764:
    return
  num_users = len([f for f in os.listdir('users') if f.endswith('.txt')])
  await update.message.reply_text(text=f"Users: *{num_users}*",
                                  parse_mode='Markdown')


def main():
  app = Application.builder().token(TOKEN).build()
  app.add_handler(CommandHandler("start", start))
  app.add_handler(CommandHandler("user", users))
  app.add_handler(MessageHandler(filters.TEXT, start))
  app.add_handler(CallbackQueryHandler(button))
  print("Loading...")
  app.run_polling()


keep_alive()

if __name__ == "__main__":
  main()
