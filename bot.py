import traceback
import datetime
import time
import pytz
import numpy as np
import pyowm
import random
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import valve.source.a2s as vl
import threading
from PIL import Image, ImageDraw
import requests
from bs4 import BeautifulSoup as BS
import sqlite3
import os
from vk_api import VkApi
from vk_api.upload import VkUpload
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from newsapi import NewsApiClient

vkToken = ""
newsToken = ""
weather = ""
newsLink = "https://newsapi.org/v2/everything"
admin = 
club = 
conf = 
conf2 = 

owm = pyowm.OWM(weather, language = "RU")
maps = {
    1: "Mirage &#128542;",
    2: "Cache &#128539;",
    3: "Dust 2 &#128522;",
    4: "Inferno &#128521;",
    7: "Dust 2 &#128522;",
    5: "Train &#128526;",
    6: "Overpass &#128525;",
}

# Registration phrases
phrases = ["Введите имя", "Введите фамилию", "Введите пол (м/ж)", "Отношение к курению?", "Семейное положение?",
           "Добавьте фото"]

# Состояния
state = {
}


condition = {
}

#Weather
status ={
    1: 'Рекомендую надеть осеннюю куртку, кофту, футболку.',
    2: 'Рекомендую надеть ветровку, кофту, футболку.',
    3: 'Рекомендую надеть кофту, футболку.',
    4: 'Рекомендую надеть легкую кофту, футболку с рукавом.',
    5: 'Рекомендую надеть головной убор, футболку, шорты.',
    6: 'Рекомендую надеть головной убор, футболку, шорты.',
    7: 'Рекомендую надеть зимнюю куртку, кофту, футболку.',
    8: 'Рекомендую надеть зимнюю куртку, кофту, футболку, шапку, шарф.',
    9: 'Рекомендую надеть зимнюю куртку, кофту, футболку, шапку, шарф.',
    10: 'Рекомендую надеть шапку, куртку, толстовку. Не забывайте о шарфе и перчатках!',
    11: 'Рекомендую надеть зимнюю куртку, кофту, футболку, термобелье. Не забывайте о шарфе и перчатках!',
    12: 'Рекомендую надеть зимнюю куртку, кофту, футболку, термобелье. Не забывайте о шарфе и перчатках!',
}
#Сервера
servers = {
    "МЕДВЕДИ".lower(): ('46.174.49.123', '27015'),
    "EXTREME".lower(): ('212.22.93.49', '27040')
}

players = {
}
# Init vk_api
vk_session = VkApi(token=vkToken)
longpoll = VkBotLongPoll(vk_session, club)
vk = vk_session.get_api()
upload = VkUpload(vk_session)

# Init news_api
newsapi = NewsApiClient(api_key=newsToken)


global Random


def rand():
    Random = 0
    Random = random.randint(0, 10 ** 90)
    return Random


# Get news by query
def getNews(query):
    news = newsapi.get_everything(q=query)
    return news["articles"]


# Create string for message
def renderNews(news):
    message = ""
    for i in news:
        message += f"{i['title']}\n" \
                   f"{i['url']}\n\n"
    return message


# Create User
def createUser(user):
    try:
        conn = sqlite3.connect("botBD.db")
        cursor = conn.cursor()
        cursor.execute("insert into user values (?, ?, ?, ?, ?, ?, ?)",
                       (user[1], user[2], user[3], user[4], user[5], user[6], user[7]))
        conn.commit()
        conn.close()
        if user[7] != None:
            down_photo(user[7], user[1])
            photo_id = send_photo(user[1])
            message = [f"Ваша анкета:\n" \
                       f"Имя: {user[2]}\n" \
                       f"Фамилия: {user[3]}\n" \
                       f"Пол: {user[4]}\n" \
                       f"Отношение к курению: {user[5]}\n" \
                       f"Семейное положение: {user[6]}\n ", photo_id]
            state.pop(user[1])
            return message
        else:
            message = [f"Ваша анкета:\n" \
                       f"Имя: {user[2]}\n" \
                       f"Фамилия: {user[3]}\n" \
                       f"Пол: {user[4]}\n" \
                       f"Отношение к курению: {user[5]}\n" \
                       f"Семейное положение: {user[6]}\n ", None]
            state.pop(user[1])
            return message
    except:
        message = ["Ошибка создания анкеты &#128522;", None]
        state.pop(user[1])
        return message


