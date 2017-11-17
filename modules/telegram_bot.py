from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import configparser
from modules.sqlite_client import SqlLiteDb
from modules.giphy_api import GiphyApi
from modules.coub_api import CoubApi
import datetime


class TelegramBot:

    def __init__(self):
        self.now = datetime.datetime.now()
        self.config = configparser.ConfigParser()
        self.config.read("config.ini")
        self.db = SqlLiteDb()
        self.giphy_keywords = self.db.get_giphy_keywords()
        self.giphy = GiphyApi(self.config['API']['GiphyKey'])
        self.coub = CoubApi()

        self.updater = Updater(self.config['API']['TelegramKey'])

        self.updater.job_queue.run_repeating(self.coub_weekly, interval=datetime.timedelta(days=1),
                                             first=datetime.time(8, 00, 00))
        self.updater.dispatcher.add_handler(CommandHandler('start', self.start))
        self.updater.dispatcher.add_handler(CommandHandler('coub', self.random_coub))
        self.updater.dispatcher.add_handler(CommandHandler('ismintis', self.quotes))
        self.updater.dispatcher.add_handler(CommandHandler('prasiblaivek', self.reload))
        self.echo_handler = MessageHandler(Filters.text, self.echo)
        self.updater.dispatcher.add_handler(self.echo_handler)

        self.updater.start_polling()
        self.updater.idle()

    def coub_weekly(self, bot, job):
        if self.now.weekday() == 4:
            year = self.now.year
            week = datetime.date(self.now.year, self.now.month, self.now.day).isocalendar()[1]
            bot.send_message(chat_id=self.config['CHAT']['ChatId'], text='Nepamirstam paziureti http://coub.com/weekly/'
                                                                         + str(year) + '/' + str(week - 1))

    def start(self, bot, update):
        update.message.reply_text('Sveiki, ponai!')

    def random_coub(self, bot, update):
        coub_link = self.coub.get_random_coub()
        if coub_link != '':
            bot.send_message(chat_id=update.message.chat_id, text=coub_link)

    def quotes(self, bot, update):
        update.message.reply_text(SqlLiteDb().get_random_quote()[0]['quote'])

    def reload(self, bot, update):
        update.message.reply_text('Taip, pone')
        self.giphy_keywords = self.db.get_giphy_keywords()

    def echo(self, bot, update):
        if 'Sveikas, Marshalas'.upper() in update.message.text.upper():
            bot.send_message(chat_id=update.message.chat_id, text='Sveiki, ponai!')

        # Coub handling
        if 'Duok vaizdo'.upper() in update.message.text.upper():
            coub_link = self.coub.get_random_coub()
            if coub_link != '':
                bot.send_message(chat_id=update.message.chat_id, text=coub_link)

        # Giphy handling
        search = [item for item in self.giphy_keywords if item['keyword'].upper() in update.message.text.upper()]
        if len(search) != 0:
            url = self.giphy.get_random_gif(search[0]['search_term'])
            if url != '':
                bot.send_message(chat_id=update.message.chat_id, text=url)
