# v0.4
#
#

import config
import telebot
from SQLite3 import SQLighter

bot = telebot.TeleBot(config.token)
day = ''
day_delete = ''

@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    chat_id = message.chat.id
    msg = bot.reply_to(message, """\
Я бот-ассистент, напиши день, на который тебе назначить встречу, я его запомню
""")

@bot.message_handler(content_types=["text"])
def walk_get_day(message):  # Название функции не играет никакой роли, в принципе
    global day
    day = message.text
    name = message.from_user.first_name
    chat_id = message.chat.id
    user_id = message.from_user.id
    username = message.from_user.username
    if str.lower(message.text) != "удалить":
        bot.send_message(message.chat.id,
                     "{}({}) планирует прогулку в эту/это/этот: {}".format(name, username, message.text))
        msg = bot.reply_to(message, "С кем планируете прогулку?")
        bot.register_next_step_handler(msg, reply_to_another_user)
        db_worker = SQLighter(config.database)

        write_to_DB = db_worker.write_to(chat_id, user_id, username, message.text)

        db_worker.close()
    else:
        msg = bot.reply_to(message, "какой день удалить?")
        bot.register_next_step_handler(msg, delete_day_select_day)



@bot.message_handler(content_types=['contact'])
def reply_to_another_user(message):
    username = message.from_user.username
    db_worker = SQLighter(config.database)
    print(message)
    print(message.contact.user_id)
    userID = message.contact.user_id
    print(userID)
    get_ID = db_worker.getID(userID)
    print(get_ID)
    get_ID = "{}".format(''.join(str(x) for x in get_ID).replace('(', '').replace(')', '').replace('\'', '')[:-1])
    print(get_ID)
    bot.send_message(get_ID, "У вас прогулка с {} {} в {}".format(message.from_user.first_name, message.from_user.
                                                                  last_name, day))
    read_from_DB = db_worker.read_my_data(username)

    bot.send_message(message.chat.id,
                     "У вас запланированы прогулки на следующие дни: {} с {} {}".format(
                         ''.join(str(x) for x in read_from_DB).
                         replace('(', '').replace(')', '').
                         replace('\'', '').replace(',', ', ')[:-1],
                         message.contact.first_name,
                         message.contact.last_name)[:-2])
    db_worker.close()



@bot.message_handler(content_types=["text"])
def delete_day_select_day(message):
    global day_delete
    day_delete = message.text

    msg = bot.reply_to(message, "С кем отменяете прогулку?")
    bot.register_next_step_handler(msg, reply_to_another_user_about_delete)


@bot.message_handler(content_types=['contact'])
def reply_to_another_user_about_delete(message):
    username = message.from_user.username
    db_worker = SQLighter(config.database)
    userID = message.contact.user_id
    get_ID = db_worker.getID(userID)
    get_ID = "{}".format(''.join(str(x) for x in get_ID).replace('(', '').replace(')', '').replace('\'', '')[:-1])
    db_worker = SQLighter(config.database)
    delete_from_db = db_worker.delete_row(day_delete, message.from_user.id, get_ID)
    db_worker.close()
    bot.send_message(get_ID, "У вас отменяется прогулка с {} {}  в {}".format(message.from_user.first_name, message.from_user.
                                                                  last_name, day_delete))
    read_from_DB = db_worker.read_my_data(username)

    bot.send_message(message.chat.id,
                     "У вас запланированы прогулки на следующие дни: {} с {} {}".format(
                         ''.join(str(x) for x in read_from_DB).
                             replace('(', '').replace(')', '').
                             replace('\'', '').replace(',', ', ')[:-1],
                         message.contact.first_name,
                         message.contact.last_name)[:-2])
    db_worker.close()

# @bot.message_handler(commands=['getid'])
# def getuserid(ID):  # Название функции не играет никакой роли, в принципе
#     userid = ID.chat.id


if __name__ == '__main__':
    bot.polling(none_stop=True)
