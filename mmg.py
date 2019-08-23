import os
from flask import Flask
from flask_admin import Admin
from flask_cors import CORS
from flask_login import LoginManager

from models.db import db
from models.install import install_models
from routes.install import install_routes
from utils.config import IS_DEV

app = Flask(__name__, static_url_path='/static')
login_manager = LoginManager()
admin = Admin(name='MMG Admin',
              url='/mmg/manager',
              template_mode='bootstrap3')

app.secret_key = os.environ.get('FLASK_SECRET', 'HZ#1updrH9x6Vs!oQp0tC0!Q')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_POOL_SIZE'] = int(os.environ.get('DATABASE_POOL_SIZE', 20))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SESSION_COOKIE_SECURE'] = False if IS_DEV else True
app.config['REMEMBER_COOKIE_DURATION'] = 90 * 24 * 3600
app.config['PERMANENT_SESSION_LIFETIME'] = 90 * 24 * 3600
app.config['REMEMBER_COOKIE_HTTPONLY'] = True
app.config['FLASK_ADMIN_FLUID_LAYOUT'] = True

admin.init_app(app)
db.init_app(app)
login_manager.init_app(app)


@app.teardown_request
def remove_db_session(exc):
    try:
        db.session.remove()
    except AttributeError:
        pass


cors = CORS(app,
            resources={r"/*": {"origins": "*"}},
            supports_credentials=True
            )

app.url_map.strict_slashes = False

with app.app_context():
    if IS_DEV:
        install_models()
    install_routes()

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=IS_DEV, use_reloader=True)
