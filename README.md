## Описание

Простой телеграм-бот, который записывает все сообщения в БД. 
На основе python-telegram-bot и Django.

Смотреть видео: [https://youtu.be/s9RHzPLtYWk]

## Настройка

Установить зависимости:

    cd /Users/vladimir/Developer/td
    mkvirtualenv --python=python3 td
    workon td
    pip install -r pip-requirements.txt

Запуск админки:

    workon td
    cd /Users/vladimir/Developer/td/tga
    python manage.py runserver
    
    
Запуск бота:

    workon td
    cd /Users/vladimir/Developer/td/tga
    python manage.py bot
