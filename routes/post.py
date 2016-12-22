from . import *
from models.Post import Post
from models.Node import Node
from flask import current_app

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
    return render_template('add_post.html', **data)

@main.route('/<int:post_id>')
def view(post_id):
    u = current_user()
    p = Post.query.get(post_id)
    if p is None:
        abort(404)

    page = request.args.get('page', '1')
    if not page.isdigit():
        page = '1'
    page = int(page)
    pre_page = current_app.config.get('COMMENT_PRE_PAGE', 20)
    paginate = p.comments.paginate(page, pre_page, False)
    post_comments = paginate.items
    data = {
        'post': p,
        'user': u,
        'paginate': paginate,
        'post_comments': post_comments,
    }
    return render_template('post.html', **data)

@main.route('/edit/<int:post_id>')
@user_required
def edit(post_id):
    u = current_user()
    p = Post.query.get(post_id)
    if p is None:
        abort(404)

    valid = p.permission_valid(u)
    node_list = Node.query.filter_by(hidden=False)
    if valid:
        data = {
            'node_list': node_list,
            'post': p,
            'user': u
        }
        return render_template('edit_post.html', **data)
    else:
        abort(404)

@main.route('/delete/<int:post_id>')
@user_required
def delete(post_id):
    u = current_user()
    p = Post.query.get(post_id)
    if p is None:
        abort(404)

    valid = p.permission_valid(u)
    if valid:
        p.delete()
        return redirect(url_for('index.index'))
    else:
        abort(404)

