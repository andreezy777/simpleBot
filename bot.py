# v0.2
#
#

import config
import telebot
from SQLite3 import SQLighter

bot = telebot.TeleBot(config.token)


@bot.message_handler(content_types=["text"])
def repeat_all_messages(message):  # Название функции не играет никакой роли, в принципе
    name = message.from_user.first_name
    username = message.from_user.username
    bot.send_message(message.chat.id,
                     "{}({}) планирует прогулку в эту/это/этот: {}".format(name, username, message.text))
    db_worker = SQLighter(config.database)
    write_to_DB = db_worker.write_to(username, name, message.text)
    read_from_DB = db_worker.read_my_data(username)

    bot.send_message(message.chat.id,
<<<<<<< HEAD
                     "У вас запланированы прогулки на следующие дни: {}".format(''.join(str(x) for x in read_from_DB).
                                                                                replace('(', '').replace(')', '').
                                                                                replace('\'', ''))[:-1])
=======
                    "У вас запланированы прогулки на следующие дни: {}".format(''.join(str(x) for x in read_from_DB).replace('(','').replace(')','').replace('\'',''))[:-1])
>>>>>>> 16bd6bbf704668784be21ed24a230d1af0176c39
    db_worker.close()


# @bot.message_handler(commands=['getid'])
# def getuserid(ID):  # Название функции не играет никакой роли, в принципе
#     userid = ID.chat.id


if __name__ == '__main__':
    bot.polling(none_stop=True)
