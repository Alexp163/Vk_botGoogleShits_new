import vk_api
from vk_api import keyboard
from vk_api.bot_longpoll import VkBotEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.longpoll import VkLongPoll, VkEventType
from toks import main_token
from connect_table import recording_data
from connect_table import recording_transport_company
from connect_table import recording_delivery_address
from connect_table import data_collection_function
from connect_table import data_delivery_function

vk_session = vk_api.VkApi(token=main_token)
session_api = vk_session.get_api()
longpoll = VkLongPoll(vk_session)
user_name = ''
transport_company = ''



def sender(id: int, text: str, keyboard=None): # функция общения с пользователем , подключение клавиатуры
    """
    1. Функция взаимодействия пользователя с ботом
    2. Функция, которая запускает работу бота, после ввода сообщения "привет" и подгружает
    меню с 5-ю кнопками, а так же выводит приветствие пользователя.
    3. Args: message: discord.Message - аргумент для взаимодействия между пользователем и ботом.
    message.chat.id выводит сообщение пользователю в бот
    4. функция ничего не возвращает
    """
    if keyboard:
        session_api.messages.send(user_id=id, message=text, random_id=0, keyboard=keyboard.get_keyboard())
    else:
        session_api.messages.send(user_id=id, message=text, random_id=0)
    print('1', type(id))
    print('2', type(text))
    print('3', type(keyboard))
    return text

def personal_account(id): # меню входа в личный кабинет
    keyboard = VkKeyboard(one_time=False)
    keyboard.add_button('Ввести личные данные', color=VkKeyboardColor.PRIMARY)
    keyboard.add_button('Я уже вводил данные', color=VkKeyboardColor.PRIMARY)
    sender(id, text='Перенаправляем в личный кабинет', keyboard=keyboard)


def start_keyboard(id): # меню запуска главной клавиатуры бота
    keyboard = VkKeyboard(one_time=False)
    keyboard.add_button('Главное меню', color=VkKeyboardColor.PRIMARY)
    keyboard.add_button('Калькулятор', color=VkKeyboardColor.PRIMARY)
    keyboard.add_button('Личный Кабинет', color=VkKeyboardColor.PRIMARY)
    keyboard.add_button('Частые вопросы', color=VkKeyboardColor.PRIMARY)
    keyboard.add_button('Связь с нами', color=VkKeyboardColor.PRIMARY)
    sender(id, text='Привет! Я запустил для тебя Стартовое меню', keyboard=keyboard)


def change_delivery(id): # меню выбора траспортной компании
    keyboard = VkKeyboard(one_time=False)
    keyboard.add_button('Почта России', color=VkKeyboardColor.PRIMARY)
    keyboard.add_button('Сдек', color=VkKeyboardColor.PRIMARY)
    keyboard.add_button('Боксбери', color=VkKeyboardColor.PRIMARY)
    sender(id, text='Выберите траспортную компанию', keyboard=keyboard)


def further_action(id): # меню работы в личном кабинете
    keyboard = VkKeyboard(one_time=False)
    keyboard.add_button('Мои заказы', color=VkKeyboardColor.PRIMARY)
    keyboard.add_button('Отследить заказ', color=VkKeyboardColor.PRIMARY)
    keyboard.add_button('Мои личные данные', color=VkKeyboardColor.PRIMARY)
    keyboard.add_button('Вернуться в стартовое меню', color=VkKeyboardColor.PRIMARY)
    sender(id, text='Выберите дальнейшее действие', keyboard=keyboard)


def main():
    user_name = ''
    transport_company = ''
    delivery_address = ''
    for event in longpoll.listen():
        print('Бот запущен')
        if event.type == VkEventType.MESSAGE_NEW:
            if event.to_me:
                msg = event.text.lower()
                id = event.user_id
                if msg == 'привет':
                    print('Я здесь')
                    start_keyboard(id)
                if msg == 'главное меню':
                    sender(id, text='Теперь ты в главном меню')
                elif msg == 'калькулятор':
                    sender(id, text='Теперь можешь воспользоваться калькулятором')
                elif msg == 'личный кабинет':
                    print(f'переменная мсг-2 {msg}')
                    personal_account(id)
                if msg == 'ввести личные данные':
                    print('Введите ФИО')
                    sender(id, text='Введите ФИО, телефон, индекс и адрес')
                    for event in longpoll.listen():
                        if event.type == VkEventType.MESSAGE_NEW:
                            if event.to_me:
                                msg = event.text.lower()
                                id = event.user_id
                                user_name += msg
                                recording_data(user_name, id)
                                print(f'это ФИО{user_name}')
                                change_delivery(id)
                                print(f'я юзянем из файла майн {user_name}')
                                if msg == 'почта россии' or msg == 'сдек' or msg == 'боксбери':
                                    transport_company += msg
                                    print(f'это транспортная компания {transport_company}')
                                    recording_transport_company(id, transport_company)
                                    sender(id, text='Введите индекс и адрес доставки')
                                    for event in longpoll.listen():
                                        if event.type == VkEventType.MESSAGE_NEW:
                                            if event.to_me:
                                                msg = event.text.lower()
                                                id = event.user_id
                                                delivery_address += msg
                                                recording_delivery_address(delivery_address, id)
                                                sender(id, text='Вы вошли в личный кабинет')
                                                data_collection = data_collection_function(id, user_name)
                                                data_delivery = data_delivery_function(id)
                                                further_action(id)
                                                for event in longpoll.listen():
                                                    if event.type == VkEventType.MESSAGE_NEW:
                                                        if event.to_me:
                                                            msg = event.text.lower()
                                                            id = event.user_id
                                                            if msg == 'мои заказы':
                                                                sender(id, text=f'Ваша заказы: \n{data_collection}')
                                                            elif msg == 'мои личные данные':
                                                                sender(id, text=f'ваши личные данные{data_delivery}')
                                                            elif msg == 'вернуться в стартовое меню':
                                                                sender(id, text=f'переводим вас в стартовое меню {main()}')
                                                                start_keyboard(id)

                if msg == 'я уже вводил данные':
                    change_delivery(id)
                if msg == 'почта россии' or msg == 'сдек' or msg == 'боксбери':
                    transport_company += msg
                    # recording_data(user_name, id)
                    recording_transport_company(id, transport_company)
                    print(f'это транспортная компания {transport_company}')
                    sender(id, text='Введите индекс и адрес доставки')
                    for event in longpoll.listen():
                        if event.type == VkEventType.MESSAGE_NEW:
                            if event.to_me:
                                msg = event.text.lower()
                                id = event.user_id
                                delivery_address += msg
                                recording_delivery_address(delivery_address, id)
                                sender(id, text='Вы вошли в личный кабинет')
                                further_action(id)
                                data_collection = data_collection_function(id, user_name)
                                data_delivery = data_delivery_function(id)
                                for event in longpoll.listen():
                                    if event.type == VkEventType.MESSAGE_NEW:
                                        if event.to_me:
                                            msg = event.text.lower()
                                            id = event.user_id
                                            if msg == 'мои заказы':
                                                sender(id, text=f'Ваша заказы: \n{data_collection}')
                                            elif msg == 'мои личные данные':
                                                sender(id, text=f'ваши личные данные{data_delivery}')
                elif msg == 'частые вопросы':
                    sender(id, text='Наиболее частый вопрос: "Что ты здесь делаешь, бедолага?"')
                if msg == 'связь с нами':
                    sender(id, text='Кстати, с нами лучше не связываться!')




if __name__ == "__main__":
    # enetering_main_menu()
    main()
