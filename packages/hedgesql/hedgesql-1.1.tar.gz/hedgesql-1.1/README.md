<h1 align="center">HedgeSQL

<h3 align="center">Теперь вам не нужно каждый раз устанавливать соединение, писать sql-запрос и закрывать соединение. Данная библиотека сделает это за вас

Она поддерживает как синхронную, так и асинхронную работу

</h3>

Установка:
```python
pip install hedgesql
```
Теперь импортируем нужное:
```python
from hedgesql import Sqlite, AioSqlite, DataTypes
```
Определяем экземпляр класса:
```python
db = Sqlite(db_name='db.db')
```
Открытие/закрытие соединения:
```python
# Рекомендуется так:
with db:
# пока код внутри блока, соединение открыто, затем оно закрывается

# но можно и вручную:
db.open_conn()
db.close_conn()
```
Создание таблиц:
```python
db.create_table(table_name='users', columns={'id': DataTypes.TEXT(), 'name': DataTypes.TEXT()})
```
Добавление записей:
```python
db.insert_data(table_name='users', data={'id': '123', 'name': 'Дмитрий'})
```
Получение записей:
```python
db.select_data(table_name='users', columns=['name'], where=[{'id': '123'}])
# В columns по умолчанию: '*', то есть все столбцы
# В where словари списка разделены "OR" (или), а данные словарей - "AND" (и)
```
Обновление записей:
```python
db.update_data(table_name='users', set_data={'name': 'Сергей'}, where=[{'id': '123'}])
```
Удаление записей:
```python
db.delete_data(table_name='users', where=[{'id': '123'}])
```
Ну а как сделать работу с бд асинхронной, думаю, знаете