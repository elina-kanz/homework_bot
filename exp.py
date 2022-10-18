# import os
# import logging


# import requests
# import telegram
# from pprint import pprint

# from homework import (PRACTICUM_TOKEN, TELEGRAM_TOKEN,
#                       ENDPOINT, HEADERS, HOMEWORK_STATUSES)


# TELEGRAM_CHAT_ID = None


# def check_response(response):
#     try:
#         return response.get('homeworks')
#     except Exception:
#         print("check_response сломался")


# def parse_status(homework):
#     homework_name = homework['homework_name']
#     homework_status = homework['status']
#     verdict = HOMEWORK_STATUSES[homework_status]
#     return f'Изменился статус проверки работы "{homework_name}". {verdict}'


# def check_tokens():
#     """Проверяет доступность переменных окружения"""
#     logger = logging.getLogger(__name__)
#     # env_variables = [TELEGRAM_TOKEN, PRACTICUM_TOKEN, TELEGRAM_CHAT_ID]
#     # for env_var in env_variables:
#     #     if env_var is None:
#     #         logger.critical('Отсутствует обязательная переменная окружения:'
#     #                         f'{env_var.__name__}. Программа принудительно'
#     #                         f'остановлена')
#     #         return False
#     if type(PRACTICUM_TOKEN) != str:
#         logger.critical('Отсутствует обязательная переменная окружения:'
#                         'PRACTICUM_TOKEN. Программа принудительно остановлена')
#         return False
#     if type(TELEGRAM_CHAT_ID) != int:
#         logger.critical(
#             'Отсутствует обязательная переменная окружения: TELEGRAM_CHAT_ID.'
#             'Программа принудительно остановлена')
#     if type(TELEGRAM_TOKEN) != str:
#         logger.critical('Отсутствует обязательная переменная окружения:'
#                         'TELEGRAM_TOKEN. Программа принудительно остановлена')
#         return False
#     return True


# timestamp = 1663848772
# params = {'from_date': timestamp}
# response = requests.get(ENDPOINT, headers=HEADERS, params=params).json()
# TEST = os.getenv('TEST')
# homeworks = check_response(response)
# status = parse_status(homeworks[0])
# bot = telegram.Bot(token=TELEGRAM_TOKEN)
# pprint(check_tokens())
