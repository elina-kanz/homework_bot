import os
import sys
import logging
import time
from logging import StreamHandler

from dotenv import load_dotenv
import requests
import telegram
from http import HTTPStatus
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
        bot.send_message(TELEGRAM_CHAT_ID, message)
        logger.info(f'Отправлено сообщение: "{message}"')
    except Exception:
        log_message = f'Сбой при отправке сообщения: "{message}"'
        logging.error(log_message)
        raise NotSendingError


def get_api_answer(current_timestamp):
    """Делает запрос к эндпоинту API-сервиса."""
    params = {'from_date': current_timestamp}
    try:
        response = requests.get(ENDPOINT, headers=HEADERS, params=params)
    except Exception:
        log_message = (f'Сбой в работе программы: Эндпоинт {ENDPOINT}'
                       'недоступен.')
        logging.error(log_message)
        raise SendingError
    if response.status_code == HTTPStatus.OK:
        logging.info('Отправлен запрос')
        return response.json()
    else:
        log_message = (f'Сбой в работе программы: Эндпоинт {ENDPOINT} '
                       f'недоступен. Код ответа API: {response.status_code}')
        logging.error(log_message)
        raise SendingError


def check_response(response):
    """Проверяет корректность API ответа."""
    if not isinstance(response, dict):
        log_message = ('Сбой в работе программы: ответ API имеет'
                       ' некорректный тип')
        logging.error(log_message)
        raise TypeError
    if "homeworks" not in response:
        log_message = ('Сбой в работе программы:'
                       'в ответе API нет ключа "homeworks"')
        logging.error(log_message)
        raise TypeError
    if not isinstance(response.get('homeworks'), list):
        log_message = ('Сбой в работе программы: в ответе API под ключом '
                       '"homeworks" хранится некорректный тип')
        logging.error(log_message)
        raise TypeError
    return response.get('homeworks')


def parse_status(homework):
    """
    Извлекает из информации о конкретной домашней работе статус этой работы.
    """
    homework_name = homework['homework_name']
    homework_status = homework['status']
    try:
        verdict = HOMEWORK_STATUSES[homework_status]
        return f'Изменился статус проверки работы "{homework_name}". {verdict}'
    except KeyError:
        log_message = ('Недокументированный статус домашней работы:'
                       f' "{homework_status}" в домашней работе '
                       f'{homework_name}')
        logging.error(log_message)
        raise SendingError


def check_tokens():
    """Проверяет доступность переменных окружения."""
    logger = logging.getLogger(__name__)
    if type(PRACTICUM_TOKEN) != str:
        logger.critical('Отсутствует обязательная переменная окружения:'
                        'PRACTICUM_TOKEN. Программа принудительно остановлена')
        return False
    if type(TELEGRAM_CHAT_ID) != int:
        logger.critical(
            'Отсутствует обязательная переменная окружения: TELEGRAM_CHAT_ID.'
            'Программа принудительно остановлена')
    if type(TELEGRAM_TOKEN) != str:
        logger.critical('Отсутствует обязательная переменная окружения:'
                        'TELEGRAM_TOKEN. Программа принудительно остановлена')
        return False
    return True


def main():
    """
    Основная логика работы бота: запускаем бота, отправляем запрос,
    анализируем, бот отправляет анализ
    """

    if check_tokens():
        bot = telegram.Bot(token=TELEGRAM_TOKEN)
        current_timestamp = int(time.time())
        # current_timestamp = 1663848772
        old_message = ''
        while True:
            try:
                response = get_api_answer(current_timestamp)
                homeworks = check_response(response)
                current_timestamp = response.get('current_date')
                if len(homeworks) != 0:
                    message = parse_status(homeworks[0])
                    if old_message != message:
                        send_message(bot, message)
                        old_message = message
                    time.sleep(RETRY_TIME)
                else:
                    logging.debug('Изменений в статусах нет')
                    time.sleep(RETRY_TIME)
            except SendingError:
                log_message = ('Ошибка выполнения программы.'
                               'Посмотрите в логах подробнее')
                send_message(bot, log_message)
                time.sleep(RETRY_TIME)
            except NotSendingError:
                time.sleep(RETRY_TIME)
            else:
                time.sleep(RETRY_TIME)


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s, %(levelname)s, %(message)s, %(name)s',
        handlers=[StreamHandler(stream=sys.stdout)]
    )
    main()
