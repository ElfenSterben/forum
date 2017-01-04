from flask import Flask, g, session
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from models import db, timestamp
from models.User import User
from routes.api import  main as routes_api
from routes.index import main as routes_index
from routes.login import main as routes_login
from routes.logout import main as routes_logout
from routes.node import main as routes_node
from routes.post import main as routes_post
from routes.user import main as routes_user
from utils.plugin import *

app = Flask(__name__)
manager = Manager(app)
hostname = 'kaede'

@app.before_request
def current_user():
    u_id = session.get('user_id')
    if u_id is not None:
        user =  User.query.get(u_id)
    else:
        user = None
    g.user = user

@app.context_processor
def create_base_data():
    data = {
        'user': g.user,
        'hostname': hostname,
        'current_time': timestamp(),
    }
    return data

def register_routes(app):
    app.register_blueprint(routes_index)
    app.register_blueprint(routes_post, url_prefix='/post')
    app.register_blueprint(routes_node, url_prefix='/node')
    app.register_blueprint(routes_api, url_prefix='/api')
    app.register_blueprint(routes_login, url_prefix='/login')
    app.register_blueprint(routes_logout, url_prefix='/logout')
    app.register_blueprint(routes_user, url_prefix='/user')

def configure_app():
    app.config.from_object('config')
    db.init_app(app)
    csrf.init_app(app)
    register_routes(app)
    configure_uploads(app, (avatar,))
    patch_request_class(app, 2 * 1024 * 1024) # 最大2Mb


def configured_app():
    configure_app()
    return app

# 自定义的命令行命令用来运行服务器
@manager.command
def server():
    print('server run')
    app = configured_app()
    config = dict(
        debug = True,
        host = 'localhost',
        port = 3000,
    )
    app.run(**config)


def configure_manager():
    """
    这个函数用来配置命令行选项
    """
    Migrate(app, db)
    manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    configure_manager()
    configure_app()
    manager.run()
