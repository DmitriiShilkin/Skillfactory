import requests
import json
from config import keys, API_KEY


# собственный класс исключений
class APIException(Exception):
    pass


# класс обработки пользовательского ввода и запроса валют
class CurrencyConverter:
    @staticmethod
    def get_price(values: list):

        quote, base, amount = values

        if quote == base:
            raise APIException('Нельзя конвертировать валюту саму в себя!')

        if (quote or base) not in keys:
            raise APIException('Не верно указана валюта!')

        try:
            float(amount)
        except ValueError:
            raise APIException('Количество должно быть числом!')

        if float(amount) == 0:
            raise APIException('Количество не может быть равным 0!')
        
        if float(amount) < 0:
            raise APIException('Количество не может быть отрицательным!')


        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={keys[quote]}&tsyms={keys[base]}\
&api_key={API_KEY}').content
        total_base = float(json.loads(r)[keys[base]]) * float(amount)
        
        if 0 < float(amount) <= 1:

            if quote[-1] == 'о':
                end_q = ''
            elif quote[-1] == 'ь':
                quote = quote[:-1]
                end_q = 'я'
            else:
                end_q = 'а'
            
            if base[-1] == 'о':
                end_b = ''
            elif base[-1] == 'ь':
                base = base[:-1]
                end_b = 'ях'
            else:
                end_b = 'ах'

        else:

            if quote[-1] == 'о':
                end_q = ''
            elif quote[-1] == 'ь':
                quote = quote[:-1]
                end_q = 'ей'
            else:
                end_q = 'ов'
            
            if base[-1] == 'о':
                end_b = ''
            elif base[-1] == 'ь':
                base = base[:-1]
                end_b = 'ях'
            else:
                end_b = 'ах'    

        return total_base, quote, base, amount, end_q, end_b