def showProfile(id):
    try:
        conn = sqlite3.connect("botBD.db")
        cursor = conn.cursor()
        cursor.execute("select * from user where id = :id", {"id": id})
        profile = cursor.fetchone()
        conn.close()
        if profile[6] != None:
            down_photo(profile[6], profile[0])
            photo_id = send_photo(profile[0])
            message = [f"Ваша анкета:\n" \
                      f"Имя: {profile[1]}\n" \
                      f"Фамилия: {profile[2]}\n" \
                      f"Пол: {profile[3]}\n" \
                      f"Отношение к курению: {profile[4]}\n" \
                      f"Семейное положение: {profile[5]}\n", photo_id]
            return message
        else:
            message = [f"Ваша анкета:\n" \
                       f"Имя: {profile[1]}\n" \
                       f"Фамилия: {profile[2]}\n" \
                       f"Пол: {profile[3]}\n" \
                       f"Отношение к курению: {profile[4]}\n" \
                       f"Семейное положение: {profile[5]}\n", None]
            return message
    except:
        message = ["Вашей анкеты нет, зарегистрируйтесь)", None]
        return message


def deleteUser(id):
    try:
        conn = sqlite3.connect("botBD.db")
        cursor = conn.cursor()
        cursor.execute("delete from user where id = :id", {"id": id})
        conn.commit()
        conn.close()
        message = "Ваша анкета успешно удалена &#128521;"
        return message
    except:
        message = "Не удалось удалить вашу анкету &#128542;"
        return message

# Create character
def create_character(character, id):
    try:
        conn = sqlite3.connect("characters.db")
        cursor = conn.cursor()
        cursor.execute("insert into characters values(?,?,?,?,?,?,?,?,?)",
                       (id, character.name, character.exp, character.exp_next_lvl, character.lvl, character.str,
                        character.agil, character.int, str(character.inventory)))
        conn.commit()
        conn.close()
        message = f"Ваш персонаж:\n" \
                  f"Имя: {character.name}\n" \
                  f"Опыт: {character.exp}\n" \
                  f"Опыт для лвл апа: {character.exp_next_lvl}\n" \
                  f"Уровень: {character.lvl}\n" \
                  f"Сила: {character.str}\n" \
                  f"Ловкость: {character.agil}\n" \
                  f"Интелект: {character.int}\n" \
                  f"Инвентарь: {str(character.inventory)}\n"
        return message
    except:
        message = "ошибка"
        return message

# Search
def getSex(id):
    conn = sqlite3.connect("botBD.db")
    c = conn.cursor()
    c.execute("select sex from user where id = :id", {"id": id})
    sex = c.fetchone()
    conn.close()
    return sex


def getUser(sex):
    try:
        conn = sqlite3.connect("botBD.db")
        c = conn.cursor()
        if sex[0] == "м":
            c.execute("SELECT * FROM user where sex = 'ж' ORDER BY RANDOM() LIMIT 1;")
            user = c.fetchone()
            if user[6] != None:
                down_photo(user[6], user[0])
                photo_id = send_photo(user[0])
                message = [f"Нашел кое кого для тебя:\n 1) Подходит, остановить поиск; 2) Искать дальше\n" \
                           f"Имя: {user[1]}\n" \
                           f"Фамилия: {user[2]}\n" \
                           f"Отношение к курению: {user[4]}\n" \
                           f"Семейное положение: {user[5]}\n ", user[0], photo_id]
                conn.close()
                return message
            else:
                message = [f"Нашел кое кого для тебя:\n 1) Подходит, остановить поиск; 2) Искать дальше\n" \
                           f"Имя: {user[1]}\n" \
                           f"Фамилия: {user[2]}\n" \
                           f"Отношение к курению: {user[4]}\n" \
                           f"Семейное положение: {user[5]}\n ", user[0], None]
                conn.close()
                return message
        elif sex[0] == "ж":
            c.execute("SELECT * FROM user where sex = 'м' ORDER BY RANDOM() LIMIT 1;")
            user = c.fetchone()
            if user[6] != None:
                down_photo(user[6], user[0])
                photo_id = send_photo(user[0])
                message = [f"Нашел кое кого для тебя:\n 1) Подходит, остановить поиск; 2) Искать дальше\n" \
                           f"Имя: {user[1]}\n" \
                           f"Фамилия: {user[2]}\n" \
                           f"Отношение к курению: {user[4]}\n" \
                           f"Семейное положение: {user[5]}\n ", user[0], photo_id]
                conn.close()
                return message
            else:
                message = [f"Нашел кое кого для тебя:\n 1) Подходит, остановить поиск; 2) Искать дальше\n" \
                           f"Имя: {user[1]}\n" \
                           f"Фамилия: {user[2]}\n" \
                           f"Отношение к курению: {user[4]}\n" \
                           f"Семейное положение: {user[5]}\n ", user[0], None]
                conn.close()
                return message
    except:
        message = ["Кажется вы еще не зарегистрированы((", None]
        return message



