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


TOKEN = '820420748:AAGamzQWI3kcgg3ROav-tUCBEsBiNk20aew'
URI = 'postgres://peliixtyhsfiuv:092749581c3028c628fbe0b346f2ae624d877dc694c30e2a2e8befb7964c832b@ec2-184-72-237-95.compute-1.amazonaws.com:5432/ddgjcqg98is45a'
