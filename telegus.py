import requests
import os
from aiogram import Bot, executor, filters
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
import logging
import time
import sys
from settings.config import TG_settings as settings


API_TG_TOKEN = settings['token']

CHANNEL_ID = settings['channel_id']

bot_TG = Bot(token=API_TG_TOKEN)
dp_TG = Dispatcher(bot_TG, storage=MemoryStorage())
dp_TG.middleware.setup(LoggingMiddleware())

bot = Bot(token=API_TG_TOKEN, parse_mode=types.ParseMode.HTML)


def getus():
    post = open('post', 'r')
    post_list = str(post.read()).split('&:&')
    post.close()
    photos = post_list[-1].split(' ')
    return {'text': str(post_list[0]), 'photos': photos}


@dp_TG.message_handler(commands=['posts'], commands_prefix=settings['prefix'])
async def help(message: types.Message):
    media = []

    await message.answer('Мониторинг файла-трансфера..')
    a = 1
    print("tg_bot: Start of monitoring..")
    while a > 0:
        media = []
        post = getus()
        try:
            post['photos'].remove('')
        except:
            pass
        mem = open('tg_mem.txt', 'r')
        if str(post) != mem.read():
            if len(post['photos']) == 0:
                await bot.send_message(CHANNEL_ID, post['text'])
            elif len(post['photos']) > 0:
                media.append(types.InputMediaPhoto(post['photos'][0],
                                                   caption=str(post['text'])))
                for photo in post['photos']:
                    if photo != post['photos'][0]:
                        media.append(types.InputMediaPhoto(photo))
                if len(media) > len(post['photos']):
                    exit('tg_bot: Откуда-то взялась лишняя фотка. Ты и сам отлично знаешь, кому писать.')
                await bot.send_media_group(CHANNEL_ID, media=media)
            mem = open('tg_mem.txt', 'w')
            mem.write(str(post))
            mem.close()
        media = []
        delet_qw = open('delete_message', 'r')
        if 'True' in delet_qw.read():
            message_id = await bot.send_message(CHANNEL_ID, '.', disable_notification=True)
            message_id = message_id['message_id']
            await bot.delete_message(CHANNEL_ID, message_id)
            await bot.delete_message(CHANNEL_ID, message_id - 1)

            for x in 'tg_bot: Согласен, глупее их я ещё не видел.':
                print(x, end='')
                sys.stdout.flush()
                time.sleep(0.1)
            print()
            for x in 'tg_bot: А ведь оба совершеннолетние..':
                print(x, end='')
                sys.stdout.flush()
                time.sleep(0.1)
            print()
            for x in 'tg_bot: По крайней мере, по их меркам.':
                print(x, end='')
                sys.stdout.flush()
                time.sleep(0.1)
            print()
            for x in 'tg_bot: Я удалил соответствующее сообщение в подвластном мне канале связи.':
                print(x, end='')
                sys.stdout.flush()
                time.sleep(0.1)
            print()
            delet_qw.close()
            delet_qw = open('delete_message', 'w')
            delet_qw.write('')
            delet_qw.close()

        time.sleep(5)
        a += 1


if __name__ == "__main__":
    executor.start_polling(dp_TG, skip_updates=True)
