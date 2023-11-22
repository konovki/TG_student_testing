import asyncio,os,numpy,pandas,random
import telebot
import numpy as np
import pandas as pd
from datetime import datetime as dt
from aiogram import Bot, types, Dispatcher
from aiogram.utils import executor
from config import Telegram_token,My_tg
import config
global trade_df
pd.options.mode.chained_assignment = None
bot = Bot(token=Telegram_token)
bot_usual = telebot.TeleBot(Telegram_token, parse_mode=None)
dp = Dispatcher(bot)
df_name = f'df_{str(dt.now()).replace(":","_").replace(".","_").replace("-","_").replace(" ","_")}'+'.csv'

global df
df = pd.DataFrame(columns=['id','name','task','answ'])
df = df.astype({'id': int,'name':str,'answ':str})
def send_usual_message(event,console = True,telegram = True):
    def simple_message(event):
        bot_usual.send_message(My_tg,event)
        print(event)
    def list_message(event_list):
        for ev in event_list:
            simple_message(ev)
    def str_concat(data):
        s = ''
        for s0 in data:
            s+= s0
        print(s)
        bot_usual.send_message(My_tg,s)
    print(type(event))
    if isinstance(event,str):
        simple_message(event)
    elif isinstance(event,list) or isinstance(event,numpy.ndarray):
        list_message(event)
    elif isinstance(event,pd.DataFrame):
        str_concat(event.to_csv())
        print(event)
def add_figi(message):
    global trade_df
    print(message)
    list_row =[message[1], message[2],message[3],message[4],message[5],message[6]]

    send_usual_message(trade_df)
def del_figi(message):
    global trade_df
    trade_df = trade_df.drop(trade_df.index[int(message[1])]).reset_index(drop=True)
    print(trade_df)
    send_usual_message(trade_df)
def create_test_df():
    return pd.DataFrame(data={'name':['Sber','MTS'],'figi':['1','2'],'priceIn':[100,200],'priceOut':[120,220],
                              'N':[1,2],'status':['by','by']})

class Inicilize():
    def __init__(self):
        # asyncio.run(b_mes('make it!'))
        print('hello')
        trade_list_path = config.trade_list_path
        if os.path.exists(trade_list_path):
            self.trade_df = pd.read_csv(trade_list_path)
        else:
            self.trade_df = pd.DataFrame(columns=['name','figi','priceIn','priceOut','N','status'])
            print(self.trade_df)
            send_usual_message(self.trade_df)

class Analitics():
    pass

class Trade():

    pass

@dp.message_handler(commands="task")
async def cmd_random(message: types.Message):
    await bot.send_message('yep')
    await message.answer("Нажмите на кнопку, чтобы бот отправил число от 1 до 10")
@dp.message_handler(content_types=["text"])
async def process_start_command(message: types.Message):
    global df
    command = message['text'].split()
    if command[0] == 'add':
        add_figi(command)
    elif command[0] == 'del':
        del_figi(command)
    elif command[0] == 'task':
        if message.from_user.id in np.array(df['id']):
            print('here')
            answ = np.array(df[df['id'] == message.from_user.id]['answ'])
            if '--' in answ:
                print('here1')
                await bot.send_message(message.from_user.id, 'Вы не решили задание')
            else:
                print('here2')
                list = os.listdir('./school/')
                # path = '   '
                # while path[-3:] != 'png':
                path = f'./school/{list[random.randrange(len(list))]}'
                print(path)
                print('here')
                await bot.send_photo(message.from_user.id,photo=open(path, 'rb'))
                df.loc[len(df)] = [message.from_user.id,'name',path,'--']
                df.to_csv(f'./{df_name}')
        else:
            list = os.listdir('./school/')
            path = f'./school/{list[random.randrange(len(list))]}'
            await bot.send_photo(message.from_user.id,photo=open(path, 'rb'))
            df.loc[len(df)] = [message.from_user.id,'name',path,'--']
            df.to_csv(f'./{df_name}')
            # print(df)# await bot.send_message(message.from_user.id, path)
    elif command[0] == 'a':
        index = df[df['id']==message.from_user.id].index[-1]
        df['answ'][index] = command[2]
        df['name'][index] = command[1]
        print(df)
        #Девчонке задание пришло два раза и получился затуп
        #Надо прописать ограничение на добавление строки в df
        #Если такая строка уже есть, то не добавлять

@dp.message_handler(content_types=["text"])
async def process_start_command(message: types.Message):
    command = message['text'].split()
    if command[0] == 'add':
        add_figi(command)
    elif command[0] == 'del':
        del_figi(command)




if __name__ == '__main__':
    # loop = asyncio.get_event_loop()
    # loop.create_task(main())
    executor.start_polling(dp)
