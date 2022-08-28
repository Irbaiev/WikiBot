import logging, wikipedia, re, os


from aiogram import Bot, Dispatcher, executor, types

API_TOKEN = os.environ.get('BOT_TOKEN')

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

wikipedia.set_lang('ru')

def getwiki(s):
    try:
        ny = wikipedia.page(s)
        # Получаем первую тысячу символов
        wikitext=ny.content[:1500]
        # Разделяем по точкам
        wikimas=wikitext.split('.')
        # Отбрасываем всЕ после последней точки
        wikimas = wikimas[:-1]
        # Создаем пустую переменную для текста
        wikitext2 = ''
        # Проходимся по строкам, где нет знаков «равно» (то есть все, кроме заголовков)
        for x in wikimas:
            if not('==' in x):
                    # Если в строке осталось больше трех символов, добавляем ее к нашей переменной и возвращаем утерянные при разделении строк точки на место
                if(len((x.strip()))>3):
                   wikitext2=wikitext2+x+'.'
            else:
                break
        # Теперь при помощи регулярных выражений убираем разметку
        wikitext2=re.sub('\([^()]*\)', '', wikitext2)
        wikitext2=re.sub('\([^()]*\)', '', wikitext2)
        wikitext2=re.sub('\{[^\{\}]*\}', '', wikitext2)
        # Возвращаем текстовую строку
        return wikitext2
    # Обрабатываем исключение, которое мог вернуть модуль wikipedia при запросе
    except Exception as e:
        return 'В энциклопедии нет информации об этом'

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.reply(f"Привет {message.from_user.username}! Отправьте мне любое слово, и я найду его значение на Wikipedia")

@dp.message_handler(content_types=['text'])
async def handler(message: types.Message):
    await message.reply(getwiki(message.text))




if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)  
