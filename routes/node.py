from . import *

from models.Node import Node


main = Blueprint('node', __name__)

@main.route('/')
@admin_required
def node_view():
    node_list = Node.query.order_by(Node.id.desc()).all()
    u=current_user()
    data = {
        'node_list': node_list,
        'user': u
    }
    data_list.update(data)
    return render_template('nodes.html', **data_list)


