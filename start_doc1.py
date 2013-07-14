from docutils.core import publish_doctree

from pprint import pprint
import tempfile

doctree = publish_doctree(open('testfile.rst').read())

def collect_robot_nodes(node, collected=[]):
    robot_tagname = 'literal_block'
    robot_classes = ['code', 'robotframework']
    is_robot_node = (
        node.tagname == robot_tagname
        and node.attributes.get('classes') == robot_classes
    )
    if is_robot_node:
        collected.append(node)
        for node in node.children:
            collected = collect_robot_nodes(node, collected)
    else:
        for node in node.children:
            collected = collect_robot_nodes(node, collected)
    return collected

robot_nodes= collect_robot_nodes(doctree)



robot_data = "\n\n".join([node.rawsource for node in robot_nodes])
print robot_data

bfile = open('temp.robot','w')
bfile.write(robot_data)
bfile.close()


