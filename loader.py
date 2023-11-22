from telebot import TeleBot, custom_filters
from telebot.storage import StateMemoryStorage
from telebot.types import BotCommand

from config import *
from database import DataBase

bot = TeleBot(TOKEN, state_storage=StateMemoryStorage(), use_class_middlewares=True, parse_mode="html")

bot.add_custom_filter(custom_filters.StateFilter(bot))
bot.set_my_commands(commands=[
    BotCommand('start', 'Usefull Bot')])

db = DataBase(dbname=DB_NAME, password=DB_PASSWORD, host=DB_HOST, user=DB_USER)

bot.add_custom_filter(custom_filters.ChatFilter())


