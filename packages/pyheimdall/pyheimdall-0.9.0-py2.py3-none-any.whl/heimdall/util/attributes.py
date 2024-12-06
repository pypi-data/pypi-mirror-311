# -*- coding: utf-8 -*-

"""
Provides utility functions around HERA attributes.

:copyright: The pyHeimdall contributors.
:licence: Afero GPL, see LICENSE for more details.
:SPDX-License-Identifier: AGPL-3.0-or-later
"""
import heimdall
from . import get_node as _get_node, set_language as _set_language
from lxml import etree


'''
class Relationship:
    def __init__(self, eid, source, target):
        self.eid = eid  # a Relationship is an Entity, it's its id
        self.source = source  # source attribute pid
        self.target = target  # target attribute pid
'''


def refactor_relationship(tree, relationship, eid, euid, pid, cleanup=True):
    """TODO
    """
    R_ID = relationship['eid']
    R_SOURCE = relationship['source']
    R_TARGET = relationship['target']
    # TODO only create property if not exists
    p = heimdall.createProperty(tree, id=pid)
    e = heimdall.getEntity(tree, lambda n: n.get('id') == eid)
    # TODO only create attribute if not exists
    a = heimdall.createAttribute(e, pid=pid)
    # iterate over all items belonging to the relationship entity
    items = heimdall.getItems(tree, lambda n: n.get('eid') == R_ID)
    for old in items:
        source = heimdall.getMetadata(old, R_SOURCE)[0].text
        target = heimdall.getMetadata(old, R_TARGET)[0].text

        def is_source(item):
            is_of_entity = item.get('eid') == eid
            has_unique_id = False
            # Unique id shouldn't be a repeatable attribute,
            # but we know what real world looks like. Thus,
            # try to not break in this edge case, and let's
            # hope our caller knows what she does.
            for v in heimdall.getValues(item, euid):
                has_unique_id = has_unique_id or (v == source)
            return is_of_entity and has_unique_id

        # get the item which must contain the new repeatable metadata
        now = heimdall.getItem(tree, is_source)
        etree.SubElement(now, 'metadata', pid=pid).text = target
        if cleanup:
            # delete `old` relationship item, because it is
            # now represented by new metadata in item `now`
            old.getparent().remove(old)
    if cleanup:
        # delete the `relationship` entity, as there are no more items using it
        heimdall.deleteEntity(tree, lambda n: n.get('id') == R_ID)


