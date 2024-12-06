# -*- coding: utf-8 -*-
from lxml import etree as _etree
from urllib.parse import urlparse
from urllib.request import urlopen
from ..decorators import connector_in, connector_out

"""
Provides connectors to HERA-formatted XML files.

This podule defines input and output connectors to databases
composed in full or in part of XML files following the HERA schema.

* :py:class:`heimdall.connectors.xml.getDatabase` is the input connector
* :py:class:`heimdall.connectors.xml.serialize` is the output connector

:copyright: The pyHeimdall contributors.
:licence: Afero GPL, see LICENSE for more details.
:SPDX-License-Identifier: AGPL-3.0-or-later
"""


@connector_in('hera:xml')
def getDatabase(**options):
    url = options['url']
    if not is_url(url):
        tree = _etree.parse(url)
        # can raise OSError (file not found, ...)
    else:
        with urlopen(url) as response:
            tree = _etree.fromstring(response.read().decode())
            # can raise urllib.error.HTTPError (HTTP Error 404: Not Found, ...)
    return tree


def is_url(path):
    schemes = ('http', 'https', )
    return urlparse(path).scheme in schemes


def createDatabase():
    xml_schema = 'http://www.w3.org/2001/XMLSchema-instance'
    hera_xsd = 'https://gitlab.huma-num.fr/datasphere/hera/schema/schema.xsd'
    qname = _etree.QName(xml_schema, 'schemaLocation')
    root = _etree.Element('hera', {qname: hera_xsd})
    properties = _etree.SubElement(root, 'properties')
    entities = _etree.SubElement(root, 'entities')
    items = _etree.SubElement(root, 'items')
    return root


@connector_out('hera:xml')
def serialize(tree, url, **options):
    r"""Serialize a HERA elements tree into an XML file

    :param tree: HERA elements tree
    :param url: Path of the XML file to create
    """
    raise NotImplementedError("TODO")


__copyright__ = "Copyright the pyHeimdall contributors."
__license__ = 'AGPL-3.0-or-later'
__all__ = [
    'getDatabase',
    'createDatabase',
    'serialize',

    '__copyright__', '__license__',
    ]
