if __name__ == '__main__':

    import telebot
    from telebot import types
    import random
    import requests
    from bs4 import BeautifulSoup
    from selenium import webdriver
    import matplotlib.pyplot as plt
    from matplotlib.figure import Figure
    from mysql.connector import connect, Error
    from math import *


    driver = webdriver.Chrome()
    bot = telebot.TeleBot('1718596856:AAFkQZz3_IlyW9UkNg1OVm230h74iQyrmXs')


    with connect(
        user='root',
        password='Faggot_2002',
        host='127.0.0.1',
        database='Users'
    ) as connection:


        def analis(x, ans):

            if 'x' in ans:
                if x < 0:
                    ans = ans.replace('x', '({})'.format(float(x)))
                else:
                    ans = ans.replace('x', '({})'.format(float(x)))

            elif 'y' in ans:
                if x < 0:
                    ans = ans.replace('y', '({})'.format(float(x)))
                else:
                    ans = ans.replace('y', '({})'.format(float(x)))

            ans = ans.replace('r(', 'exp(')
            return eval(ans)


        def build_graph(x1, x2, step, ans, ax):

            x = [x1]
            i = 0
            a = x[0]

            while x[i] < x2:
                a += step
                x.append(a)
                i += 1

            y = [analis(x[j], ans[2: len(ans)]) for j in range(0, len(x))]

            if 'y=' in ans:
                return ax.plot(x, y)
            elif 'x=' in ans:
                return ax.plot(y, x)


        def set_new_name(user_id, first_name, username):

            update_table = '''
            INSERT INTO telegramm (id, FirstName, UserName)
            VALUES ({0}, '{1}', '{2}')
            '''.format(user_id, first_name, username)

            try:
                with connection.cursor() as cursor:
                    cursor.execute(update_table)
                    connection.commit()
            except Error as error:
                print(error)


        def update_name(user_id, username):

            update_table = '''
                UPDATE telegramm SET UserName = '{0}' WHERE id = {1}
                '''.format(username, user_id)

            try:
                with connection.cursor() as cursor:
                    cursor.execute(update_table)
                    connection.commit()
            except Error as error:
                print(error)


        def search_name(user_id):

            search = '''
                SELECT UserName FROM users.telegramm WHERE id = {}
            '''.format(user_id)

            with connection.cursor() as cursor:
                cursor.execute(search)
                return cursor.fetchone()[0]


        def get_name(message):
            person_id = message.from_user.id
            update_name(person_id, message.text)
            bot.send_message(person_id, 'Теперь буду называть тебя ' + search_name(person_id))


        def register(message):
            bot.send_message(message.from_user.id, 'Как мне к тебе обращаться?')
            bot.register_next_step_handler(message, get_name)


        def some_help(message):
            bot.send_message(message.from_user.id, '''/start - начать с самого начала.
            \n/reg - поменять свое имя.
            \nМожешь попробовать простые слова и фразы. если я их знаю, то обязательно отвечу.
            \nНапиши картинка, если хочешь, чтобы я отправил тебе картинку.
            \nМожешь так же попросить у меня рифму.
            \nНапиши график и я построю его тебе.''')


        def wait(message):
            person_id = message.from_user.id
            bot.send_message(person_id, 'Картинку чего хочет ' + search_name(person_id) + '?')
            bot.register_next_step_handler(message, get_picture)


        def wait_riphm(message):
            person_id = message.from_user.id
            bot.send_message(person_id, search_name(person_id) +
                             ', напиши слово, к которому хочешь получить рифму')
            bot.register_next_step_handler(message, get_riphm)


        def get_picture(message):

            url = 'https://www.google.co.in/search?q=' + message.text + '&source=lnms&tbm=isch'
            driver.get(url)
            html = str(driver.page_source)
            html = html[int(len(html) * 0.85): len(html)]

            min = 0
            total = 0
            actual_image = []

            while total < 15:
                if 'jpg' in html[min: len(html)]:
                    second = html.find('.jpg', min)
                    for i in range(second, 0, -1):
                        if html[i - 4: i] == 'http':
                            first = i
                            min = second + 20
                            total += 1
                            actual_image.append('http' + html[first: second] + '.jpg')
                            break
                else:
                    break

            r = random.randint(0, len(actual_image))

            try:
                bot.send_message(message.from_user.id, actual_image[r])
            except:
                bot.send_message(message.from_user.id, 'Я не смог найти картинку, сообщи об этом создателю')

            bot.send_message(message.from_user.id,
                             'Если хочешь еще картинку к этому слову- напиши "еще".\nЕсли хочешь закончить- напиши "хватит".\nХочешь картинку по другому слову- просто напиши это слово.')

            action = 'picture'
            bot.register_next_step_handler(message, more, actual_image, action)


        def pleasent(message):
            murkup = types.InlineKeyboardMarkup(row_width=2)
            button1 = types.InlineKeyboardButton('хорошо', callback_data='хорошо')
            button2 = types.InlineKeyboardButton('плохо', callback_data='плохо')
            murkup.add(button1, button2)

            bot.send_message(message.from_user.id, 'Нормально, а ты как?', reply_markup=murkup)


        def page(url):

            response = requests.get(url)
            soup = BeautifulSoup(response.content, 'lxml')

            links_page = []
            pages = 1

            for i in range(1, 4):
                try:
                    text = soup.find(text='{}'.format(str(i)))
                    parent = text.find_parent()
                    links_page.append('https://makeword.ru' + str(parent['href']))
                    pages += 1
                except:
                    if i == 1:
                        return url
                    elif i < 4:
                        return links_page

            return links_page


        def riphm(url):

            response = requests.get(url)
            soup = BeautifulSoup(response.content, 'lxml')

            texts = soup.find_all('a')
            words = []

            for text in texts:
                words.append(text.text)

            for i in range(0, len(words)):
                if words[i] == '\nРифма к слову\n':
                    first = i + 1
                elif words[i] == '1' or words[i] == '2' or words[i] == '3':
                    second = i
                    break
                elif 'Слова на букву' in words[i]:
                    second = i
                    break

            try:
                return words[first: second]
            except:
                pass


        def get_riphm(message):

            words = []
            links_page = (page('https://makeword.ru/rhyme/' + message.text))
            try:
                for i in range(0, len((links_page))):
                    words.append(riphm(links_page[i]))
            except:
                words.append(riphm(links_page))

            try:
                r = random.randint(0, len(words) - 1)
                actual_words = words[r]
                f = random.randint(0, len(actual_words) - 1)

                bot.send_message(message.from_user.id, actual_words[f])
            except:
                bot.send_message(message.from_user.id, 'Я не смог найти рифму, сообщи об этом создателю')

            bot.send_message(message.from_user.id,
                                 'Если хочешь еще рифму к этому слову- напиши "еще".'
                                 '\nЕсли хочешь закончить- напиши "хватит".'
                                 '\nХочешь рифму к другому слову- просто напиши это слово.')

            action = 'riphm'
            bot.register_next_step_handler(message, more, words, action)
            

        def more(message, words, action):

            if message.text.lower() == 'хватит':
                bot.send_message(message.from_user.id, 'Хорошо, закончим')

            elif action == 'riphm':

                if str(message.text.lower()).replace('ё', 'е') == 'еще':

                    r = random.randint(0, len(words) - 1)
                    actual_words = words[r]
                    f = random.randint(0, len(actual_words) - 1)

                    try:
                        bot.send_message(message.from_user.id, actual_words[f])
                        bot.send_message(message.from_user.id,
                                         'Если хочешь еще рифму к этому слову- напиши "еще".'
                                         '\nЕсли хочешь закончить- напиши "хватит".'
                                         '\nХочешь рифму к другому слову- просто напиши это слово.')
                        bot.register_next_step_handler(message, more, words, action)
                    except:
                        bot.send_message(message.from_user.id, 'Я не смог найти рифму, сообщи об этом создателю')

                else:
                    get_riphm(message)

            elif action == 'picture':

                if str(message.text.lower()).replace('ё', 'е') == 'еще':

                    r = random.randint(0, len(words))
                    try:
                        bot.send_message(message.from_user.id, words[r])
                        bot.send_message(message.from_user.id,
                                         'Если хочешь еще картинку к этому слову- напиши "еще".'
                                         '\nЕсли хочешь закончить- напиши "хватит".'
                                         '\nХочешь картинку по другому слову- просто напиши это слово.')
                        bot.register_next_step_handler(message, more, words, action)
                    except:
                        bot.send_message(message.from_user.id, 'Я не смог найти картинку, сообщи об этом создателю')

                else:
                    get_picture(message)


        def wait_graph(message):
            murkup = types.InlineKeyboardMarkup(row_width=3)
            button1 = types.InlineKeyboardButton('закончить', callback_data='leave')
            button3 = types.InlineKeyboardButton('помощь', callback_data='help')
            button2 = types.InlineKeyboardButton('продолжить', callback_data='continue')
            murkup.add(button1, button2, button3)

            bot.send_message(message.from_user.id,
                             '''Нужен график- нажми продолжить. Хочешь закончить- нажми взакончить. Нужна помощь- нажми справка.''',
                             reply_markup=murkup)


        ans = {'/reg': register,
               '/help': some_help}


        tipical_name_ans = {'привет': 'Ну привет, ',
                            'пока': 'Эх, пока, '}


        command_ans = {'картинка': wait,
                       'картинки': wait,
                       'как дела?': pleasent,
                       'как дела': pleasent,
                       'дела как?': pleasent,
                       'дела как': pleasent,
                       'как ты': pleasent,
                       'как ты?': pleasent,
                       'ты как?': pleasent,
                       'ты как': pleasent,
                       'рифма': wait_riphm,
                       'игра в рифмы': wait_riphm,
                       'скажи рифму': wait_riphm,
                       'дай рифму': wait_riphm,
                       'срифмуй': wait_riphm,
                       'рифмы': wait_riphm,
                       'график': wait_graph,
                       'построй график': wait_graph,
                       'нарисуй график': wait_graph,
                       'сделай график': wait_graph}


        @bot.message_handler(commands=['start'])
        def start_work(message):
            person_id = message.from_user.id
            first_name = message.from_user.first_name + ' ' + message.from_user.last_name

            try:
                search_name(person_id)
            except:
                if message.from_user.username == None:
                    set_new_name(person_id, first_name, first_name)
                else:
                    set_new_name(person_id, first_name, message.from_user.username)

            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            button1 = types.KeyboardButton('подбросить монетку')
            button2 = types.KeyboardButton('картинка')
            markup.add(button1, button2)

            bot.send_message(person_id, '''Привет, {}, я очень тупой бот (как и мой создатель).
        \nНо если хочешь поговорить- пиши.
        \nЧтобы узнать, что я могу ответить, набери /help'''.format(search_name(person_id)), reply_markup=markup)


        @bot.message_handler(content_types=['text'])
        def get_text_message(message):
            person_id = message.from_user.id
            first_name = message.from_user.first_name + ' ' + message.from_user.last_name

            try:
                search_name(person_id)
            except:
                if message.from_user.username == None:
                    set_new_name(person_id, first_name, first_name)
                else:
                    set_new_name(person_id, first_name, message.from_user.username)

            text_get = message.text.lower()

            if message.text[0] == '/':
                try:
                    ans[text_get](message)
                except:
                    bot.send_message(person_id, 'Я тебя не понимаю :(')

            elif tipical_name_ans.get(text_get, None) != None:
                bot_ans = tipical_name_ans[text_get]
                bot.send_message(person_id, bot_ans + search_name(person_id))

            elif command_ans.get(text_get, None) != None:
                command_ans[text_get](message)

            elif text_get == 'подбросить монетку':
                coin = random.randint(0, 1)
                if coin == 0:
                    bot.send_message(person_id, 'орел')
                else:
                    bot.send_message(person_id, 'решка')

            else:
                bot.send_message(person_id, 'Я тебя не понимаю :(')


        @bot.callback_query_handler(func=lambda call: True)
        def callback_ans(call):
            if call.message:
                if call.data == 'хорошо':
                    bot.send_message(call.message.chat.id, 'Это радует!')
                elif call.data == 'плохо':
                    bot.send_message(call.message.chat.id, 'Это печально :(')
                elif call.data == 'leave':
                    bot.send_message(call.message.chat.id, 'Хорошо, закончим')
                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                          text='''Нужен график- нажми продолжить. Хочешь закончить- нажми взакончить. Нужна помощь- нажми справка.''', reply_markup=None)
                elif call.data == 'help':
                    bot.send_message(call.message.chat.id, '''Вводить можно как функции вида y=f(x) / x=f(y), так и просто f(x) / f(y).\nНа пробелы и регистры можно не обращать внимания.
                    \nВсе функции должны закрываться скобкой, например sin(x). Обратные тригонометрические можно писать как: atan, asin, acos; либо cos^-1, sin^-1, tg^-1.
                    \n Не путай с tg(x)^-1 и т.д. по аналогии.
                    \nТак же учитывай диапазон x, если в нем будут недопустимые значения (например корень отицательного числа), тогда график не построится.''')
                elif call.data == 'continue':
                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                          text='Нужен график- нажми продолжить. Хочешь закончить- нажми взакончить. Нужна помощь- нажми справка.', reply_markup=None)
                    '''murkup = types.InlineKeyboardMarkup(row_width=2)
                    button1 = types.InlineKeyboardButton('закончить', callback_data='leave')
                    button2 = types.InlineKeyboardButton('помощь', callback_data='help')
                    murkup.add(button1, button2)'''
                    bot.send_message(call.message.chat.id, 'Напиши свою функцию, чтобы построить график.')

                    fig, ax = plt.subplots()
                    bot.register_next_step_handler(call.message, create, fig, ax)


        def create(message, fig, ax):
            ans = message.text.lower()
            ans = ans.replace(' ', '').replace('х', 'x').replace('у', 'y').replace('е', 'e')

            if 'y=' in ans or 'x=' in ans:
                pass
            else:
                if 'x' in ans:
                    ans = 'y=' + ans
                elif 'y' in ans:
                    ans = 'x=' + ans
                else:
                    ans = 'y=' + ans

            ans = ans.replace('tg^-1', 'atan').replace('sin^-1', 'asin').replace('cos^-1', 'acos')
            ans = ans.replace('^', '**').replace(',', '.').replace('tg', 'tan').replace('exp', 'r')
            for i in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
                ans = ans.replace('{}('.format(i), '{}*('.format(i))
                ans = ans.replace('{}sqrt'.format(i), '{}*sqrt'.format(i))
                ans = ans.replace('){}'.format(i), ')*{}'.format(i))
                ans = ans.replace('{}sin'.format(i), '{}*sin'.format(i))
                ans = ans.replace('{}cos'.format(i), '{}*cos'.format(i))
                ans = ans.replace('{}tan'.format(i), '{}*tan'.format(i))
                ans = ans.replace('{}e'.format(i), '{}*e'.format(i))
                ans = ans.replace('{}r'.format(i), '{}*r'.format(i))
                ans = ans.replace('{}x'.format(i), '{}*x'.format(i))
                ans = ans.replace('{}y'.format(i), '{}*y'.format(i))
                ans = ans.replace('{}pi'.format(i), '{}*pi'.format(i))

            bot.send_message(message.from_user.id, 'Задай начальное значение x или y')
            bot.register_next_step_handler(message, first_x, ans, fig, ax)


        def first_x(message, ans, fig, ax):
            first = float(message.text)
            bot.send_message(message.from_user.id, 'Задай конечное значение x или y')
            bot.register_next_step_handler(message, second_x, ans, first, fig, ax)


        def second_x(message, ans, first, fig, ax):
            second = float(message.text)
            step = (second - first) / 10000
            second = second - step
            try:
                build_graph(x1=first, x2=second, step=step, ans=ans, ax=ax)
                fig.savefig(str(message.from_user.id) + 'graph.png', dpi=100)
                bot.send_photo(message.from_user.id, photo=open(str(message.from_user.id) + 'graph.png', 'rb'))
                bot.send_message(message.from_user.id, 'Хочешь на этом закончить- напиши закончить. Хочешь добавить еще график к уже существующему - напиши добавить. Хочешь построить график заново- напиши график.')
                bot.register_next_step_handler(message, setting, fig, ax)
            except:
                bot.send_message(message.from_user.id, 'Не удалось построить график. Ты знаешь, кому об этом писать))')


        def setting(message, fig, ax):
            if message.text.lower() == 'закончить':
                bot.send_message(message.from_user.id, 'Хорошо, закончим')
            elif message.text.lower() == 'график':
                bot.send_message(message.from_user.id, 'Напиши свою функцию, чтобы построить график.')
                fig, ax = plt.subplots()
                bot.register_next_step_handler(message, create, fig, ax)
            elif message.text.lower() == 'добавить':
                bot.send_message(message.from_user.id, 'Напиши функцию, которую хочешь добавить.')
                bot.register_next_step_handler(message, create, fig, ax)


        bot.polling(none_stop=True, interval=0)
