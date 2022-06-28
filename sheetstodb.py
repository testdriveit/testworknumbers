from apiclient import discovery
from database import delete_value_from_db, get_data_from_db, get_value_from_db, insert_data_to_db, insert_value_to_db, update_value_to_db
import time
from cbrfquote import get_usd_rub_price

SLEEP_TIME = 30 #Скрипт запускается каждые 30 секунд

def get_sheet_data():
    '''
        Функция получения данных из таблицы Google
    '''
    spreadsheet_id = '1dKBEYDjUgSEOfA2ckrwDHFKa8n78HtGDl2N7hMNg_dU' # ID таблицы
    key = 'AIzaSyD8i261_u97Uuwz24HrhiwxLE5jMcAf3bQ' # API-key для обращения к таблице
    range_name = 'B2:YY' # запрашиваемый диапазон ячеек

    service = discovery.build('sheets', 'v4', developerKey=key)

    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=spreadsheet_id,
                                    range=range_name).execute()
    values = result.get('values', [])
    return values



if __name__ == "__main__":
    # Инициализация данных при первом запуске
    previous_time = time.gmtime()
    usd_rub = get_usd_rub_price()
    previous_values = get_data_from_db()

    while True:
        values = get_sheet_data()
        print('Data retrieved: %s' % time.ctime())
        current_time = time.gmtime()
        # Если произошла смена дня, то запрашиваем котировки USD_RUB и обновляем цену товара в таблице
        if current_time.tm_yday != previous_time.tm_yday:
            usd_rub = get_usd_rub_price()
            for value in values:
                update_value_to_db(value, usd_rub)
        
        # Если БД была пустой, заполняем ее полученными значениями
        if len(previous_values) == 0:
            insert_data_to_db(values, usd_rub)
        
        # Если количество записей предыдущего чтения больше, чем на текущей итерации,
        # данные были удалены, обновляем БД
        elif len(previous_values) > len(values):
            for previous_value in previous_values:
                exists = False
                for value in values:
                    if int(previous_value[0]) == int(value[0]):
                        exists = True
                        break
                if not exists:
                    delete_value_from_db(previous_value[0])
        # Актуализация данных их таблицы и БД
        else:
            for value in values:
                db_data = get_value_from_db(value[0])
                if len(db_data) == 0:
                    insert_value_to_db(value, usd_rub)
                else:
                    if int(value[1]) != int(db_data[0][1]):
                        update_value_to_db(value, usd_rub)
        print('Database updated: %s' % time.ctime())

        # Созраняем значения для сравнения на следующей итерации
        previous_values = values[:]
        previous_time = current_time
        time.sleep(SLEEP_TIME)
