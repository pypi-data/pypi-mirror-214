import logging
import jsonpack

class Cache:
    def __init__(self):
        """
        Used to store values.
        
        Methods
        ---
        append, clear, get
        """
        self.cache = {}

    def append(self, name:str, value):
        """
        Add a new value to cache.
        
        Arguments
        ---
        `name` - Name of the cache to append to.

        `value` - The value of cache to set
        """
        try:
            self.cache[name].append(value)
        except KeyError:
            self.cache[name] = [value]

        return self.get(name, -1)

    def clear(self, name:str):
        """
        Clears all cache in this name.

        Arguments
        ---
        `name` - Name of the cache to clear.
        """
        try:
            self.cache[name].clear()
        except KeyError: pass
        return self

    def get(self, name:str, index:int, default=None):
        """
        Returns the cached value.

        Arguments
        ---
        `name` - Name of the cache.

        `index` - Index in cache to fetch.

        `default` - Default value to return if cache item cannot be found.
        """
        try:
            return self.cache[name][index]
        except IndexError:
            return default
        
class ResourcePath(object):
    def __init__(self, module_type:str, node_name:str):
        """
        Describes a resrouce path used for annotations.

        Arguments
        ---
        `module_type` - The node type that it should except.

        `node_name` - The node name that is should except.

        Methods
        ---
        exists
        """
        self.module_type = module_type
        self.node_name = node_name

    # TODO
    def exists(self) -> bool:
        """
        Checks if this resource path exists
        """
        raise NotImplementedError()
    
class Context:
    def __init__(self, node, module, **extras):
        """
        Arguments
        ---
        `node` - The node that this context came from.

        `module` - The module that this context came from.

        **extras - Extra arguments to pass.

        Methods
        ---
        add_extras, copy, from_dict, to_dict
        """
        self.logger = logging.getLogger('App')
        self.node = node
        self.module = module
        self.app = jsonpack.getApp()
        self.add_extras(**extras)

    def add_extras(self, **kw):
        """
        Extra arguments to pass.
        """
        for key, value in kw.items(): setattr(self, str(key), value)
        return self

    def copy(self):
        """
        Creates a copy of this class.
        """
        return self.__class__.from_dict(self.to_dict())
    
    @classmethod
    def from_dict(cls, data:dict):
        """
        Converts a :class:`dict` to a :class:`Context`.
        """
        self = cls.__new__(cls)
        for key, value in data.items():
            setattr(self, str(key), value)
        return self

    def to_dict(self) -> dict:
        """
        Converts a :class:`Context` to a :class:`dict.`
        """
        result = {
            key: getattr(self, key)
            for key in self.__dict__
        }
        return result

    def __repr__(self) -> str:
        inner = ', '.join((f'{k}={v!r}' for k, v in self.__dict__.items() if not k.startswith('_')))
        return f'Context({inner})'
