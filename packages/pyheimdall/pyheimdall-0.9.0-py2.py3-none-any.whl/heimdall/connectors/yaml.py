# -*- coding: utf-8 -*-
import heimdall
from ..decorators import connector_in, connector_out
from .json import is_url, _create_tree, _tree2object
from urllib.parse import urlparse
from urllib.request import urlopen
try:
    from yaml import safe_load, dump
    available = True
except ModuleNotFoundError:
    available = False


@connector_in('hera:yaml')
def getDatabase(**options):
    r"""Imports a database from one YAML file

    :param url: URL of a YAML file to read from
    :param \**options: Keyword arguments, see below.
    :return: HERA element tree
    :rtype: lxml.ElementTree

    :Keyword arguments:
        * **encoding** (``str``, default: ``utf-8``) -- ``url`` file encoding

    This function can be used to load a database from a local or remote
    YAML-formatted HERA database file.
    For example: ::

      >>> import heimdall
      >>> url = 'path/to/a/hera/database/file.yaml'
      >>> tree = heimdall.getDatabase(format='hera:json', url=url)
    """
    if not available:
        raise ModuleNotFoundError("Module 'pyyaml' required.")
    url = options['url']
    encoding = options.get('encoding', 'utf-8')
    if not is_url(url):
        with open(url, 'r') as f:
            data = safe_load(f)
    else:
        with urlopen(url) as response:
            data = safe_load(response.read().decode(encoding))
    return _create_tree(data or dict())


@connector_out('hera:yaml')
def serialize(tree, url, **options):
    r"""Serializes a HERA elements tree into a YAML file

    :param tree: HERA elements tree
    :param url: Path of the YAML output file
    :param \**options: Keyword arguments, see below.

    :Keyword arguments:
        * **style** (``str``, default: ``block``) -- YAML flow style for
          output file. Valid values are ``flow`` of ``block``.
          Any value other than ``flow`` will be interpreted as ``block``.
        * **sort** (``bool``, default: ``False``) -- If ``True``, keys will be
          sorted in output file; if ``False`` keys will be written to ``url``
          as they are found in ``tree``.
    """
    if not available:
        raise ModuleNotFoundError("Module 'pyyaml' required.")
    data = _tree2object(tree)
    # write data to file
    style = options.get('style', 'block')
    style = (style == 'flow')
    sort = options.get('sort', False)
    with open(url, 'w', encoding='utf-8') as f:
        dump(data, f, default_flow_style=style, sort_keys=sort)
