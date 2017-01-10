from . import *
from models.Post import Post
from models.Node import Node
from flask import current_app

main = Blueprint('index', __name__)

@main.route('/')
def index():
    data = get_page_data(Post)
    return render_template('index.html', **data)

@main.route('/<string:node_name>')
def node_index(node_name):
    selected_node = Node.query.filter_by(name=node_name).first()
    if selected_node is None:
        return redirect(url_for('index.index'))

    data = get_page_data(Post, selected_node)
    return render_template('index.html', **data)

def get_page_data(Model, node=None):
    page = request.args.get('page', '1')
    if not page.isdigit():
        page = '1'
    page = int(page)
    pre_page = current_app.config.get('COMMENT_PRE_PAGE', 20)
    if node == None:
        query = Model.query
    else:
        query = node.posts

    paginate = query.order_by(Model.created_time.desc()).paginate(page, pre_page, False)
    post_list = paginate.items
    node_list = Node.query.all()
    data = {
        'post_list': post_list,
        'paginate': paginate,
        'node_list': node_list,
        'selected_node': node,
    }
    return data