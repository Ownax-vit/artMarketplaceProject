
Marketplace
-----------
**Тестовое задание**

Схема БД:
![Страница результатов](assets/bd.png)



**Установка**
1) Клонировать директорию
2) Создать виртуальное окружение:
```
python -m venv venv
```

3) Активировать виртуальное окружение

на windows:
```.\venv\scripts\activate``` 

на линукс:
```source venv/bin/activate```


4) Установить зависимости:
```
pip install -r requirements.txt
```
5) Указать переменные окружения в файле .env (полный список в src/config Settings). 
Обязательно данные БД

6) Применить миграции
```commandline
alembic revision --autogenerate -m "init"
alembic upgrade heads
```

7) Запустить start_server.py
доки по /docs
админ панель: /admin


9) Тесты (на данный момент недоделаны)
```commandline
    pytest
    или 
    python -m pytest 
```