def merge_l10n_attributes(
        tree, eid, languages,
        pid=None, aid=None,
        cleanup=True, update_items=True
        ):
    """Merge attributes that are in fact translations of one another.

    :param tree: HERA elements tree
    :param eid: Identifier of the HERA entity in ``tree``
            containing all attributes to merge
    :param languages: dict containing attribute ids (aid) as keys
            and language codes as values
            it's not the other way around in case you have more than one
            attribute for the same language
    :param pid: HERA attribute pid of merged attribute
    :param aid: (optional, default ``{pid}_attr``): HERA attribute id
            (aid) other attributes must be merged into; if ``aid`` is not
            the id of an attribute already present in ``entity``, an attribute
            of this identifier and of type ``text`` will be created
    :param cleanup: (optional, default: ``True``) True if attributes in
            ``languages`` should be removed from ``entity`` after they
            are merged; ``base_aid`` is of course never removed.
    :param update_items: (optional, default: ``True``) True if items in
            ``tree`` should be updated with the new ``pid`` and ``aid``.

    Usage example: ::

      >>> import heimdall
      >>> tree == ...  # load HERA tree
      >>> # let's say `tree` contains this entity:
      >>> # <entity id='person'>
      >>> #     <attribute pid='name_de' id='person.name_de_attr'>
      >>> #         <name>Personenname</name>
      >>> #     <attribute>
      >>> #     <attribute pid='name_en' id='person.name_en_attr'>
      >>> #         <name>Name</name>
      >>> #         <description>Name of the person</description>
      >>> #     <attribute>
      >>> #     <attribute pid='name_fr' id='person.name_fr_attr'>
      >>> #         <name>Nom</name>
      >>> #         <description>Nom de la personne</description>
      >>> #     <attribute>
      >>> # </entity>
      >>> # MERGE "columns"/attributes that are translations of one another
      >>> # give ourselves a property for merging human-readable names
      >>> heimdall.createProperty(
      >>>     tree, 'dcmi:title', type='text',
      >>>     name={'en': "Title", 'fr': "Titre", },
      >>>     description={
      >>>         'en': "A name given to the resource.",
      >>>         'fr': "Nom de la ressource.",
      >>>         },
      >>>     uri=[
      >>>         'http://purl.org/dc/terms/title',
      >>>         'http://datacite.org/schema/kernel-4/title',
      >>>         ],
      >>>     )
      >>> # merge the_people names
      >>> e = heimdall.getEntity(tree, lambda n: n.get('id') == 'person')
      >>> merge_l10n_attributes(tree, e, {
      >>>     'person.name_de_attr': 'de',
      >>>     'person.name_en_attr': 'en',
      >>>     'person.name_fr_attr': 'fr',
      >>>     },
      >>>     aid='person.name',
      >>>     pid='dcmi:title')
      >>> # now entity person looks like that:
      >>> # <entity id='person'>
      >>> #     <attribute pid='dcmi:title' id='person.name'>
      >>> #         <name xml:lang='de'>Personenname</name>
      >>> #         <name xml:lang='en'>Name</name>
      >>> #         <name xml:lang='fr'>Nom</name>
      >>> #         <description xml:lang='en'>Name of the person</description>
      >>> #         <description xml:lang='fr'>Nom de la personne</description>
      >>> #     <attribute>
      >>> # </entity>
    """
    entity = heimdall.getEntity(tree, lambda n: n.get('id') == eid)
    if entity is None:
        raise ValueError(f"Entity '{eid}' doesn't exist")
    # Check all attr languages have same pid and type
    aids = list(k for k in languages.keys())
    first_aid = aids[0]
    first_a = heimdall.getAttribute(entity, lambda n: n.get('id') == first_aid)
    if first_a is None:
        raise ValueError(f"Unknown attribute identifier '{first_aid}'")
    base_pid = pid or first_a.get('pid')
    base_aid = aid or f'{base_pid}_attr'
    base_type = _get_node(first_a, 'type')
    if base_type is not None:
        base_type = base_type.text
    amin = 0
    # first pass: consistency checks
    for aid in aids[1:]:
        attr = heimdall.getAttribute(entity, lambda a: a.get('id') == aid)
        if attr is None:
            raise ValueError(f"Attribute '{aid}' doesn't exist in {eid}")
        atype = _get_node(attr, 'type')
        if atype is not None:
            atype = atype.text
        if atype != base_type:
            raise ValueError("Attributes don't all have the same type")
        amin = max(amin, int(attr.get('min')))
    # get or create the attribute that will merge all others of `languages`
    base_a = heimdall.getAttribute(entity, lambda n: n.get('id') == base_aid)
    if base_a is None:
        base_a = heimdall.createAttribute(
                entity, id=base_aid, pid=base_pid,
                min=amin, max=None,
                type=base_type,
                )
    # second pass: merge attributes, and ...
    # * ... if `cleanup` delete `language` attributes (except base_atr ofc)
    # * ... if `update_items`, update_items to use id = base_a.id / base_aid
    items = []
    if update_items:
        items = heimdall.getItems(tree, lambda n: n.get('eid') == eid)
    for aid, language in languages.items():
        attr = heimdall.getAttribute(entity, lambda a: a.get('id') == aid)
        node = _get_node(attr, 'name')
        if node is not None:
            _set_language(node, language)
            base_a.append(node)
        node = _get_node(attr, 'description')
        if node is not None:
            _set_language(node, language)
            base_a.append(node)

        if cleanup and (aid != base_aid):
            attr.getparent().remove(attr)
        for item in items:
            for metadata in heimdall.getMetadata(item, aid=aid):
                metadata.set('aid', base_aid)
                metadata.set('pid', base_pid)
                _set_language(metadata, language)


__copyright__ = "Copyright the pyHeimdall contributors."
__license__ = 'AGPL-3.0-or-later'