# Download and Upload
def send_photo(id):
    data = vk.photos.getMessagesUploadServer(peer_id=admin)
    url = data['upload_url']
    fp = open(r'photos/' + str(id) + '.jpg', 'rb')
    img = {'photo': ('photos/' + str(id) + '.jpg', fp)}
    r = requests.post(url, files=img)
    r = r.json()
    server = r['server']
    photo = r['photo']
    hash = r['hash']
    photo_id = vk.photos.saveMessagesPhoto(server=server, photo=photo, hash=hash)
    photo_id = photo_id[0]['id']
    fp.close()
    os.remove("photos/"+str(id)+".jpg")
    return photo_id

def send_file(id):
    data = vk.docs.getMessagesUploadServer(type="doc", peer_id=admin)
    url = data['upload_url']
    ft = open(r'docs/'+str(id)+'.txt', 'rb')
    txt = {'file': (f'docs/{str(id)}.txt', ft)}
    rr = requests.post(url, files=txt)
    rr = rr.json()
    file = rr['file']
    file_id = vk.docs.save(file=file)
    file_id = file_id['doc']['id']
    ft.close()
    os.remove(f"docs/{str(id)}.txt")
    return file_id

def down_photo(url, id):
    resp = requests.get(url)
    filename = "photos/" + str(id) + ".jpg"
    with open(filename, "wb") as img:
        img.write(resp.content)

#Получить количество игроков
def get_players():
    threading.Timer(300.0, get_players).start()
    for name in servers:
        with vl.ServerQuerier((servers[name][0],int(servers[name][1]))) as server:
            if name not in players:
                players[name] = [0]
            if players[name][0] == 288:
                copy = players[name][288::]
                players[name] = [0]
                players[name].append(copy[0::])
            moscow_time = datetime.datetime.now(pytz.timezone("Europe/Moscow"))
            m_time = moscow_time.strftime("%H:%M")
            players[name].append(server.info()["player_count"])
            players[name].append(m_time)
            players[name][0] += 1
get_pl = True
if get_pl:
    get_players()
    get_pl = False

