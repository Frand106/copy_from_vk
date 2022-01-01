from discord.ext import commands
import time
import pyshorteners

bot = commands.Bot(command_prefix=settings['prefix'])


def getus():
    post = open('post', 'r')
    post_list = str(post.read()).split('&:&')
    post.close()
    photos = post_list[-1].split(' ')
    return {'text': str(post_list[0]), 'photos': photos}


@bot.command()
async def hello(ctx):
    a = 1
    s = pyshorteners.Shortener()
    channel = bot.get_channel(919952311068016643)
    old_post = []
    print('hello')
    while a > 0:
        post = getus()
        pl = post['text'].split(' ')
        mem = open('ds_mem', 'r')
        if str(post) != mem:
            await channel.send(post['text'])
            print(post['photos'])
            old_post = str(post)
            mem = open('ds_mem', 'w')
            mem.write(str(old_post))
            mem.close()
            if len(post['photos']) > 1:
                post['photos'].pop(0)
            try:
                for i in post['photos']:
                    await channel.send(i)
                    print(i)
            except:
                pass
        post = {}
        time.sleep(5)


if __name__ == "__main__":
    bot.run(settings['token'])
