from num2words import num2words


def number_to_words(number):
    if number < 0:
        return "Отрицательные числа не поддерживаются."

    # Преобразование числа в слова
    return num2words(number, lang='ru', to='cardinal')


# Примеры использования
print(f"{number_to_words(250).capitalize()}")  # "Двести пятьдесят"
print(number_to_words(36))  # "Тридцать шесть"
print(number_to_words(1001))  # "Одна тысяча один"
print(number_to_words(0))  # "Ноль"