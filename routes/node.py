from . import *

from models.Node import Node

main = Blueprint('node', __name__)

@main.route('/')
@admin_required
def node_view():
    data = Node.user_list()
    return render_template('nodes.html', **data)


