import os

class Config(object):
    STAGE = 'heroku'
    SECRET_KEY = '1234'
    TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), 'templates')
    OUTPUT_PATH = os.path.join(os.path.dirname(__file__), 'output', 'latest-littlefield.csv')

    if STAGE == 'dev':
        CHROME_PATH = os.path.abspath(os.path.join(os.path.dirname(__name__), 'driver', 'chromedriver.exe'))
        CHROME_BIN = None
    if STAGE == 'heroku':
        CHROME_PATH = os.path.abspath(os.path.join(os.path.dirname(__name__), '.chromedriver', 'bin', 'chromedriver'))
        CHROME_BIN = os.path.abspath(os.path.join(os.path.dirname(__name__), '.apt', 'usr', 'bin', 'google-chrome'))
