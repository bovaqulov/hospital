from telebot.handler_backends import State, StatesGroup

class RegisterState(StatesGroup):
    name = State()
    lastname = State()
    contact = State()
    birthdate = State()
    address = State()
    submit = State()


class CardState(StatesGroup):
    card = State()


class AdminMessageState(StatesGroup):
    message = State()


class CategoryState(StatesGroup):
    category = State()
    about = State()

class ProductState(StatesGroup):
    product_name = State()
    image = State()
    price = State()
    link = State()
    category_id = State()