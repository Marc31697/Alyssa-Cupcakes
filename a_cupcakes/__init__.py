from flask import Flask
from config import Config
from .site.routes import site
from .authentication.routes import auth
from .api.routes import api
from .admin.routes import admin
from flask_migrate import Migrate
from a_cupcakes.helpers import JSONEncoder
from flask_cors import CORS
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from .models import db as root_db, login_manager, ma


app = Flask(__name__)
bootstrap = Bootstrap(app)

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'noreplycupcakes@gmail.com'
app.config['MAIL_PASSWORD'] = '022420cup'
mail=Mail(app)

app.register_blueprint(site)
app.register_blueprint(auth)
app.register_blueprint(api)
app.register_blueprint(admin)

app.config.from_object(Config)

root_db.init_app(app)

migrate = Migrate(app,root_db)

login_manager.init_app(app)
login_manager.login_view = 'signin'

ma.init_app(app)

app.json_encoder = JSONEncoder
CORS(app)