import random
from PIL import Image, ImageDraw
import requests
import sqlite3
import os
from vk_api import VkApi
from vk_api.upload import VkUpload
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from newsapi import NewsApiClient

vkToken = "токен группы"
newsToken = "токен news-api"
newsLink = "https://newsapi.org/v2/everything"
admin = "Ваш id вк"
club = "id группы"

# dicts
chat = {

}

maps = {

}

# Registration pgrases
phrases = ["Введите имя", "Введите фамилию", "Введите пол (м/ж)", "Отношение к курению?", "Семейное положение?",
           "Добавьте фото"]

# Состояния
state = {
}

condition = {
}

# Init vk_api
vk_session = VkApi(token=vkToken)
longpoll = VkBotLongPoll(vk_session, "194548161")
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


# Фото в серых тонах
def grey_photo(img, id):
    x = img.size[0]
    y = img.size[1]
    pix = img.load()
    draw = ImageDraw.Draw(img)
    for i in range(x):
        for j in range(y):
            a = pix[i, j][0]
            b = pix[i, j][1]
            c = pix[i, j][2]
            S = (a + b + c) // 3
            draw.point((i, j), (S, S, S))
    img.save("photos/" + str(id) + "2.jpg", "JPEG")
    img.close()


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


def down_photo(url, id):
    resp = requests.get(url)
    filename = "photos/" + str(id) + ".jpg"
    with open(filename, "wb") as img:
        img.write(resp.content)


while True:
    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            if event.message.text.lower() == "шевцов лох?":
                peer_id = event.object.message['peer_id']
                vk.messages.send(
                    random_id=rand(),
                    peer_id=peer_id,
                    message="Да, еще какой",
                )
            elif "ставь лайк" in event.message.text.lower() and "леха" not in event.message.text.lower() and "леху" not in event.message.text.lower():
                peer_id = event.object.message['peer_id']
                vk.messages.send(
                    random_id=rand(),
                    peer_id=peer_id,
                    message="Лайк &#128077;",
                )
            elif event.message.text.lower() == "!новости" and event.message.from_id not in condition:
                peer_id = event.object.message['peer_id']
                personId = event.message.from_id
                condition[personId] = "новости"
                vk.messages.send(
                    random_id=rand(),
                    peer_id=peer_id,
                    message="Про что вывести новости?(!выход если не хочешь искать новости)",
                )
            elif "!шанс" in event.message.text.lower():
                peer_id = event.object.message['peer_id']
                vk.messages.send(
                    random_id=rand(),
                    peer_id=peer_id,
                    message=f"Шанс этого {random.randint(0, 100)}%",
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
            elif event.message.text.lower() == "!моя анкета":
                peer_id = event.object.message['peer_id']
                personId = event.message.from_id
                message = showProfile(personId)
                vk.messages.send(
                    peer_id=peer_id,
                    message=message[0],
                    random_id=rand(),
                    attachment = "photo"+str(admin)+"_"+str(message[1])
                )
            elif event.message.text.lower() == "!удалить анкету":
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
            elif event.message.text.lower() == "!help":
                peer_id = event.object.message['peer_id']
                vk.messages.send(
                    random_id=rand(),
                    peer_id=peer_id,
                    message=f"Команды:\n"
                            f"🔹 Шевцов лох?\n"
                            f"🔹 !Шанс (можно писать в любом месте предложения)\n"
                            f"🔹 Ставь лайк\n"
                            f"🔹 !Новости\n"
                            f"🔹 !Кто\n"
                            f"🔹 !Регистрация\n"
                            f"🔹 !Моя анкета\n"
                            f"🔹 !Удалить анкету\n"
                            f"🔹 !Фото\n"
                            f"🔹 !Пик\n"
                            f"🔹 !Поиск\n",
                )
            elif event.message.text.lower() == "!фото" and event.message.from_id not in condition:
                condition[event.message.from_id] = "фото"
                vk.messages.send(
                    peer_id=event.object.message['peer_id'],
                    random_id=rand(),
                    message="Скинь свое фото &#128527;"
                )
            elif "!кто" in event.message.text.lower() or "!кого" in event.message.text.lower():
                peer_id = event.object.message['peer_id']
                vk.messages.send(
                    random_id=rand(),
                    peer_id=peer_id,
                    message=f"Я думаю, это {chat[random.randint(1, 7)]} &#128533;",
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
                    message=message + f"Самые свежие новости для тебя, семпай &#128525;",
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
            elif event.message.from_id in condition and condition[event.message.from_id] == "фото":
                url = event.object.message['attachments'][0]['photo']['sizes'][-1]['url']
                down_photo(url, event.message.from_id)
                image = Image.open('photos/' + str(event.message.from_id) + ".jpg")
                grey_photo(image, event.message.from_id)

                data = vk.photos.getMessagesUploadServer(peer_id=admin)
                url = data['upload_url']
                fp = open(r'photos/' + str(event.message.from_id) + '2.jpg', 'rb')
                img = {'photo': ('photos/' + str(event.message.from_id) + '2.jpg', fp)}
                r = requests.post(url, files=img)
                r = r.json()
                server = r['server']
                photo = r['photo']
                hash = r['hash']
                photo_id = vk.photos.saveMessagesPhoto(server=server, photo=photo, hash=hash)
                photo_id = photo_id[0]['id']
                fp.close()

                vk.messages.send(
                    peer_id=event.object.message['peer_id'],
                    random_id=rand(),
                    message="Фото уже готово &#128515;",
                    attachment="photo" + str(admin) + "_" + str(photo_id),
                )
                os.remove("photos/" + str(event.message.from_id) + ".jpg")
                os.remove("photos/" + str(event.message.from_id) + "2.jpg")
                condition.pop(event.message.from_id)
