# Домашнее задание к занятию "`Работа с данными (DDL/DML)`" - `Блинов А.С.`

---

### Задание 1
1.1. Поднимите чистый инстанс MySQL версии 8.0+. Можно использовать локальный сервер или контейнер Docker.

1.2. Создайте учётную запись sys_temp. 

1.3. Выполните запрос на получение списка пользователей в базе данных. (скриншот)

1.4. Дайте все права для пользователя sys_temp. 

1.5. Выполните запрос на получение списка прав для пользователя sys_temp. (скриншот)

1.6. Переподключитесь к базе данных от имени sys_temp.

Для смены типа аутентификации с sha2 используйте запрос: 
```sql
ALTER USER 'sys_test'@'localhost' IDENTIFIED WITH mysql_native_password BY 'password';
```
1.6. По ссылке https://downloads.mysql.com/docs/sakila-db.zip скачайте дамп базы данных.

1.7. Восстановите дамп в базу данных.

1.8. При работе в IDE сформируйте ER-диаграмму получившейся базы данных. При работе в командной строке используйте команду для получения всех таблиц базы данных. (скриншот)

*Результатом работы должны быть скриншоты обозначенных заданий, а также простыня со всеми запросами.*

### Решение 1
![Скриншот-1](https://github.com/AleksanderB5/sys-pattern-homework-8-2/blob/DDL/DML/фото/1-1%20ddl.png)
![Скриншот-2](https://github.com/AleksanderB5/sys-pattern-homework-8-2/blob/DDL/DML/фото/1-2%20ddl.png)
![Скриншот-3](https://github.com/AleksanderB5/sys-pattern-homework-8-2/blob/DDL/DML/фото/1-3%20ddl.png)
![Скриншот-4](https://github.com/AleksanderB5/sys-pattern-homework-8-2/blob/DDL/DML/фото/1-4%20ddl.png)

```
sudo apt-get install mysql-server
systemctl status mysql
mysql -u root -p
CREATE USER 'sys_temp'@'localhost' IDENTIFIED BY '****';
SELECT User,Host FROM mysql.user;
GRANT ALL PRIVILEGES ON *.* TO sys_temp@localhost;
SHOW GRANTS FOR 'sys_temp'@'localhost';
\quit
unzip sakila-db.zip
mysql -u sys_temp -p
CREATE DATABASE `sakila`;
SHOW DATABASES;
exit
export ASNAME=sakila
mysql -u sys_temp -p ${ASNAME} < /home/aleks/Загрузки/sakila-db/sakila-schema.sql
mysql -u sys_temp -p ${ASNAME} < /home/aleks/Загрузки/sakila-db/sakila-data.sql
mysql -u sys_temp -p
SHOW DATABASES;
USE sakila;
SHOW TABLES;
exit

```
---

### Задание 2
Составьте таблицу, используя любой текстовый редактор или Excel, в которой должно быть два столбца: в первом должны быть названия таблиц восстановленной базы, во втором названия первичных ключей этих таблиц. Пример: (скриншот/текст)
```
Название таблицы | Название первичного ключа
customer         | customer_id
```

### Решение 2
```
Название таблицы             | Название первичного ключа
actor                        | actor_id
actor_info                   | 
address                      | address_id
category                     | category_id
city                         | city_id
country                      | country_id
customer                     | customer_id
customer_list                | 
film                         | film_id
film_actor                   | actor_id, film_id
film_category                | film_id, category_id
film_list                    | 
film_text                    | film_id
inventory                    | inventory_id
language                     | language_id
nicer_but_slower_film_list   | 
payment                      | payment_id
rental                       | rental_id
sales_by_film_category       | 
sales_by_store               | 
staff                        | staff_id
staff_list                   | 
store                        | store_id
```
