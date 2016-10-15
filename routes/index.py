from . import *
from models.Post import Post
from models.Node import Node
from functools import wraps

main = Blueprint('index', __name__)

@main.route('/')
def index():
    post_list = Post.query.order_by(Post.created_time.desc()).all()
    u = current_user()
    node_list = Node.query.all()
    data = {
        'post_list': post_list,
        'user': u,
        'node_list': node_list,
        'select_all': True,
        'selected_node': None
    }
    data_list.update(data)
    return render_template('index.html', **data_list)

@main.route('/<string:node_name>')
def node_index(node_name):
    selected_node = Node.query.filter_by(name=node_name).first()
    if selected_node is None:
        return redirect(url_for('index.index'))
    post_list = selected_node.posts
    if len(post_list) != 0:
        post_list.reverse()
    u = current_user()
    node_list = Node.query.all()
    data = {
        'post_list': post_list,
        'user': u,
        'node_list': node_list,
        'select_all': False,
        'selected_node': selected_node
    }
    data_list.update(data)
    return render_template('index.html', **data_list)