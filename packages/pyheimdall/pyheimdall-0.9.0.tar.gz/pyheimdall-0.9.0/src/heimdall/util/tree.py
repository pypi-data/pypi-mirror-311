# -*- coding: utf-8 -*-

"""
Provides utility functions around HERA elements tree refactoring or cleanup.

:copyright: The pyHeimdall contributors.
:licence: Afero GPL, see LICENSE for more details.
:SPDX-License-Identifier: AGPL-3.0-or-later
"""
from lxml import etree as _et


def get_nodes(tree, tag, filter=None):
    nodes = tree.findall(f'.//{tag}')
    if filter:
        return [node for node in nodes if filter(node)]
    return nodes


def get_node(tree, tag, filter=None):
    nodes = get_nodes(tree, tag, filter)
    if len(nodes) == 0:
        return None
    if len(nodes) == 1:
        return nodes[0]
    raise IndexError(f"Too many {tag} elements ({len(nodes)})")


def get_root(tree):
    return tree.xpath('//hera')[0]


def get_language(node):
    qname = _et.QName('http://www.w3.org/XML/1998/namespace', 'lang')
    return node.get(qname)


def set_language(node, language):
    qname = _et.QName('http://www.w3.org/XML/1998/namespace', 'lang')
    return node.set(qname, language)


def create_nodes(parent, tag, text):
    nodes = list()
    if type(text) is str:
        node = create_node(parent, tag, text)
        nodes.append(node)
    else:
        for language_key, value in text.items():
            node = create_node(parent, tag, value)
            set_language(node, language_key)
            nodes.append(node)
    return nodes


def create_node(parent, tag, text=None):
    node = _et.SubElement(parent, tag)
    if text is not None:
        node.text = text
    return node


def update_node_value(node, key, value):
    if value is not None:
        node.set(key, str(value))
    else:  # remove value
        node.attrib.pop(key)


def maybe_update_node_values(node, keys, **kwargs):
    for key in keys:
        try:
            value = kwargs[key]
            update_node_value(node, key, value)
        except KeyError:
            pass  # nothing to change


def update_node_children(node, key, value):
    children = get_nodes(node, key)
    for child in children:
        if value is not None:
            child.text = str(value)
        else:  # remove child node
            child.getparent().remove(child)


def maybe_update_node_children(node, keys, **kwargs):
    for key in keys:
        try:
            value = kwargs[key]
            update_node_children(node, key, value)
        except KeyError:
            pass  # nothing to change


__copyright__ = "Copyright the pyHeimdall contributors."
__license__ = 'AGPL-3.0-or-later'
