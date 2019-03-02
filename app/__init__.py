from flask import Flask
from flask_bootstrap import Bootstrap
from config import Config


app = Flask(__name__)
app.config.from_object(Config)
app.template_folder = app.config['TEMPLATE_PATH']
bootstrap = Bootstrap(app)


from app import routes
