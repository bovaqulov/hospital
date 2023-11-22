from telebot.types import CallbackQuery

from loader import  bot
from keyboards.default import *
from keyboards.inlines import *
from config import ADMINS


class AdminCallMessage():
    def __init__(s, call: CallbackQuery):
        s.data = call.data
        s.chat_id = call.message.chat.id
        s.msg_id = call.message.id
        s.keyboard_list = call.message.reply_markup.keyboard
        s.call = call
        print()

    def manager(s):
        data = s.data

        if data == 'main_menu':
            return s.reaction_main_menu()

        if "category|admin|" in data:
            return s.reaction_category(data)

        if "user|" in data:
            return s.reaction_unregestrate(data)

        if data == True:
            return bot.send_message(s.chat_id, "Salom")

    def reaction_unregestrate(s, data):
        admin_btn = generate_btn([
            "Total patients",
            "Message patients",
            "Delete patients from queues"])
        bot.delete_message(s.chat_id, s.msg_id)
        datas = data.split("|")
        db.delete_patient_by_telegam_id(datas[-1])
        bot.send_message(s.chat_id, f"You have deleted",reply_markup=admin_btn)
        bot.send_message(chat_id=datas[-1], text=f"You have been removed from the register by the hospital")

    def reaction_category(s, data):
        print(data)
        category = data.split("|")
        bot.delete_message(s.chat_id, s.msg_id)
        if not db.get_all_patients_by_category_id(category[-1]):
            bot.send_message(s.chat_id, 'There are no patients on this route')
        else:
            bot.send_message(s.chat_id, f'Click to unsubscribe',reply_markup=category_all(category[-1]))

    def reaction_main_menu(s):
        admin_btn = generate_btn([
            "Total patients",
            "Message patients",
            "Delete patients from queues"])
        bot.delete_message(s.chat_id, s.msg_id)
        bot.send_message(s.chat_id, 'Main Menu', reply_markup=admin_btn)

@bot.callback_query_handler(func=lambda call: bool(call) == True, chat_id=ADMINS)
def main(call: CallbackQuery):
    try:
        AdminCallMessage(call=call).manager()
    except Exception as e:
        bot.send_message(AdminCallMessage(call=call).chat_id, f"ERROR: {e}")
        print(F"ERROR: {e}")
