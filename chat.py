from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, InlineQueryHandler
from telegram import InlineQueryResultArticle, InputTextMessageContent, MessageEntity
from config import Config
import logging
import random
import flickr
import datetime


def get_answers():
    file_answers = open("answers", "r")
    answers = []
    for line in file_answers.read().splitlines():
        answers.append(line)
    return answers


def get_hello():
    file_hello = open("hello", "r")
    hello = []
    for line in file_hello.read().splitlines():
        hello.append(line)
    return hello


def get_bye():
    file_bye = open("bye", "r")
    bye = []
    for line in file_bye.read().splitlines():
        bye.append(line)
    return bye


answers_list = get_answers()
hello_list = get_hello()
bye_list = get_bye()


def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Привет! Я чат бот :-)")


def echo(update, context):
    incoming_message = update.message.text.lower()
    print("Message {}", incoming_message)
    hello_list_lower = [each_string.lower() for each_string in hello_list]
    bye_list_lower = [each_string.lower() for each_string in bye_list]
    if incoming_message.replace("@mike_is_here_20210405_bot ", '') in hello_list_lower:
        context.bot.send_message(chat_id=update.effective_chat.id, text=random.choice(hello_list))
    elif incoming_message.replace("@mike_is_here_20210405_bot ", '') in bye_list_lower:
        context.bot.send_message(chat_id=update.effective_chat.id, text=random.choice(bye_list))
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text=random.choice(answers_list))


def pic(update, context):
    print('Get a pic command')
    random_picture = flickr.get_random()
    context.bot.send_photo(chat_id=update.effective_chat.id, photo=random_picture['link'],
                           caption=random_picture['title'])


def pic_from_sunny(update, context):
    print('Get a pic from Sunny command')
    timestamp = datetime.datetime.now().isoformat()
    context.bot.send_photo(chat_id=update.effective_chat.id,
                           photo="https://elasticbeanstalk-us-west-2-030334106137.s3-us-west-2.amazonaws.com/sunny/180_view_pic/image_small.jpg"+'?a='+timestamp,
                           caption="Hello from Sunny")


def big_pic_from_sunny(update, context):
    print('Get a pic from Sunny command')
    timestamp = datetime.datetime.now().isoformat()
    context.bot.send_photo(chat_id=update.effective_chat.id,
                           photo="https://elasticbeanstalk-us-west-2-030334106137.s3-us-west-2.amazonaws.com/sunny/180_view_pic/image.jpg"+'?a='+timestamp,
                           caption="Hello from Sunny")


def echo_inline(update, context):
    # incoming_message = update.message.text.lower()
    # print(incoming_message)
    query = update.inline_query.query
    if not query:
        return
    print("Query {}", query)
    hello_list_lower = [each_string.lower() for each_string in hello_list]
    bye_list_lower = [each_string.lower() for each_string in bye_list]
    results = list()
    results.append(
        InlineQueryResultArticle(
            id=query.upper(),
            title='Caps',
            input_message_content=InputTextMessageContent(query.upper())
        )
    )
    context.bot.answer_inline_query(update.inline_query.id, results)


if __name__ == "__main__":
    config = Config()
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    updater = Updater(token=config.config["apiKey"], use_context=True)
    dispatcher = updater.dispatcher
    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)
    picture_handler = CommandHandler('pic', pic)
    dispatcher.add_handler(picture_handler)
    picture_sunny_handler = CommandHandler('sunny_pic', pic_from_sunny)
    big_picture_sunny_handler = CommandHandler('big_sunny_pic', big_pic_from_sunny)
    dispatcher.add_handler(picture_sunny_handler)
    dispatcher.add_handler(big_picture_sunny_handler)
    echo_handler = MessageHandler((Filters.chat_type.private & Filters.text & (~Filters.command)) | (Filters.chat_type.groups & Filters.entity(MessageEntity.MENTION)), echo)
    dispatcher.add_handler(echo_handler)
    updater.start_polling()