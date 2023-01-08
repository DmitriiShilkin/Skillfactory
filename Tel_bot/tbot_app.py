import telebot
from extensions import APIException, CurrencyConverter
from config import keys, TOKEN


# создание бота
bot = telebot.TeleBot(TOKEN)


# обработчик команд /start и /help
@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Чтобы начать работу, введите команду боту в следующем формате:\n<валюта 1> <валюта 2> <количество>\n\
где:\nвалюта 1 - имя валюты, цену которой хотите узнать;\nвалюта 2 - имя валюты, в которой хотите узнать цену первой валюты;\n\
количество - количество первой валюты.\nВ качестве разделителя используется пробел.\nПросмотр всех доступных валют: /values'
    bot.reply_to(message, text)


# обработчик команды /values
@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key))
    bot.reply_to(message, text)


# обработчик вводимого текста
@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    try:
        values = message.text.lower().split()

        if len(values) > 3:
            raise APIException('Слишком много параметров!')
        elif len(values) < 3:
            raise APIException('Слишком мало параметров!')

        total_base, quote, base, amount, end_q, end_b = CurrencyConverter.get_price(values)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду.\n{e}')
    else:    
        text = f'Цена {amount} {quote}{end_q} в {base}{end_b} - {total_base:.2f}'
        bot.send_message(message.chat.id, text)


# запуск бота в режиме автоматического обновления
bot.polling()

