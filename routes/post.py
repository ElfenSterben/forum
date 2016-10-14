from . import *
from models.Post import Post
from models.Node import Node


main = Blueprint('post', __name__)

@main.route('/new')
@user_required
def new():
    u = current_user()
    node_list = Node.query.filter_by(hidden=False)
    data = {
        'user': u,
        'node_list': node_list
    }
    data_list.update(data)
    return render_template('add_post.html', **data_list)

@main.route('/<int:post_id>')
def view(post_id):
    u = current_user()
    p = Post.query.get(post_id)
    if p is None:
        abort(404)
    data = {
        'post': p,
        'user': u
    }
    data_list.update(data)
    return render_template('post.html', **data_list)