#отрисовка графика
def drow_graph(id, serv):
    try:
        with vl.ServerQuerier((servers[serv][0], int(servers[serv][1]))) as server:
            name = server.info()["server_name"]
        plt.title(str(servers[serv][0])+":"+str(servers[serv][1]))
        plt.xlabel("Время")
        plt.ylabel("Игроков")
        ax = plt.gca()
        img = plt.imread("photos/back.jpg")
        mas = players[serv][1:len(players[serv]):2]
        ax.imshow(img, extent=[0, len(mas), 0, max(mas) + 20])
        ox = players[serv][2:len(players[serv]):2]
        ax.xaxis.set_major_locator(ticker.MultipleLocator(12))
        ax.yaxis.set_minor_locator(ticker.MultipleLocator(5))
        ax.tick_params(axis='both',  # Применяем параметры к обеим осям
                       which='major',  # Применяем параметры к основным делениям
                       direction='inout',  # Рисуем деления внутри и снаружи графика
                       length=8,  # Длинна делений
                       width=1,  # Ширина делений
                       color='b',  # Цвет делений
                       pad=0,  # Расстояние между черточкой и ее подписью
                       labelsize=9,  # Размер подписи
                       labelcolor='r',  # Цвет подписи
                       bottom=True,  # Рисуем метки снизу
                       left=True,  # слева
                       labelbottom=True,  # Рисуем подписи снизу
                       labelleft=True,  # слева
                       labelrotation=30)  # Поворот подписей

        plt.plot(ox, mas, color = "green", label = str(name), linewidth=0.90)
        ax.legend(loc = "upper left")
        ax.fill_between(ox[0:], mas[0:], 0, facecolor="#0ef", interpolate=True, alpha=0.7)
        plt.savefig("photos/" + str(id) + '.jpg', format='JPEG', dpi=100)
        plt.clf()
    except:
        vk.messages.send(
            peer_id=peer_id,
            random_id=rand(),
            message="Видимо не было еще ниодного запроса на сервер, подождите",
        )

#WEATHER
def weather_message(temp, stat):
    zont =  ""
    message = f"Температура воздуха: {temp}°\n"
    if "дождь" not in stat.lower():
        message += "&#9728; Осадков на улице не предвидится. "
    else:
        message += "&#127783; Осадки в виде дождя. "
        zont += " Не забывайте про зонт!"
    if temp >= 0 and temp <=5:
        stats = 1
    elif temp > 5 and temp <=10:
        stats = 2
    elif temp > 10 and temp <=15:
        stats = 3
    if temp > 15 and temp <=20:
        stats = 4
    elif temp > 20 and temp <=25:
        stats = 5
    elif temp > 25:
        stats = 6
    elif temp < 0 and temp >= -5:
        stats = 7
    elif temp < -5 and temp >= -10:
        stats = 8
    elif temp < -10 and temp >= -15:
        stats = 9
    elif temp < -15 and temp >= -20:
        stats = 10
    elif temp < -20 and temp >= -25:
        stats = 11
    elif temp < -25:
        stats = 12
    message += status[stats]
    if zont != "":
        message += zont
    return message

#music
def parsing(id, url):
    flag = True
    r = requests.get(url)
    r = r.content
    html = BS(r, "html.parser")
    with open(f"docs/{str(id)}.txt", 'w') as file:
        for el in html.select(".string_container"):
            original = el.select(".original")[0].text
            translate = el.select(".translate")[0].text
            if flag:
                file.write(f"{original}\n{translate}\n\n")
                flag = False
                continue
            file.write(f"{original}{translate}\n\n")

