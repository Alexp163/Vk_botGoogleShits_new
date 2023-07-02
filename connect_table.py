"""
Файл connect_table.py содержит в себе функции, которые будут осуществлять
ввод и вывод данных из гугл-таблицы при взаимодействии с пользователем через
телеграмм-бот посредством импорта в файл main.py содержащих в себе функций
"""
import os.path
from google.oauth2 import service_account
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SAMPLE_SPREADSHEET_ID = '1wgZRhyKNsZEXfm2fumy1xDeGi2fvhjklvhjldzu_8'
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SERVICE_ACCOUNT_FILE = os.path.join(BASE_DIR, 'creds_130523.json')
SAMPLE_RANGE_NAME = 'Sheet1'


def definition_credentials(): # даёт права доступа для работы с гугл-таблицей
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    service = build('sheets', 'v4', credentials=credentials)
    sheets = service.spreadsheets()
    result = sheets.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range='Sheet1!C1:C30').execute()
    values = result.get('values', []) # список пользователей в столбце "С"
    return values, service, sheets, result, credentials


def recording_transport_company(id, transport_company): # запись названия транспортной компании в таблицу
    values, service, sheets, result, credentials = definition_credentials()
    count = 0
    for i in values:
        count += 1
        if i[0] == str(id):
            range_ = f'Sheet1!J{count}'
            array = {'values': [[transport_company]]}
            service.spreadsheets().values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=range_,
                                                   valueInputOption='USER_ENTERED',
                                                   body=array).execute()


def recording_data(user_name, id):  # запись данных о покупателе(фио, адрес...)
    values, service, sheets, result, credentials = definition_credentials()
    count = 0
    for i in values:
        count += 1
        if i[0] == str(id):
            range_ = f'Sheet1!I{count}'
            array = {'values': [[user_name]]}
            service.spreadsheets().values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=range_,
                                                   valueInputOption='USER_ENTERED',
                                                   body=array).execute()


def recording_delivery_address(delivery_address, id):  # запись адреса доставки в таблицу
    values, service, sheets, result, credentials = definition_credentials()
    count = 0
    for i in values:
        count += 1
        if i[0] == str(id):
            range_ = f'Sheet1!K{count}'
            array = {'values': [[delivery_address]]}
            service.spreadsheets().values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=range_,
                                                   valueInputOption='USER_ENTERED',
                                                   body=array).execute()


def data_collection_function(id, user_name):  # выводит (user_name, товар, стоимость, статус заказа)в бот
    values, service, sheets, result, credentials = definition_credentials()
    report1 = ""
    count = 0
    count_2 = 0
    for i in values:
        count += 1
        if i[0] == str(id):
            count_2 += 1
            result = sheets.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=f'Sheet1!D{count}:M{count}').execute()
            values_ = result.get('values')
            report1 += f'Покупатель - {user_name} ,\nзаказ номер - {values_[0][8]} \nваш товар - {values_[0][0]}\nстоимостью - {values_[0][1]}\nстоимость доставки - {values_[0][3]}\nстатус - {values_[0][9]}\n\n'
    return report1


def data_delivery_function(id):  # выводит данные доставки в бот
    values, service, sheets, result, credentials = definition_credentials()
    report2 = ""
    count = 0
    for i in values:
        count += 1
        if i[0] == str(id):
            result = sheets.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=f'Sheet1!I{count}:K{count}').execute()
            values_ = result.get('values')
    report2 += f'{values_[0][0]}\nтранспортная компания - {values_[0][1]}\nАдрес отделения - {values_[0][2]}\n\nЕсли вы хотите поменять свои данные, напишите администратору\n\n\n'
    return report2


# if __name__ == "__main__":
#     recording_data()
    # main_2()
#     recording_data(user_name, dict_customer_data)
