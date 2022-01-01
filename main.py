import subprocess
from vk_api import *
import requests
import os
import logging
import time
import hashlib
from settings.config import VK_settings as settings

link_to_group = settings['group']

vk_session = vk_api.VkApi(settings['num'], settings['pass'])
vk_session.auth()


def getus(count=2):
    rs = vk_session.method('wall.get',
        {
              'domain': link_to_group, "type": "text",
              'count': 1
        })

    if rs['items'][0]['is_pinned'] == 1:
        rs = vk_session.method('wall.get',
                               {
                                   'domain': link_to_group, "type": "text",
                                   'count': count
                               })
    return rs


def get_data_from_rs(count=2):
    locc = ''
    rs = getus(count)
    try:
        if len(rs['items'][-1]['attachments']) > 1:
            locc = rs['items'][-1]['text'] + ' &:&'
            for i in rs['items'][-1]['attachments']:
                locc += ' ' + i['photo']['sizes'][-1]['url']
        elif len(rs['items'][-1]['attachments']) == 1:
            locc = rs['items'][-1]['text'] + '&:&' + rs['items'][-1]['attachments'][-1]['photo']['sizes'][-1]['url']
    except KeyError:
        locc = rs['items'][-1]['text'] + '&:&'
    data = locc
    locc = ''

    return data, rs


vk = vk_session.get_api()

logging.basicConfig(level=logging.INFO)

three_last = []

a = 1

old_data = ''
data = ''

subprocess.Popen('python3 temp.py', shell=True)

subprocess.Popen('python3 telegus.py', shell=True)

while a > 0:
    data = get_data_from_rs()[0]
    rs = get_data_from_rs(2)[1]
    if data != old_data:
        try:
            if str(data) not in three_last:
                rs['items'].pop(0)
                buf = ''
                post = open('post', 'w')
                for i in rs['items']:
                    buf += str(i) + '\n'
                post.write(data)
                post.close()
                print('monit: ' + data)
                if len(three_last) < 3:
                    three_last.append(str(data))
                else:
                    three_last.pop(-1)
            else:
                print('monit: ' + 'Тупые человеки опять удалили пост')
                to_delete = open('delete_message', 'w')
                to_delete.write('True')
                to_delete.close()
                three_last.clear()
        except IndexError:
            rs['items'].pop(0)
            buf = ''
            post = open('post', 'w')
            for i in rs['items']:
                buf += str(i) + '\n'
            post.write('tg_bot: ' + data)
            post.close()
            print('monit: ' + data)

    time.sleep(45)
    old_data = data
