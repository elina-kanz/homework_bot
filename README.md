# homework_bot
### Описание
Telegram-бот, оповещающий об изменении статуса домашнего задания с помощью API сервиса Практикум.Домашка.
Раз в 10 минут присылает запрос, по изменению статуса анализирует ответ API и отправляет уведомление в Telegram.
Так же логирует свою работу, а при важных проблемах сообщает о них в Telegram. Бот создавался для упражнения
в технологиях API, использовании exceptions, логировании и в общем для опыта создания бота.

### Зависимости
```
flake8==3.9.2
flake8-docstrings==1.6.0
pytest==6.2.5
python-dotenv==0.19.0
python-telegram-bot==13.7
requests==2.26.0
```
### Как запустить проект
Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:elina-kanz/homework_bot.git
cd homework_bot
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv env
source env/bin/activate
```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
pip install -r requirements.txt
```

Запустить проект

```
python3 homework.py
```

Для запуска проекта понадобится файл c переменными окружения ```.env```.
Образец наполнения:
```
PRACTICUM_TOKEN={выдается ученикам курса}
TELEGRAM_TOKEN={Токен созданного бота}
TELEGRAM_CHAT_ID={ID вашего телеграм-чата}
```


