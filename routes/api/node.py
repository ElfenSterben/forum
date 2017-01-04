from models.Node import Node
from . import *


@main.route('/node/add', methods=['post'])
@admin_required
def node_add():
    r = {}
    n_json = request.get_json()
    n = Node.query.filter_by(name=n_json.get('name')).first()
    if n is not None:
        r['success'] = False
        r['message'] = "节点已存在"
    else:
        node = Node(n_json)
        node.save()
        r['success'] = True
        r['data'] = node.json()
    return jsonify(r)

@main.route('/node/delete', methods=['post'])
@admin_required
def node_delete():
    r = {}
    json = request.get_json()
    nid = json.get('id')
    node = Node.query.get(nid)
    if node is None:
        r['success'] = False
        r['message'] = 'node不存在'
    else:
        node.delete()
        r['success'] = True
    return jsonify(r)