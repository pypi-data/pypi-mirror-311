# -*- coding: utf-8 -*-
from .heimdall import CONNECTORS_IN as _IN, CONNECTORS_OUT as _OUT
from functools import wraps


def connector_in(format):
    # just two lines to support syntax: @connector_in('format')
    # as long as syntax: @connector_in(['format1', 'format2'])
    if type(format) is not list:
        format = [format, ]

    def decorator(function):
        # register ``function`` as an IN connector
        for f in format:
            _IN[f] = function

        @wraps(function)
        def wrapper(*args, **kwargs):
            # call ``function`` and return its result
            return function(*args, **kwargs)
        return wrapper
    return decorator


def connector_out(format):
    # just two lines to support syntax: @connector_out('format')
    # as long as syntax: @connector_out(['format1', 'format2'])
    if type(format) is not list:
        format = [format, ]

    def decorator(function):
        # register ``function`` as an OUT connector
        for f in format:
            _OUT[f] = function

        @wraps(function)
        def wrapper(*args, **kwargs):
            # call ``function`` and return its result
            return function(*args, **kwargs)
        return wrapper
    return decorator
