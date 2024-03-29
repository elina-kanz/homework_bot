"""Бот-ассистент, сообщающий о статусе отправленных домашних работ ЯП."""

import logging
import os
import sys
import time
import traceback
from http import HTTPStatus
from logging import StreamHandler

import requests
import telegram
from dotenv import load_dotenv

from exceptions import NotSendingError, SendingError

load_dotenv()


PRACTICUM_TOKEN = os.getenv('PRACTICUM_TOKEN')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

RETRY_TIME = 600
ENDPOINT = 'https://practicum.yandex.ru/api/user_api/homework_statuses/'
HEADERS = {'Authorization': f'OAuth {PRACTICUM_TOKEN}'}


HOMEWORK_STATUSES = {
    'approved': 'Работа проверена: ревьюеру всё понравилось. Ура!',
    'reviewing': 'Работа взята на проверку ревьюером.',
    'rejected': 'Работа проверена: у ревьюера есть замечания.'
}


def send_message(bot, message):
    """Отправляет сообщение в Telegram чат."""
    logger = logging.getLogger(__name__)
    try:
        logger.info('Начата отправка сообщения')
        bot.send_message(TELEGRAM_CHAT_ID, message)
        logger.info(f'Отправлено сообщение: `{message}`')
    except Exception:
        log_message = f'Сбой при отправке сообщения: "{message}"'
        raise NotSendingError(log_message)


def get_api_answer(current_timestamp):
    """Делает запрос к эндпоинту API-сервиса."""
    params = {'from_date': current_timestamp}
    try:
        logging.info(f'Попытка запроса к энпоинту {ENDPOINT}')
        response = requests.get(ENDPOINT, headers=HEADERS, params=params)
    except Exception:
        log_message = (f'Сбой в работе программы: Эндпоинт {ENDPOINT}'
                       'недоступен.')
        raise SendingError(log_message)
    if response.status_code != HTTPStatus.OK:
        log_message = (f'Сбой в работе программы: Эндпоинт {ENDPOINT} '
                       f'недоступен. Код ответа API: {response.status_code}')
        raise SendingError(log_message)
    logging.info('Отправлен запрос')
    return response.json()


def check_response(response):
    """Проверяет корректность API ответа."""
    if not isinstance(response, dict):
        log_message = ('Сбой в работе программы: ответ API имеет'
                       ' некорректный тип')
        raise TypeError(log_message)
    if ('homeworks' or 'current_date') not in response:
        log_message = ('Сбой в работе программы:'
                       'в ответе API нет необходимого ключа')
        raise TypeError(log_message)
    homeworks = response.get('homeworks')
    if not isinstance(homeworks, list):
        log_message = ('Сбой в работе программы: в ответе API под ключом '
                       '`homeworks` хранится некорректный тип')
        raise TypeError(log_message)
    return response.get('homeworks')


def parse_status(homework):
    """Извлекает из конкретной домашней работы статус этой работы."""
    homework_name = homework.get('homework_name')
    homework_status = homework.get('status')
    if ('homework_name' or 'status') not in homework:
        log_message = 'В домашней работе нет необходимого ключа'
        raise KeyError(log_message)
    try:
        verdict = HOMEWORK_STATUSES[homework_status]
        # в тесте требуются двойные кавычки ¯\_(ツ)_/¯
        return f'Изменился статус проверки работы "{homework_name}". {verdict}'
    except KeyError:
        log_message = ('Недокументированный статус домашней работы:'
                       f' `{homework_status}` в домашней работе '
                       f'{homework_name}')
        raise SendingError(log_message)


def check_tokens():
    """Проверяет доступность переменных окружения."""
    tokens = (PRACTICUM_TOKEN, TELEGRAM_CHAT_ID, TELEGRAM_TOKEN)
    return all(tokens)


def main():
    """
    Основная логика работы бота.

    Запускаем бота, отправляем запрос, анализируем, бот отправляет анализ
    """
    if not check_tokens():
        message = ('Отсутствует обязательная переменная окружения.'
                   'Программа принудительно остановлена')
        sys.exit(message)

    bot = telegram.Bot(token=TELEGRAM_TOKEN)
    current_timestamp = int(time.time())
    current_timestamp = 1663848772
    old_message = ''
    while True:
        try:
            response = get_api_answer(current_timestamp)
            homeworks = check_response(response)
            current_timestamp = response.get('current_date')
            if homeworks:
                message = parse_status(homeworks[0])
                if old_message != message:
                    send_message(bot, message)
                    old_message = message
            else:
                logging.debug('Изменений в статусах нет')
        except SendingError:
            log_message = traceback.format_exc()
            logging.error(log_message)
            send_message(bot, log_message)
        except NotSendingError:
            log_message = traceback.format_exc()
            logging.critical(log_message)
        finally:
            time.sleep(RETRY_TIME)


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s, %(levelname)s, %(message)s, %(name)s',
        handlers=[StreamHandler(stream=sys.stdout)]
    )
    main()
