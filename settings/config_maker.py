import pathlib

path = input('path to copy_from_vk dir: ')

prefix = input('prefix for bots: ')

DS_token = input('DS_token: ')
DS_name = input('DS_bot_name: ')
DS_channel = input("DS channel to send posts: ")

TG_token = input('TG_token: ')
TG_channel_id = input('TG channel to send posts: ')

VK_num = input('VK_phone_number: ')
VK_pass = input('VK_password: ')
VK_group_id = input('VK_group_id: ')

with open(path + '/settings/config.py', 'w') as config:
    config.write("DS_settings = {    'token':" + DS_token + ",    'bot': " + DS_name + ",    'id': "  + DS_channel + " ,    'prefix': " + prefix + "} "
                "\n TG_settings = {    'token': " + TG_token + "    'channel_id': " + TG_channel_id + ",    'prefix': " + prefix + "}"
                "\nVK_settings = {    'num': " + VK_num + "    'pass': " + VK_pass + ", 'group: '" + VK_group_id + " '}")
