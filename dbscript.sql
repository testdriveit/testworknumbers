-- Создание БД
CREATE DATABASE Sheets;
-- Создание таблицы для внесения данных
CREATE TABLE sheets (
    recordId serial PRIMARY KEY,
    orderId int,
    price_usd int,
    supply_date Date,
    price_rub float8
);
-- Создание пользователя, для доступа к БД
create role joe 
login 
password 'Abcd1234';
-- Назначение прав и привилегий пользователю
GRANT ALL 
ON Sheets 
TO joe;

GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO joe;