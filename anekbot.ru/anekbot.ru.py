import requests
import html2text
import telebot
from telebot import types
import random

bot = telebot.TeleBot('token')
jokes = []

@bot.message_handler(commands = ["start"])
def start(m, res = False):
    markup = types.ReplyKeyboardMarkup(resize_keyboard = False)
    item0 = types.KeyboardButton("из этой же категории")
    item1 = types.KeyboardButton("оjcyjdе")
    item2 = types.KeyboardButton("лучшие прошлых лет")
    item3 = types.KeyboardButton("все новые за день")
    item4 = types.KeyboardButton("злободневные")
    item5 = types.KeyboardButton("без политики")
    item6 = types.KeyboardButton("приличные")
    item7 = types.KeyboardButton("авторские")
    markup.add(item0)
    markup.add(item1)
    markup.add(item2)
    markup.add(item3)
    markup.add(item4)
    markup.add(item5)
    markup.add(item6)
    markup.add(item7)
    bot.send_message(m.chat.id, 'Анекдоты взяты с сайта: https://www.anekdot.ru/ \n\n\nВыберете интересующую вас тему анекдотов из предложенного ниже списка:', reply_markup=markup)

@bot.message_handler(content_types = ["text"])


def handle_text(message):
    if message.text.strip() != "из этой же категории":
        s = requests.get('https://www.anekdot.ru')
        d = html2text.HTML2Text()
        d.ignore_links = False
        record = False
        part_link = ''
        c = d.handle(s.text)
        count = c.find(message.text.strip())
        jokes.clear()

        while(c[count] != ")"):
            if c[count - 1] == "(":
                record = True
            if record:
                part_link+=c[count]
            count+=1

        s = requests.get('https://www.anekdot.ru' + part_link)
        e = s.text
        
        while e.find('class="topicbox"') > 0:
            counter = e.find('class="text">')
            e = e[counter + 1:len(e)]
            counter = e.find('>') + 1
            tmp = ''
            while counter != e.find('</div>'):
                tmp+=e[counter]
                counter+=1
            tmp = tmp.replace('<br>','\n')
            jokes.append(tmp)
   
        bot.send_message(message.chat.id, random.choice(jokes))

    else:
        if  len(jokes) == 0:
            bot.send_message(message.chat.id, 'выберете категорию')
        else:
            bot.send_message(message.chat.id, random.choice(jokes))
            
bot.polling(none_stop = True, interval = 0)
