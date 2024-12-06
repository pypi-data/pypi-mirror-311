# -*- coding: utf-8 -*-

"""
Provides utility functions around HERA entities refactoring or cleanup.

:copyright: The pyHeimdall contributors.
:licence: Afero GPL, see LICENSE for more details.
:SPDX-License-Identifier: AGPL-3.0-or-later
"""
import heimdall
from heimdall.util import get_node, create_node
from lxml import etree as _et


ENTITIES = 'entities'
ATTRIBUTES = 'attributes'
PROPERTIES = 'properties'
INT_MAX_VALUE = 999999  # should theorically be `sys.maxsize * 2 + 1` but heck


def update_entities(tree, delete_orphans=False):
    """
    If ``delete_orphans`` is ``True``, metadata with neither ``aid`` nor
    ``pid`` will be deleted from their containing item, as they cannot be
    linked to any entity or property. If ``False``, these metadata will be
    left untouched.
    """
    data = dict()
    data[ENTITIES] = dict()
    data[PROPERTIES] = dict()
    all_entities = set()
    ALL_ATTRIBUTES = 'all'
    for item in heimdall.getItems(tree):
        eid = item.get('eid')
        if eid is None:
            continue  # we can't do anything if item has no entity
        entity = _get_entity(tree, data, eid)
        metas = dict()  # {aid <> counter} of already encountered metadata
        for metadata in heimdall.getMetadata(item):
            # (1) retrieve attribute and property for metadata
            aid = metadata.get('aid', None)
            attribute = _get_attribute(entity, aid)
            pid = metadata.get('pid', None)
            if attribute is not None:
                if pid is None:
                    pid = attribute.get('pid', None)
                else:  # pid is not None
                    _set_attribute_pid(attribute, pid)
            else:
                # try to deduce attribute from just eid+pid
                attribute = _get_attribute_by_pid(entity, pid)
                aid = attribute['id']
            property_ = _get_property(tree, data, pid, aid)
            if property_ is not None:
                _set_attribute_pid(attribute, property_['id'])
            else:  # pid AND aid should be null here, so metadata is orphan
                if delete_orphans:
                    metadata.getparent().remove(metadata)
                    continue  # rest of the loop is moot for orphan

            assert attribute is not None
            assert property_ is not None
            # (2) infer attribute type
            value = metadata.text
            type_ = attribute.get('type', None)
            if type_ != 'text':
                attribute['type'] = _infer_type(value)
            # (2a) infer attribute length
            # TODO: kinda useful for SQL, but not really used yet
            attribute['length'] = max(attribute.get('length', 0), len(value))
            # (3) count metadata in this item to infer min and max later
            all_attributes = entity.get(ALL_ATTRIBUTES, set())
            if eid in all_entities:
                if aid not in all_attributes:
                    # there was already an item for this entity, and this item
                    # did not have this metadata ; thus metadata is optional
                    attribute['min'] = 0
            # track that we saw this attribute, and how much times
            all_attributes.add(aid)
            entity[ALL_ATTRIBUTES] = all_attributes
            count = metas.get(aid, 0)
            count += 1
            metas[aid] = count
            # NOTE: name, description or uri cannot be infered from metadata

        # track we already saw this entity (this was the first item with it)
        all_entities.add(eid)
        # (4) update attributes min and max
        for aid, count in metas.items():
            attribute = [a for a in entity[ATTRIBUTES] if a['id'] == aid][0]
            amin = int(attribute.get('min', INT_MAX_VALUE))
            amax = int(attribute.get('max', 0))
            attribute['min'] = min(amin, count)
            attribute['max'] = max(amax, count)
    # cleanup
    for entity in data[ENTITIES].values():
        del entity[ALL_ATTRIBUTES]

    # TODO (5) infer properties types form all attributes that use it

    # (6) create/update tree nodes from infered data
    update_tree(tree, data)
    return tree


