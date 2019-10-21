import os

HELLO_MESSAGE = """
Привет, {}. Давай расскажу как пользоваться моими способностями, все очень просто: \n
1. Ты кидаешь мне гео-локацию места, рядом с которым тебе нужно что-то напомнить\n
2. Пишешь то, что тебе напомнить \n
2. Делишься гео-локацией в режиме реального времени, чтобы я понимал где ты идешь.
"""


def get_env_param(name):
    try:
        val = os.environ[name]
    except KeyError:
        raise Exception('Not set param {} in the environment'.format(name))
    return val


TOKEN = get_env_param('TOKEN')
URI = get_env_param('URI')
