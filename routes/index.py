from . import *
from models.Post import Post
from models.Node import Node
from functools import wraps

main = Blueprint('index', __name__)

@main.route('/')
def index():
    node_name = request.args.get('node')
    selected_node = Node.query.get(1)
    node = Node.query.filter_by(name=node_name).first()
    if node is not None:
        selected_node = node
    post_list = selected_node.posts
    u = current_user()
    node_list = Node.query.all()
    data = {
        'post_list': post_list,
        'user': u,
        'node_list': node_list,
        'selected_node': selected_node
    }
    data_list.update(data)
    return render_template('index.html', **data_list)
