import logging
from telegram.ext import Updater
from telegram.ext import CommandHandler #copy\ start
from telegram.ext import MessageHandler
from telegram.ext import Filters
import requests
import json
import random



class WeatherApi:
    def __init__(self, token):
        self.token = token
        
    def data_for(self, *args):
        query = ','.join(args)
        url = f"http://api.openweathermap.org/data/2.5/weather?q={query}&appid={self.token}&units=metric"
        data = requests.get(url)
        return data.json()
    

class Bot:
    def __init__(self, token):
        self.enable_logging()
        self.updater = Updater(token=token, use_context = True)
        self.dispatcher = self.updater.dispatcher
        self.weather_api = WeatherApi('96d3a61a7040975572116ff4f0555b69')
        self.add_handlers() #обработчик создаваемых событий
    
    def enable_logging(self):
        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
        
    def add_handlers(self):
        start = CommandHandler('start', self.start) #start
        self.dispatcher.add_handler(start)
        
        message = MessageHandler(Filters.text & (~Filters.command), self.msg)
        self.dispatcher.add_handler(message)
        
        weather = CommandHandler('weather', self.show_weather)
        self.dispatcher.add_handler(weather)
        
        suggest = CommandHandler('suggest_clothes', self.suggest)
        self.dispatcher.add_handler(suggest)
        
        unknown = MessageHandler(Filters.command, self.unknown)
        self.dispatcher.add_handler(unknown)
        
    def start(self, update, context):
        context.bot.send_message(chat_id = update.effective_chat.id, text='Hi! I am feelslikebot! I am here to inform you about weather!')
     
    def get_temp(self, temp):
        temp = float(temp)
        if temp > 5.0 and temp < 15.0:
            return 'cool'
        elif temp < 5.0:
            return 'cold'
        elif temp > 15.0  and temp < 25.0:
            return 'warm'
        else:
            return 'heat'
        
     
    def suggest(self, context, update, weather, temp):
        weather = weather.lower()
        temp_range = self.get_temp(temp)
        with open('dump_json_clothes.txt', 'r') as dump:
            suggestions = json.load(dump)
            if weather in suggestions:
                random_number = random.randint(0, len(suggestions[weather][temp_range]['top'])-1)
                top = f"This would be perfect for top: {suggestions[weather][temp_range]['top'][random_number]}\n"
                down = f"And this for down: {suggestions[weather][temp_range]['down'][random_number]}"
                context.bot.send_message(chat_id = update.effective_chat.id, text= top + down )
            else:
                sorry = 'Sorry, didn`t find something suitable for you!'
                context.bot.send_message(chat_id = update.effective_chat.id, text= sorry )
    
    def show_weather(self, update, context):
        data = self.weather_api.data_for(*context.args)
        weather = data['weather'][0]['main']
        temp = data['main']['temp']
        weather_data = f"I guess it is:\n{data['weather'][0]['description'].capitalize()}\n"
        temp_data = f"And temperature is {data['main']['temp']} C. Feels like {data['main']['feels_like']} C.\n"
        wind = f"Wind is about {data['wind']['speed']} m/s."
        context.bot.send_message(chat_id = update.effective_chat.id, text= weather_data + temp_data + wind)
        self.suggest(context,update, weather, temp)
    
    def msg(self, update, context):
        with open('dictionary.txt') as di:
            data = json.load(di)
            if update.message.text.lower() in data:
                text = data[update.message.text.lower()]
            else: 
                text = 'I didn`t get it!'
        context.bot.send_message(chat_id = update.effective_chat.id, text=text)
     
    def unknown(self, update, context):
        context.bot.send_message(chat_id = update.effective_chat.id, text='I dont speak that language')
        
     
    def work(self):
        self.updater.start_polling() #начать запрашивать обновления из телеграма
        print('Bot is ready for work!')
        self.updater.idle()
        
Bot = Bot('1429562086:AAHQdGeYPF-NKFT-XecDoPskFeKdf69jD_Q')
Bot.work()