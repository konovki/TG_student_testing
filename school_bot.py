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



@dp.message_handler(content_types=["text"])
async def process_start_command(message: types.Message):
    global df
    command = message['text'].split()
    if command[0] == 'task':
        if message.from_user.id in np.array(df['id']):
            answ = np.array(df[df['id'] == message.from_user.id]['answ'])
            if '--' in answ:
                await bot.send_message(message.from_user.id, 'Вы не решили задание')
            else:
                list = os.listdir('./school/')
                path = f'./school/{list[random.randrange(len(list))]}'
                await bot.send_photo(message.from_user.id,photo=open(path, 'rb'))
                df.loc[len(df)] = [message.from_user.id,'name',path,'--']
                df.to_csv(f'./{df_name}')
        else:
            list = os.listdir('./school/')
            path = f'./school/{list[random.randrange(len(list))]}'
            await bot.send_photo(message.from_user.id,photo=open(path, 'rb'))
            df.loc[len(df)] = [message.from_user.id,'name',path,'--']
            df.to_csv(f'./{df_name}')
    elif command[0] == 'a':
        index = df[df['id']==message.from_user.id].index[-1]
        df['answ'][index] = command[2]
        df['name'][index] = command[1]
        print(df)
        df.to_csv(f'./{df_name}')





if __name__ == '__main__':
    executor.start_polling(dp)
