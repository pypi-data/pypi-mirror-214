"""
This module is used as the JSON_ (de)serializer.

.. _JSON: https://www.json.org/
"""
import os
from enum import Enum


class Package(Enum):
    """Supported Python packages for (de)serializing JSON_ objects.

    By default, the builtin :mod:`json` module is used.

    To change which JSON_ package to use you can call :func:`.use` to set
    the backend during runtime, or you can specify an ``MSL_NETWORK_JSON``
    environment variable as the default backend. For example, creating an
    environment variable named ``MSL_NETWORK_JSON`` and setting its value
    to be ``ULTRA`` would use UltraJSON_ to (de)serialize JSON_ objects.

    .. _UltraJSON: https://pypi.python.org/pypi/ujson
    .. _RapidJSON: https://pypi.python.org/pypi/python-rapidjson
    .. _simplejson: https://pypi.python.org/pypi/simplejson
    .. _orjson: https://pypi.org/project/orjson/

    .. versionchanged:: 1.0
       Moved from the :mod:`msl.network.constants` module and renamed.
       Added ``JSON``, ``UJSON``, ``RAPIDJSON`` and ``SIMPLEJSON`` aliases.
       Added ``OR`` (and alias ``ORJSON``) for orjson_.
       Removed ``YAJL``.

    """
    BUILTIN = 'BUILTIN'  #: :mod:`json`
    JSON = 'BUILTIN'  #: :mod:`json`
    ULTRA = 'ULTRA'  #: UltraJSON_
    UJSON = 'ULTRA'  #: UltraJSON_
    RAPID = 'RAPID'  #: RapidJSON_
    RAPIDJSON = 'RAPID'  #: RapidJSON_
    SIMPLE = 'SIMPLE'  #: simplejson_
    SIMPLEJSON = 'SIMPLE'  #: simplejson_
    OR = 'OR'  #: orjson_
    ORJSON = 'OR'  #: orjson_


def use(value):
    """Set which JSON backend to use.

    .. versionadded:: 1.0

    Parameters
    ----------
    value : :class:`.Package` or :class:`str`
        An enum value or member name (case-insensitive).

    Examples
    --------
    .. invisible-code-block: pycon

       >>> from msl.network import json
       >>> original = json.backend.enum

    >>> from msl.network import json
    >>> json.use(json.Package.UJSON)
    >>> json.use('ujson')

    .. invisible-code-block: pycon

       >>> json.use(original)

    """
    backend.use(value)


def serialize(obj):
    """Serialize an object as a JSON-formatted string.

    Parameters
    ----------
    obj
        A JSON-serializable object.

    Returns
    -------
    :class:`str`
        The JSON-formatted string.
    """
    out = backend.dumps(obj, **backend.kwargs_dumps)
    if isinstance(out, bytes):
        return out.decode()
    return out


def deserialize(s):
    """Deserialize a JSON-formatted string to Python objects.

    Parameters
    ----------
    s : :class:`str`, :class:`bytes` or :class:`bytearray`
        A JSON-formatted string.

    Returns
    -------
    The deserialized Python object.
    """
    if isinstance(s, (bytes, bytearray)):
        s = s.decode()
    obj = backend.loads(s, **backend.kwargs_loads)
    return obj


class _Backend(object):

    def __init__(self, value):
        self.loads = None
        self.dumps = None
        self.enum = None
        self.name = ''
        self.kwargs_loads = {}
        self.kwargs_dumps = {}
        self.use(value)

    def use(self, value):
        if isinstance(value, str):
            value = Package[value.upper()]
        if value == Package.BUILTIN:
            import json
            self.loads = json.loads
            self.dumps = json.dumps
            self.enum = Package.BUILTIN
            self.name = 'json'
            self.kwargs_loads = {}
            self.kwargs_dumps = {'ensure_ascii': False}
        elif value == Package.UJSON:
            import ujson
            self.loads = ujson.loads
            self.dumps = ujson.dumps
            self.enum = Package.UJSON
            self.name = 'ujson'
            self.kwargs_loads = {}
            self.kwargs_dumps = {
                'ensure_ascii': False,
                'encode_html_chars': False,
                'escape_forward_slashes': False,
                'indent': 0,
            }
        elif value == Package.SIMPLEJSON:
            import simplejson
            self.loads = simplejson.loads
            self.dumps = simplejson.dumps
            self.enum = Package.SIMPLEJSON
            self.name = 'simplejson'
            self.kwargs_loads = {}
            self.kwargs_dumps = {'ensure_ascii': False}
        elif value == Package.RAPIDJSON:
            import rapidjson
            self.loads = rapidjson.loads
            self.dumps = rapidjson.dumps
            self.enum = Package.RAPIDJSON
            self.name = 'rapidjson'
            self.kwargs_loads = {
                'number_mode': rapidjson.NM_NATIVE
            }
            self.kwargs_dumps = {
                'ensure_ascii': False,
                'number_mode': rapidjson.NM_NATIVE
            }
        elif value == Package.ORJSON:
            import orjson
            self.loads = orjson.loads
            self.dumps = orjson.dumps
            self.enum = Package.ORJSON
            self.name = 'orjson'
            self.kwargs_loads = {}
            self.kwargs_dumps = {}
        else:
            assert False, f'Unhandled JSON backend {value!r}'


# initialize the default backend
backend = _Backend(os.getenv('MSL_NETWORK_JSON', default='BUILTIN'))
