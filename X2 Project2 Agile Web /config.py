import os

class Config(object):

    SECRET_KEY = os.environ.get('SERCRET_KEY') or "123-key"