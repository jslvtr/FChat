from flask import Flask, render_template
from src.common.database import Database

UPLOAD_FOLDER = '/static/uploads'
app = Flask(__name__)
app.config.from_object('src.config')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = '123'

@app.before_first_request
def init_db():
    Database.initialise()


@app.route('/')
def home():
    return render_template('home.html')


from src.models.users.views import user_blueprint
app.register_blueprint(user_blueprint, url_prefix='/users')
from src.models.seeds.views import seed_blueprint
app.register_blueprint(seed_blueprint, url_prefix='/seeds')