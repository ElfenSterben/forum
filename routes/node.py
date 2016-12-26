from . import *

from models.Node import Node

main = Blueprint('node', __name__)

@main.route('/')
@admin_required
def node_view():
    node_list = Node.query.order_by(Node.id.desc()).all()
    data = {
        'node_list': node_list,
    }
    return render_template('nodes.html', **data)


