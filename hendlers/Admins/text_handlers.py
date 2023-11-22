import json

from telebot.types import Message, ReplyKeyboardRemove

from loader import db, bot
from keyboards.default import *
from keyboards.inlines import *
from states import *
from config import ADMINS


class AdminText():
    def __init__(self, msg: Message):
        self.chat_id = msg.chat.id
        self.text = msg.text
        self.name = msg.chat.first_name
        self.from_user = msg.from_user.id
        self.msg_id = msg.message_id


    def manager(self):
        text = self.text

        if text == "/start":
            return self.reaction_admins_command()

        if text == "Total patients":
            return self.reaction_count_users()

        if text == "Message patients":
            return self.reaction_message_to_users()

        if text == "Delete patients from queues":
            return self.delete_patients_from_queues()

    def reaction_admins_command(self):
        admin_btn = generate_btn([
            "Total patients",
            "Message patients",
            "Delete patients from queues"])

        bot.send_message(self.chat_id, f"Hello Admin {self.name}", reply_markup=admin_btn)


    def reaction_count_users(self):
        count_users = db.count_users()
        bot.send_message(self.chat_id, f"Total patients: {count_users}")


    def reaction_message_to_users(self):
        bot.send_message(self.chat_id, "What do send ?", reply_markup=ReplyKeyboardRemove())
        bot.set_state(self.from_user, AdminMessageState.message, self.chat_id)

    @bot.message_handler(content_types=['text', 'photo', 'video', 'voice'], state=AdminMessageState.message, chat_id=ADMINS)
    def reaction_admin_message(message: Message):
        admin_btn = generate_btn([
            "Total patients",
            "Message patients",
            "Delete patients from queues"])
        chat_id = message.chat.id
        users = db.get_all_users()
        count_users = db.count_users()
        iterator = 0
        for i in users:
            try:
                bot.copy_message(i, chat_id, message.id)
                iterator += 1
            except:
                bot.send_message(chat_id, f"{i} Failed to send to user ID")

        bot.send_message(chat_id, f"Send message  {iterator}/{count_users}", reply_markup=admin_btn)
        bot.delete_state(message.from_user.id, chat_id)

    def delete_patients_from_queues(self):
        bot.send_message(self.chat_id, "Choose this", reply_markup=get_all_categories_admin())

@bot.message_handler(content_types=['text'], chat_id=ADMINS)
def main(msg: Message):
    try:
        AdminText(msg).manager()
    except Exception as e:
        bot.send_message(AdminText(msg).chat_id, f"ERROR: {e}")
        print(F"ERROR: {e}")