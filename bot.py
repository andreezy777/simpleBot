# v0.1
#
#

import config
import telebot

bot = telebot.TeleBot(config.token)


@bot.message_handler(content_types=["text"])
def repeat_all_messages(message):  # Название функции не играет никакой роли, в принципе
    bot.send_message(message.chat.id, "Саша любит Андрея")


if __name__ == '__main__':
    bot.polling(none_stop=True)
