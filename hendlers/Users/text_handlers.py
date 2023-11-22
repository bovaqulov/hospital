import json

from telebot.types import Message, ReplyKeyboardRemove
from telebot.apihelper import download_file


from loader import bot
from keyboards.default import *
from states import *
from about_us import *
from about_us_2 import *
from keyboards.inlines import *

class TextMessage():
    def __init__(s, msg: Message):
        s.chat_id = msg.chat.id
        s.text = msg.text
        s.name = msg.chat.first_name
        s.user_id = msg.from_user.id
        s.msg = msg
        s.msg_id = msg.message_id

    def manager(s):
        text = s.text
        print(text)
        if text == "/start": return s.reaction_start()

        if text == "Regestiration ✍️" and not db.find_user_id(s.chat_id) : return s.reaction_register()

        if bool(text) != db.find_user_id(s.chat_id):
            return bot.send_message(s.chat_id, "Please, Regestration at us", reply_markup=register_btn())

        else:
            if text == "Directions 🗒": return s.reaction_directions()

            lst: list = [pediatricians, cardiologists, neurologists, dentists, oncologists]
            lst_2: list = ["Pediatricians", "Cardiologists", "Neurologists", "Gentists", "Oncologists"]

            if text in lst_2:
                return s.all_directions(lst[lst_2.index(text)])

            if text == "Main menu": return s.main_menu()

            if text == "Contact the hospital ☎️": return s.categories_id()

            if text == "View queues 👀": return s.queues()

            if text == "About Hospital 📓": return s.about_us()

            if text == "Locations 📍" : return s.location()

            else:
                return s.auto_answer()



    def main_menu(s):
        bot.send_message(s.chat_id, "Choose, Please !!!", reply_markup=main_menu_btn())

    def reaction_start(s):
        db.insert_telegram_id(s.chat_id)
        bot.send_message(s.chat_id, (f"hello {s.name}"), reply_markup=main_menu_btn())

    def reaction_register(s):
        print("step 1")
        bot.set_state(s.user_id, RegisterState.name, s.chat_id)
        bot.send_message(s.chat_id, 'Your firstname: ', reply_markup=ReplyKeyboardRemove())

    @bot.message_handler(content_types=['text'], state=RegisterState.name)
    def reaction_name(message: Message):
        chat_id = message.chat.id
        user_id = message.from_user.id
        with bot.retrieve_data(user_id, chat_id) as data:
            data['name'] = message.text.capitalize()
        bot.set_state(user_id, RegisterState.lastname, chat_id)
        bot.send_message(chat_id, 'Your surname: ', reply_markup=ReplyKeyboardRemove())

    @bot.message_handler(content_types=['text'], state=RegisterState.lastname)
    def reaction_lastname(message: Message):
        chat_id = message.chat.id
        user_id = message.from_user.id
        with bot.retrieve_data(user_id, chat_id) as data:
            data['lastname'] = message.text.capitalize()
        bot.set_state(user_id, RegisterState.contact, chat_id)
        bot.send_message(chat_id, 'Your phone nomer:  <b>+998XXXXXXXXX</b> yoki ulashing!',
                         reply_markup=send_contact_btn(), parse_mode='html')

    @bot.message_handler(content_types=['contact', 'text'], state=RegisterState.contact)
    def reaction_contact(message: Message):
        chat_id = message.chat.id
        user_id = message.from_user.id
        with bot.retrieve_data(user_id, chat_id) as data:
            if message.content_type == 'contact':
                data['contact'] = message.contact.phone_number
                bot.set_state(user_id, RegisterState.birthdate, chat_id)
                bot.send_message(chat_id, "Your Birthday: dd.mm.yyyy",
                                 reply_markup=ReplyKeyboardRemove())
            else:
                import re
                if re.match(r'^\+998(9(0|1|3|4|5|7|8|9)|33|77|88|55)\d{7}$', message.text):
                    data['contact'] = message.text
                    bot.set_state(user_id, RegisterState.birthdate, chat_id)
                    bot.send_message(chat_id, "Your Birthday: dd.mm.yyyy",
                                     reply_markup=ReplyKeyboardRemove())
                else:
                    bot.set_state(user_id, RegisterState.contact, chat_id)
                    bot.send_message(chat_id, "Phone nomer is wrong!, Please, Input again",
                                     reply_markup=send_contact_btn())


    @bot.message_handler(content_types=['text'], state=RegisterState.birthdate)
    def reaction_birthdate(message: Message):
        chat_id = message.chat.id
        user_id = message.from_user.id
        import re
        if re.match(r"^(?:0[1-9]|[12]\d|3[01])([\/.-])(?:0[1-9]|1[012])\1(?:19|20)\d\d$", message.text):
            with bot.retrieve_data(user_id, chat_id) as data:
                data['birthdate'] = message.text
                bot.set_state(user_id, RegisterState.address, chat_id)
                bot.send_message(chat_id, f"""Plaese input your address""", reply_markup=ReplyKeyboardRemove())
        else:
            bot.set_state(user_id, RegisterState.birthdate, chat_id)
            bot.send_message(chat_id, "Your birthday is wrong ! Please again input: dd.mm.yyyy",
                             reply_markup=ReplyKeyboardRemove())


    @bot.message_handler(content_types=['text'], state=RegisterState.address)
    def reaction_lastname(message: Message):
        chat_id = message.chat.id
        user_id = message.from_user.id
        with bot.retrieve_data(user_id, chat_id) as data:
            data['address'] = message.text
            print(data.values())
            name, lastname, contact, birthdate, address  = data.values()
            bot.set_state(user_id, RegisterState.submit, chat_id)
            bot.send_message(chat_id, f"""Check the information:\
                                            First name: {name}\
                                            Surname: {lastname}\
                                            Phone nomer: {contact}\
                                            Birthday: {birthdate}\
                                            Address: {address}\
                                    """,
                             reply_markup=submit_btn())

    @bot.message_handler(content_types=['text'], state=RegisterState.submit)
    def reaction_submit(message: Message):
        chat_id = message.chat.id
        user_id = message.from_user.id
        try:
            if message.text == "True ✅":
                print("step 2")
                with bot.retrieve_data(user_id, chat_id) as data:
                    print(data.values())
                    db.update_user_info(*data.values(), chat_id)
                    print("step 3")
                bot.send_message(chat_id, "Success, Data Saved!", reply_markup=main_menu_btn())
                bot.delete_state(user_id, chat_id)
            else:
                bot.delete_state(user_id, chat_id)
                bot.set_state(user_id, RegisterState.name, chat_id)
                bot.send_message(chat_id, "Your firstname, Please again input: ", reply_markup=ReplyKeyboardRemove())

        except Exception as e:
            bot.delete_state(user_id, chat_id)
            bot.set_state(user_id, RegisterState.name, chat_id)
            print(f"Your message is error. The : {e}")
            bot.send_message(chat_id, "Your firstname, Please again input: ", reply_markup=ReplyKeyboardRemove())

    def reaction_directions(s):
        lst : list = ["pediatricians", "cardiologists", "neurologists", "dentists", "oncologists"]
        bot.send_message(s.chat_id, "Choose, Please", reply_markup=generate_btn(lst))

    def all_directions(s, text: str):
        lst: list = ["Main Menu"]
        bot.send_message(s.chat_id, text, reply_markup=generate_btn(lst))

    def categories_id(s):
        bot.send_message(s.chat_id, "Okey let's go", reply_markup=ReplyKeyboardRemove())
        bot.send_message(s.chat_id, "Choose by your health , Please !", reply_markup=get_all_categories())

    def queues(s):
        if db.get_telegram_id_by_category_id_from_patients(s.chat_id):
            category_id = db.get_queues_patients(s.chat_id)
            category_name = db.get_category_by_telegram_id(s.chat_id)
            lst: list = db.get_all_patients_by_category_id(category_id)[::-1]
            bot.delete_message(s.chat_id, s.msg_id)
            count = 1
            for user in lst:
                if s.chat_id == user[0]:
                    text = f"<b><u>{count} - patient:\n" \
                           f"Direction: {category_name}\n" \
                           f"Name: {user[1]}\n" \
                           f"Surname: {user[2]}\n" \
                           f"phone number: {user[3][0:6]}***{user[3][-4:]}</u></b>"
                    bot.send_message(s.chat_id, text)
                else:
                    text = f"{count} - patient:\n" \
                           f"Direction: {category_name}\n" \
                           f"Name: {user[1]}\n" \
                           f"Surname: {user[2]}\n" \
                           f"phone number: {user[3][0:6]}***{user[3][-4:]}\n"

                    bot.send_message(s.chat_id, text)
                count += 1
        else:
            bot.delete_message(s.chat_id, s.msg_id)
            bot.send_message(s.chat_id, 'You are not registered yet 🤦‍♂️')

    def about_us(s):
        with open(hospetal_photo, 'rb') as photo_file:
            bot.send_photo(s.chat_id, photo=photo_file, caption=about_us_1)

    def location(s):
        bot.send_location(s.chat_id, latitude=41.32220723200667, longitude=69.25209500713164,)
        bot.send_message(s.chat_id, "we are waiting for you at this address")


    def auto_answer(s):
        bot.send_message(s.chat_id, s.text)





@bot.message_handler(content_types=['text'])
def main(msg: Message):
    TextMessage(msg).manager()