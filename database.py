import psycopg2
from psycopg2 import sql
from contextlib import closing
import datetime

DBNAME = 'Sheets'
USER = 'joe'
PASS = 'Abcd1234'
HOST = 'localhost'

def get_data_from_db():
    '''
        Функция извлечения данных из БД
    '''
    conn = psycopg2.connect(dbname = DBNAME, user = USER, password = PASS, host = HOST)
    cursor = conn.cursor()
    cursor.execute('SELECT orderId, price_usd, supply_date FROM sheets')
    result = tuple(cursor)
    cursor.close()
    conn.close()
    return result

def get_value_from_db(orderId):
    '''
        Функция извлечения данных из БД по критерию 'номер_заказа'
    '''
    conn = psycopg2.connect(dbname = DBNAME, user = USER, password = PASS, host = HOST)
    cursor = conn.cursor()
    cursor.execute('SELECT orderId, price_usd, supply_date FROM sheets WHERE orderId = %s', (orderId,))
    result = tuple(cursor)
    cursor.close()
    conn.close()
    return result

def delete_value_from_db(orderId):
    '''
        Функция удаления данных из БД по критерию 'номер_заказа'
    '''
    conn = psycopg2.connect(dbname = DBNAME, user = USER, password = PASS, host = HOST)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM sheets WHERE orderId = %s', (orderId,))
    conn.commit()
    cursor.close()
    conn.close()

def insert_data_to_db(values, usd_rub_price):
    '''
        Функция группового добавления данных в БД
    '''
    with closing(psycopg2.connect(dbname = DBNAME, user = USER, password = PASS, host = HOST)) as conn:
        with conn.cursor() as cursor:
            conn.autocommit = True
            for value in values:
                value[-1] = datetime.datetime.strptime(value[-1], "%d.%m.%Y").strftime("%Y-%m-%d")
                value.append(int(value[1]) * usd_rub_price)
                insert = sql.SQL('INSERT INTO sheets (orderId, price_usd, supply_date, price_rub) VALUES ({})').format(
                    sql.SQL(',').join(map(sql.Literal, value)))
                cursor.execute(insert)

def update_value_to_db(value, usd_rub_price):
    '''
        Функция обновления строки в БД
    '''
    with closing(psycopg2.connect(dbname = DBNAME, user = USER, password = PASS, host = HOST)) as conn:
        with conn.cursor() as cursor:
            conn.autocommit = True
            value[-1] = datetime.datetime.strptime(value[-1], "%d.%m.%Y").strftime("%Y-%m-%d")
            value.append(int(value[1]) * usd_rub_price)
            cursor.execute('UPDATE sheets SET price_usd = %s, supply_date = %s, price_rub = %s WHERE orderId = %s',
            (value[1], value[2], value[-1], value[0]))


def insert_value_to_db(value, usd_rub_price):
    '''
        Функция вставки строки в БД
    '''
    with closing(psycopg2.connect(dbname = DBNAME, user = USER, password = PASS, host = HOST)) as conn:
        with conn.cursor() as cursor:
            conn.autocommit = True
            value[-1] = datetime.datetime.strptime(value[-1], "%d.%m.%Y").strftime("%Y-%m-%d")
            value.append(int(value[1]) * usd_rub_price)
            insert = sql.SQL('INSERT INTO sheets (orderId, price_usd, supply_date, price_rub) VALUES ({})').format(
                sql.SQL(',').join(map(sql.Literal, value)))
            cursor.execute(insert)

                