def _infer_type(value):
    try:
        float(value)
        return 'number'
    except ValueError:
        pass  # not a number
    try:
        from dateutil.parser import parse
        parse(value)
        return 'datetime'
    except ModuleNotFoundError:
        pass  # dateutils missing, we can't say if it's a date
    except:  # nopep8: E722
        # I'm not explicit on error catched because dateutil.parser.parse
        # raises custom Errors that I may be unable to import
        pass  # not a date
    return 'text'


def _get_entity(tree, data, eid):
    """Retrieves the current state of an entity as an plain object.
    """
    entity = data[ENTITIES].get(eid, None)
    if entity is not None:
        return entity
    node = heimdall.getEntity(tree, lambda n: n.get('id') == eid)
    if node is not None:
        from heimdall.connectors.json import _entity2object
        data[ENTITIES][eid] = _entity2object(node)
    else:
        data[ENTITIES][eid] = {'id': eid, }
    return data[ENTITIES][eid]


def _get_attribute(entity, aid):
    if aid is None:
        return None
    attributes = entity.get(ATTRIBUTES, list())
    attribute = [a for a in attributes if a['id'] == aid]
    assert len(attribute) < 2
    if len(attribute) > 0:
        attribute = attribute[0]
    else:
        attribute = {'id': aid, }
        attributes.append(attribute)
        entity[ATTRIBUTES] = attributes
    return attribute


def _get_attribute_by_pid(entity, pid):
    if pid is None:
        return None
    attributes = entity.get(ATTRIBUTES, list())
    attribute = [a for a in attributes if a['pid'] == pid]
    assert len(attribute) < 2
    if len(attribute) > 0:
        attribute = attribute[0]
        if 'id' not in attribute:
            attribute['id'] = pid
    else:
        attribute = {'id': pid, 'pid': pid, }
        attributes.append(attribute)
        entity[ATTRIBUTES] = attributes
    return attribute


def _set_attribute_pid(attribute, pid):
    try:
        assert pid == attribute['pid']
    except KeyError:
        attribute['pid'] = pid


def _get_property(tree, data, pid, aid=None):
    if pid is None:
        if aid is not None:
            pid = aid
        else:
            return None
    property_ = data[PROPERTIES].get(pid, None)
    if property_ is not None:
        return property_
    node = heimdall.getProperty(tree, lambda n: n.get('id') == pid)
    if node is not None:
        from heimdall.connectors.json import _property2object
        data[PROPERTIES][pid] = _property2object(node)
    else:
        data[PROPERTIES][pid] = {'id': pid, }
    return data[PROPERTIES][pid]


def update_tree(tree, data):
    """Update HERA element tree with new data
    """
    for pid, payload in data[PROPERTIES].items():
        property_ = heimdall.getProperty(tree, lambda n: n.get('id') == pid)
        if property_ is None:
            _get_container(tree, 'properties')  # creates if missing
            heimdall.createProperty(tree, **payload)
        else:
            heimdall.updateProperty(property_, **payload)

    for eid, payload in data[ENTITIES].items():
        entity = heimdall.getEntity(tree, lambda n: n.get('id') == eid)
        if entity is None:
            _get_container(tree, 'entities')  # creates if missing
            entity = heimdall.createEntity(tree, **payload)
        else:
            heimdall.updateEntity(entity, **payload)
        for a in payload[ATTRIBUTES]:
            aid = a['id']
            attr = heimdall.getAttribute(entity, lambda n: n.get('id') == aid)
            if attr is None:
                attr = heimdall.createAttribute(entity, **a)
            else:
                heimdall.updateAttribute(attr, **a)
            try:
                length = a['length']
                prefix = heimdall.connectors.mysql.LENGTH_PREFIX
                create_node(attr, 'rule', f'{prefix}{str(length)}')
            except KeyError:
                pass  # no length


def _get_container(tree, tag):
    container = get_node(tree, tag)
    if container is None:
        container = _et.SubElement(tree, tag)
    return container
