from . import *
from models.Post import Post
from models.Node import Node
from flask import current_app
from controllor import post

main = Blueprint('index', __name__)

@main.route('/')
def index():
    data = post.page('1')
    return render_template('index.html', **data)

@main.route('/<string:node_name>')
def node_index(node_name):
    page = request.args.get('page', '1')
    data = post.page(page, node_name)
    return render_template('index.html', **data)
