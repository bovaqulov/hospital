from telebot.types import ReplyKeyboardMarkup, KeyboardButton

from loader import db

def main_menu_btn():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    category = [
        "Directions 🗒",
        "Contact the hospital ☎️",
        "View queues 👀",
        "About Hospital 📓",
        "Locations 📍"]
    for i in category:
        markup.add(
        KeyboardButton(i),
    )
    return markup

def register_btn():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton("Regestiration ✍️"))
    return markup

def send_contact_btn():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton("Send contact 📲", request_contact=True))
    return markup

def submit_btn():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton("True ✅"), KeyboardButton("Mistake 🔁"))
    return markup


def categories_btn():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    for item in db.get_all_categories():
        markup.add(KeyboardButton(item))
    markup.add(KeyboardButton("Asosiy menyu"))
    return markup


def generate_btn(lst: list):
    markup = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    for item in lst:

        markup.add(KeyboardButton(item.capitalize()))
    return markup