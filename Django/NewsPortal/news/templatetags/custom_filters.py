from django import template

register = template.Library()

FORBIDDEN_WORDS = [
]


@register.filter()
def censor(value):
    try:
        list_ = value.split()
    except AttributeError:
        print('Ошибка! Неверный тип данных - должна быть строка!')
    else:
        list_censored = []
        for word in list_:
            word_strip = word.strip('".,:;!?<>()')
            if word_strip.lower() in FORBIDDEN_WORDS:
                censored = word.replace(word_strip[1:], '*' * len(word_strip[1:]))
                list_censored.append(censored)
            else:
                list_censored.append(word)
        value = ' '.join(list_censored)
    return value