while True:
    try:
        for event in longpoll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW:
                if event.message.text.lower() == "!новости" and event.message.from_id not in condition:
                    peer_id = event.object.message['peer_id']
                    personId = event.message.from_id
                    condition[personId] = "новости"
                    vk.messages.send(
                        random_id=rand(),
                        peer_id=peer_id,
                        message="Про что вывести новости?(!выход если не хочешь искать новости)",
                    )
                elif event.message.text.lower() == "!регистрация" and event.message.from_id not in condition:
                    peer_id = event.object.message['peer_id']
                    personId = event.message.from_id
                    condition[personId] = ["регистрация"]
                    vk.messages.send(
                        peer_id=peer_id,
                        random_id=rand(),
                        message="Сейчас начнется небольшая регистрация. Вы готовы? &#128578;"
                    )
                    if personId not in state:
                        condition[personId].append(True)
                elif event.message.text.lower() == "!моя анкета" and event.message.from_id not in condition:
                    peer_id = event.object.message['peer_id']
                    personId = event.message.from_id
                    message = showProfile(personId)
                    vk.messages.send(
                        peer_id=peer_id,
                        message=message[0],
                        random_id=rand(),
                        attachment = "photo"+str(admin)+"_"+str(message[1])
                    )
                elif event.message.text.lower() == "!удалить анкету" and event.message.from_id not in condition:
                    peer_id = event.object.message['peer_id']
                    personId = event.message.from_id
                    message = deleteUser(personId)
                    vk.messages.send(
                        peer_id=peer_id,
                        random_id=rand(),
                        message=message,
                    )
                elif event.message.text.lower() == "!пик" or event.message.text.lower() == "!карта":
                    peer_id = event.object.message['peer_id']
                    vk.messages.send(
                        random_id=rand(),
                        peer_id=peer_id,
                        message=f"Играем {maps[random.randint(1, 7)]}",
                    )
                elif event.message.text.lower() == "!поиск" and event.message.from_id not in condition:
                    peer_id = event.object.message['peer_id']
                    personId = event.message.from_id
                    sex = getSex(personId)
                    condition[personId] = ["поиск", sex, True]
                    vk.messages.send(
                        random_id=rand(),
                        peer_id=peer_id,
                        message="Сейчас начнется поиск"
                    )
                elif event.message.text.lower() == "!погода" and event.message.from_id not in condition:
                    peer_id = event.object.message['peer_id']
                    condition[event.message.from_id] = 'погода'
                    vk.messages.send(
                        peer_id = peer_id,
                        random_id = rand(),
                        message = "В каком городе вывести погоду?"
                    )
                elif event.message.text.lower() == "!перевод" and event.message.from_id not in condition:
                    peer_id = event.object.message['peer_id']
                    condition[event.message.from_id] = "перевод"
                    vk.messages.send(
                        peer_id = peer_id,
                        random_id = rand(),
                        message = "Скиньте ссылку на песню, которую нужно запарсить."
                    )
                elif event.message.text.lower() == "!help" and event.message.from_id not in condition:
                    peer_id = event.object.message['peer_id']
                    vk.messages.send(
                        random_id=rand(),
                        peer_id=peer_id,
                        message=f"Команды:\n"
                                f"🔹 !погода\n"
                                f"🔹 !Новости\n"
                                f"🔹 !Регистрация\n"
                                f"🔹 !Моя анкета\n"
                                f"🔹 !Удалить анкету\n"
                                f"🔹 !Фото\n"
                                f"🔹 !Пик\n"
                                f"🔹 !Поиск\n"
                                f"🔹 !Добавить сервер\n"
                                f"🔹 !График\n"
                    )
                elif event.message.text.lower() == "!добавить сервер" and event.message.from_id not in condition:
                    peer_id = event.object.message['peer_id']
                    condition[event.message.from_id] = ['добавление', 0]
                    vk.messages.send(
                        peer_id = peer_id,
                        random_id = rand(),
                        message = "Введите название сервера"
                    )
                elif event.message.text.lower() == "!график" and event.message.from_id not in condition:
                    peer_id = event.object.message['peer_id']
                    condition[event.message.from_id] = 'график'
                    vk.messages.send(
                        peer_id=peer_id,
                        random_id=rand(),
                        message="График посещений какого сервера вы хотели бы получить?"
                    )
                # проверка состояний
                elif event.message.from_id in condition and condition[event.message.from_id] == "новости":
                    if event.message.text.lower() == "!выход":
                        vk.messages.send(
                            random_id=rand(),
                            peer_id=event.object.message['peer_id'],
                            message=f"Как жаль, что ты не узнаешь что творится в мире &#128530;",
                        )
                        condition.pop(event.message.from_id)
                        continue
                    query = event.message.text
                    news = getNews(query)
                    message = renderNews(news)
                    vk.messages.send(
                        random_id=rand(),
                        peer_id=event.object.message['peer_id'],
                        message=message + f"Самые свежие новости для тебя &#128525;",
                    )
                    condition.pop(event.message.from_id)
                elif event.message.from_id in condition and condition[event.message.from_id][0] == "регистрация":
                    if event.message.from_id in state:
                        i = state[event.message.from_id][0] or 0
                    else:
                        state[event.message.from_id] = [0]
                        i = state[event.message.from_id][0]
                        state[event.message.from_id].append(event.message.from_id)
                    if event.message.text.lower() == "!выход" or event.message.text.lower() == "нет":
                        vk.messages.send(
                            random_id=rand(),
                            peer_id=event.object.message['peer_id'],
                            message=f"Жаль что мы не познакомимся поближе(",
                        )
                        condition.pop(event.message.from_id)
                        if state[event.message.from_id][0] !=0:
                            state[event.message.from_id][0] -= 1
                        if state[event.message.from_id][0] == 0 or state[event.message.from_id][0] == 1:
                            state.pop(event.message.from_id)
                        continue
                    if i != 0 and i != 6:
                        vk.messages.send(
                            random_id=rand(),
                            peer_id=event.object.message['peer_id'],
                            message=phrases[i],
                        )
                    elif i == 6:
                        if event.object.message['attachments'] != [] and event.object.message['attachments'][0]['photo']['sizes'] !=[]:
                            reg_url = event.object.message['attachments'][0]['photo']['sizes'][-1]['url']
                            state[event.message.from_id].append(reg_url)
                        vk.messages.send(
                            random_id=rand(),
                            peer_id=event.object.message['peer_id'],
                            message="Регистрация почти завершена, сейчас проверю, нет ли вас в базе &#128522;",
                        )
                    elif condition[event.message.from_id][1]:
                        flag = False
                        vk.messages.send(
                            random_id=rand(),
                            peer_id=event.object.message['peer_id'],
                            message=phrases[i],
                        )
                        state[event.message.from_id][0] += 1
                        continue
                    state[event.message.from_id].append(event.message.text)
                    if i == 6:
                        message = createUser(state[event.message.from_id])
                        vk.messages.send(
                            random_id=rand(),
                            peer_id=event.object.message['peer_id'],
                            message=message[0],
                            attachment="photo" + str(admin) + "_" + str(message[1])
                        )
                        condition.pop(event.message.from_id)
                    if event.message.from_id in state:
                        state[event.message.from_id][0] += 1
                elif event.message.from_id in condition and condition[event.message.from_id][0] == "поиск":
                    if event.message.text.lower() == "!выход":
                        vk.messages.send(
                            peer_id=event.object.message['peer_id'],
                            random_id=rand(),
                            message="Поиск прекращен &#128527;"
                        )
                        condition.pop(event.message.from_id)
                        continue
                    if condition[event.message.from_id][2]:
                        message = getUser(condition[event.message.from_id][1])
                        condition[event.message.from_id][2] = False
                        vk.messages.send(
                            peer_id=event.object.message['peer_id'],
                            random_id=rand(),
                            message=message[0],
                            attachment="photo" + str(admin) + "_" + str(message[2]),
                        )
                        condition[event.message.from_id].append(message[1])
                        message = getUser(condition[event.message.from_id][1])
                        continue
                    if event.message.text.lower() == "2" or event.message.text.lower() == "ок":
                        vk.messages.send(
                            peer_id=event.object.message['peer_id'],
                            random_id=rand(),
                            message=message[0],
                            attachment = "photo"+str(admin)+"_"+str(message[2]),
                        )
                        condition[event.message.from_id][3] = message[1]
                    if event.message.text.lower() == "1":
                        vk.messages.send(
                            peer_id=event.object.message['peer_id'],
                            random_id=rand(),
                            message=f"Надеюсь вы подружитесь &#129303;\n"
                                    f"https://vk.com/id{condition[event.message.from_id][3]}"
                        )
                        condition.pop(event.message.from_id)
                        continue
                    message = getUser(condition[event.message.from_id][1])
                elif event.message.from_id in condition and condition[event.message.from_id][0] == "добавление":
                    try:
                        if event.message.text.lower() == "!выход":
                            vk.messages.send(
                                random_id=rand(),
                                peer_id=event.object.message['peer_id'],
                                message=f"А я так хотела последить за активностью твоего сервера &#128553;",
                            )
                            condition.pop(event.message.from_id)
                            continue

                        if condition[event.message.from_id][1] == 0:
                            vk.messages.send(
                                random_id=rand(),
                                peer_id=event.object.message['peer_id'],
                                message=f"Ведите адресс сервера: 'ip:port'",
                            )
                            condition[event.message.from_id][1] += 1
                            condition[event.message.from_id].append(event.message.text.lower())
                            continue
                        vk.messages.send(
                            random_id=rand(),
                            peer_id=event.object.message['peer_id'],
                            message=f"Сервер успешно добавлен.",
                        )
                        servers[condition[event.message.from_id][2]] = tuple(event.message.text.split(":"))
                        condition.pop(event.message.from_id)
                        continue
                    except:
                        vk.messages.send(
                            random_id=rand(),
                            peer_id=event.object.message['peer_id'],
                            message=f"Возникла какая то ошибка, возможно ваш сервер уже добавлен.",
                        )
                elif event.message.from_id in condition and condition[event.message.from_id] == "график":
                    if event.message.text.lower() == "!выход":
                        vk.messages.send(
                            random_id=rand(),
                            peer_id=event.object.message['peer_id'],
                            message=f"Жаль что ты не увидишь активность своего сервера(",
                        )
                        condition.pop(event.message.from_id)
                        continue
                    if event.message.text.lower() in players and len(players[event.message.text.lower()]) < 30:
                        vk.messages.send(
                            random_id=rand(),
                            peer_id=event.object.message['peer_id'],
                            message=f"Извините, но пока собрано слишком мало информации о сервере, подождите &#128564;",
                        )
                        condition.pop(event.message.from_id)
                        continue
                    drow_graph(event.message.from_id, event.message.text.lower())
                    photo_id = send_photo(event.message.from_id)
                    vk.messages.send(
                        peer_id=peer_id,
                        random_id=rand(),
                        message="Вот ваш график &#128578;",
                        attachment = "photo" + str(admin) + "_" + str(photo_id),
                    )
                    condition.pop(event.message.from_id)
                elif event.message.from_id in condition and condition[event.message.from_id] == "название":
                    if event.message.text.lower() == "!выход":
                        vk.messages.send(
                            random_id=rand(),
                            peer_id=event.object.message['peer_id'],
                            message=f"А я так хотела последить за активностью твоего сервера &#128553;",
                        )
                        condition.pop(event.message.from_id)
                        continue
                    peer_id = event.object.message['peer_id']
                    vk.messages.editChat(chat_id = peer_id - 2000000000,title = event.message.text)
                    vk.messages.send(
                        random_id=rand(),
                        peer_id=peer_id,
                        message=f"Название успешно изменено &#128521;",
                    )
                    condition.pop(event.message.from_id)
                elif event.message.from_id in condition and condition[event.message.from_id] == "погода":
                    try:
                        peer_id = event.object.message['peer_id']
                        city = event.message.text
                        obs = owm.weather_at_place(city)
                        w = obs.get_weather()
                        temp = w.get_temperature('celsius')['temp']
                        stat = w.get_detailed_status()
                        w_message = weather_message(temp, stat)
                        vk.messages.send(
                            peer_id = peer_id,
                            random_id = rand(),
                            message = w_message
                        )
                        condition.pop(event.message.from_id)
                    except:
                        vk.messages.send(
                            peer_id=peer_id,
                            random_id=rand(),
                            message=f'Вы уверены что такой город существует?'
                        )
                        condition.pop(event.message.from_id)
                elif event.message.from_id in condition and condition[event.message.from_id] == "перевод":
                    if event.message.text.lower() == "!выход":
                        vk.messages.send(
                            random_id=rand(),
                            peer_id=event.object.message['peer_id'],
                            message=f"Жаль что ты не увидишь активность своего сервера(",
                        )
                        condition.pop(event.message.from_id)
                        continue
                    peer_id = event.object.message['peer_id']
                    parsing(event.message.from_id, event.message.text)
                    id_f = send_file(event.message.from_id)
                    vk.messages.send(
                        peer_id=peer_id,
                        random_id=rand(),
                        message = "Файл готов.",
                        attachment=f"doc{str(admin)}_{str(id_f)}"
                    )
                    condition.pop(event.message.from_id)



    except Exception as err:
        with open("err_log.txt", "a") as log:
            log.write(f"{traceback.format_exc()} {str(datetime.datetime.now())}\n\n")
        vk.messages.send(
            random_id=rand(),
            peer_id=admin,
            message=f"Вылет",
        )
        condition = {}




