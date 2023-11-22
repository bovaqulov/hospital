from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup

from loader import db


def get_all_categories():
    categories = db.get_all_categories()
    markup = InlineKeyboardMarkup(row_width=1)
    for item in categories:
        markup.add(InlineKeyboardButton(item[1], callback_data=f"category|user|{item[0]}"))
    markup.add(InlineKeyboardButton("Main Menu", callback_data="main_menu") )
    return markup



def queoe(lst: list, category_id: int):
    markup = InlineKeyboardMarkup(row_width=1)
    for item in lst:
        items = item.split(" ")
        markup.add(InlineKeyboardButton(item, callback_data=f"{str(items[1]).lower()}|{int(category_id)}"))
    markup.add(InlineKeyboardButton("Main Menu", callback_data="main_menu"))
    return markup



def deregestration(category_id):
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(InlineKeyboardButton("Deregistration ❌", callback_data=f"deregis|{int(category_id)}"))
    markup.add(InlineKeyboardButton("Main Menu", callback_data="main_menu"))
    return markup



def main_menu():
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(InlineKeyboardButton("Main Menu", callback_data="main_menu"))
    return markup

def category_all(category_id):
    markup = InlineKeyboardMarkup(row_width=1)
    lst: list = db.get_all_patients_by_category_id(category_id)[::-1]
    for user in lst:
        text = f"{user[2]}\n {user[3]}\n"
        print(user[0])
        markup.add(InlineKeyboardButton(f"❌{text}", callback_data=f"user|{user[0]}"))
    return markup

def get_all_categories_admin():
    categories = db.get_all_categories()
    markup = InlineKeyboardMarkup(row_width=1)
    print("step 1")
    for item in categories:
        markup.add(InlineKeyboardButton(item[1], callback_data=f"category|admin|{item[0]}"))
    markup.add(InlineKeyboardButton("Main Menu", callback_data="main_menu") )
    return markup

