from telebot.types import CallbackQuery

from loader import bot
from keyboards.default import *
from keyboards.inlines import *



class CallMessage():
    def __init__(s, call: CallbackQuery):
        s.data = call.data
        s.chat_id = call.message.chat.id
        s.msg_id = call.message.id
        s.keyboard_list = call.message.reply_markup.keyboard
        s.call = call

    def manager(s):
        data = s.data

        if data == 'main_menu':
            return s.reaction_main_menu()

        if data == True:
            return bot.send_message(s.chat_id, "Salom")

        if "category|user" in data:
            return s.reaction_category(data)

        if "queue" in data:
            return s.reaction_queue(data)

        if "write" in data:
            return s.reaction_write(data)

        if "deregis" in data:
            return s.deregistration(data)


    def reaction_category(s, data):
        category = data.split("|")
        lst: list = ["🔍 Queue", "📝 Write"]
        bot.delete_message(s.chat_id, s.msg_id)
        bot.send_message(s.chat_id, 'Choose please, 🔍 Queue or 📝 Write"', reply_markup=queoe(lst, category[-1]))


    def reaction_queue(s, data):
        category = data.split("|")
        lst_1: list = ["🔍 Queue", "📝 Write"]
        id_category = int(category[1])
        lst: list = db.get_all_patients_by_category_id(id_category)[::-1]
        bot.delete_message(s.chat_id, s.msg_id)
        count = 1
        for user in lst:
            if s.chat_id == user[0]:
                text = f"<b><u>{count} - patient:\n" \
                   f"Name: {user[1]}\n" \
                   f"Surname: {user[2]}\n" \
                   f"phone number: {user[3][0:6]}***{user[3][-4:]}</u></b>"
                bot.send_message(s.chat_id, text)
            else:
                text = f"{count} - patient:\n" \
                       f"Name: {user[1]}\n" \
                       f"Surname: {user[2]}\n" \
                       f"phone number: {user[3][0:6]}***{user[3][-4:]}\n"


                bot.send_message(s.chat_id, text)
            count += 1



        bot.send_message(s.chat_id, 'Choose please, 🔍 Queue or 📝 Write"', reply_markup=queoe(lst_1, category[1]))




    def reaction_write(s, data):
        write = data.split("|")
        id_category = int(write[1])
        user_chat_id = s.chat_id

        if db.get_telegram_id_by_category_id_from_patients(user_chat_id):
            category_name = db.get_category_by_telegram_id(user_chat_id)
            bot.delete_message(s.chat_id, s.msg_id)
            bot.send_message(s.chat_id, f'You are already registered 🚫: For {category_name}', reply_markup=deregestration(id_category))
        else:
            db.insert_patients(user_chat_id, id_category)
            bot.delete_message(s.chat_id, s.msg_id)
            bot.send_message(s.chat_id, 'You are registered, we are waiting for you ✅', reply_markup=main_menu())

    def deregistration(s, data):
        write = data.split("|")
        id_category = int(write[1])
        user_chat_id = s.chat_id
        category_name = db.get_category_by_telegram_id(user_chat_id)
        try:
            bot.delete_message(s.chat_id, s.msg_id)
            db.delete_patient_by_telegam_id(user_chat_id)
            bot.send_message(user_chat_id, f"OK, you are deregistration from {category_name}", reply_markup=main_menu())
        except Exception as e:
            bot.send_message(user_chat_id, f"ERROR: {e}")
            print(f"ERROR: {e}")


    def reaction_main_menu(s):
        bot.delete_message(s.chat_id, s.msg_id)
        bot.send_message(s.chat_id, 'Main Menu', reply_markup=main_menu_btn())



@bot.callback_query_handler(func=lambda call: bool(call) == True)
def main(call: CallbackQuery):
    try:

        CallMessage(call=call).manager()

    except Exception as e:
        bot.send_message(CallMessage(call=call).chat_id, f"ERROR: {e}")
        print(F"ERROR: {e}")
