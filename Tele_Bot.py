import telebot
from config_tele_bot import keys, TOKEN
from Exceptions_tele_bot import ConvertionException, CryptoConverter

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['all_dollars'])
def all_dollars(message):
    text = ''
    for key in keys.keys():
        if key != 'доллар':
            text += f'1 {key} = {CryptoConverter.convert(key, "доллар", 1)} $\n'
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['start', 'help'])
def start_message(message):
    text = 'Чтобы начать работу введите комманду боту в следующем формате: \n<имя валюты>' \
           '<в какую валюту перевести>' \
           '<количество переводимой валюты>\n' \
           'Увидеть список всех доступных валют: /values\n' \
           'Список всех валют в долларах: /all_dollars'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = "\n".join((text, key,))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text'])
def convert(message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise ConvertionException('Слишком много переменных.')

        quote, base, amount = values
        total_base = CryptoConverter.convert(quote.lower(), base.lower(), amount)
    except ConvertionException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        text = f'Цена {amount} {quote} в {base} = {round(float(total_base) * float(amount), 2)}'
        bot.send_message(message.chat.id, text)


bot.polling()
