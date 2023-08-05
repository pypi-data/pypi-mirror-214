import importlib.util
import os
import logging
import json
import sys
import threading
import glob
import re
import jsonschema
import inspect
import time

from .exceptions import AppError
from .node import Node, NodeProxy, Componentable, Eventable
from .util import Cache, ResourcePath, Context

__version__ = '1.0.0'
__root_app__ = None

logger = logging.getLogger('Pack')

def getApp():
    """Returns the root App"""
    if __root_app__ is None: raise AppError('App has not started yet! Use App.run() to start your app.')
    return __root_app__

class ManifestProxy:
    def __init__(self, layer: dict):
        self.__dict__.update(layer)

    def __len__(self) -> int:
        return len(self.__dict__)

    def __repr__(self) -> str:
        inner = ', '.join((f'{k}={v!r}' for k, v in self.__dict__.items() if not k.startswith('_')))
        return f'ManifestProxy({inner})'

    def __getattr__(self, attr: str) -> None:
        return None

    def __eq__(self, other: object) -> bool:
        return isinstance(other, ManifestProxy) and self.__dict__ == other.__dict__

class Manifest:
    __slots__ = (
        'name',
        'description',
        'uuid',
        '_modules',
        '_version',
        '_dependencies',
        '_path',
        '_scripts',
        '_icon',
        '__file__'
    )

    def __init__(self, name:str, description:str, uuid:str):
        """
        A class used to describe a manifest.json file.

        Arguments
        ---
        `name` - Name of the pack.

        `description` - Description of the pack.

        `uuid` - UUID of this pack.

        `scripts` - A list of scripts.

        `version` - The packs version.

        `path` - This packs path.

        `modules` - This of modules this pack uses.

        `dependencies` - List of pack dependencies.

        Methods
        ---
        enable_scripts, set_version, set_path, set_icon, add_module, remove_module, clear_modules, add_dependency, remove_dependency, clear_dependencies, from_dict, to_dict, schema, join
        """
        self.name = str(name)
        self.description = str(description)
        self.uuid = str(uuid)

    @property
    def scripts(self):
        return getattr(self, '_scripts', False)
    
    @scripts.setter
    def scripts(self, value:bool):
        self.enable_scripts(value)

    def enable_scripts(self, value:bool):
        """
        Whether or not this pack can load scripts.

        Arguments
        ---
        `value` - True if it can load scripts. False if it cannot load scripts (default)
        """
        if value is None: self._scripts = False
        elif isinstance(value, bool):
            self._scripts = value
        else:
            raise TypeError(f'Expected bool or None but got {value.__class__.__name__} instead.')

    @property
    def version(self):
        return getattr(self, '_version', None)
    
    @version.setter
    def version(self, version):
        self.set_version(version=version)
    
    def set_version(self, *, version:list[int]):
        """
        Sets the version for the pack.

        Arguments
        ---
        `version` - The version to set in the format [major, minor, patch]
        """
        if version is None:
            try:
                del self._version
            except AttributeError:
                pass
        else:
            self._version = Version(*version)

        return self

    @property
    def path(self):
        return str(getattr(self, '_path', None))  # type: ignore

    @path.setter
    def path(self, fp):
        self.set_path(fp=fp)

    def set_path(self, *, path:str):
        """
        Sets the path for the pack.

        Arguments
        ---
        `path` - This packs path
        """
        if path is None:
            try:
                del self._path
            except AttributeError:
                pass
        else:
            self._path = str(path)

        return self
    
    @property
    def icon(self):
        return ManifestProxy(getattr(self, '_icon', {}))  # type: ignore

    def set_icon(self, *, fp:str):
        """
        Sets the icon for the pack.

        Arguments
        ---
        `fp` - Path to the pack icon to use.
        """
        if fp is None:
            try:
                del self._icon
            except AttributeError:
                pass
        else:
            self._icon = {
                'fp': str(fp)
            }

        return self
    
    @property
    def modules(self) -> list:
        return [ManifestProxy(d) for d in getattr(self, '_modules', [])]  # type: ignore
    
    def add_module(self, *, version:list[int], type:str, uuid:str, path:str=None):
        """
        Adds a module to the manifest.

        Arguments
        ---
        `version` - The version of this module.

        `type` - The type of module to load.
        
        `uuid` - UUID of this module.
        
        `path` - If type=script this is the realitive path to the Python file.
        """
        module = {
            'version': version,
            'type': str(type),
            'uuid': str(uuid),
            'path': str(path)
        }
        try:
            self._modules.append(module)
        except AttributeError:
            self._modules = [module]
        return self

    def remove_module(self, index:int):
        """
        Removes a module at a specified index.

        Arguments
        ---
        `index` - Index in Manifest.modules to delete.
        """
        try:
            del self._modules[index]
        except (AttributeError, IndexError):
            pass
        return self

    def clear_modules(self):
        """
        Removes all modules from this manifest.
        """
        try:
            self._nodes.clear()
        except AttributeError:
            self._nodes = []
        return self

    @property
    def dependencies(self) -> list:
        return [ManifestProxy(d) for d in getattr(self, '_dependencies', [])]  # type: ignore
    
    def add_dependency(self, *, uuid:str, version:list=None, min_version:list=None, description:str=None):
        """
        Adds a dependency to the manifest.

        Arguments
        ---
        `uuid` - UUID of the pack that is needed. Should match the UUID defined at the top of the manifest.json of the needed pack.

        `version` - The exact version that is needed.

        `min_version` - The minimum allowed version.

        `description` - Descirption of this dependcy.
        """
        dependency = {
            'description': str(description),
            'uuid': str(uuid),
            'version': version,
            'min_version': min_version
        }
        if dependency['version'] is not None:
            dependency['version'] = Version(*dependency['version'])
            
        if dependency['min_version'] is not None:
            dependency['min_version'] = Version(*dependency['min_version'])

        try:
            self._dependencies.append(dependency)
        except AttributeError:
            self._dependencies = [dependency]
        return self

    def remove_dependency(self, index:int):
        """
        Removes a dependency at a specified index.

        Arguments
        ---
        `index` - Deletes the dependent pack from Manifest.dependencies.
        """
        try:
            del self._dependencies[index]
        except (AttributeError, IndexError):
            pass
        return self

    def clear_dependencies(self):
        """
        Removes all dependencies from this manifest.
        """
        try:
            self._dependencies.clear()
        except AttributeError:
            self._dependencies = []
        return self

    def to_dict(self) -> dict:
        """
        Converts a :class:`Manifest` to a :class:`dict`
        """
        result = {
            key[1:]: getattr(self, key)
            for key in self.__slots__
            if key[0] == '_' and hasattr(self, key)
        }
        return result
    
    @classmethod
    def from_dict(cls, data:dict):
        """
        Converts a :class:`dict` to a :class:`Manifest`
        """
        self = cls.__new__(cls)

        self.name = data.get('name', None)
        self.description = data.get('description', None)
        self.uuid = data.get('uuid', None)
        self.version = data.get('version', None)

        if self.name is not None:
            self.name = str(self.name)

        if self.description is not None:
            self.description = str(self.description)
            
        if self.uuid is not None:
            self.uuid = str(self.uuid)

        # special cases

        for dep in data.get('dependencies', []):
            self.add_dependency(**dep)
            
        for mod in data.get('modules', []):
            self.add_module(**mod)

        return self

    @classmethod
    def schema(self):
        """
        This classes JSON schema used for validation when loading the file.
        """
        return {
            "$schema": "http://json-schema.org/draft-07/schema",
            'type': 'object',
            'required': [
                'name',
                'description',
                'uuid',
                'version'
            ],
            'properties': {
                "name": {
                    'type': 'string'
                },
                "description": {
                    'type': 'string'
                },
                'uuid': {
                    'type': 'string'
                },
                "version": {
                    'type': 'array',
                    'type': 'array',
                    'items': {
                        'type': 'integer'
                    },
                    'minItems': 3,
                    'maxItems': 3
                },
                "modules": {
                    'type': 'array',
                    'items': {
                        'type': 'object',
                        'required': [
                            'version',
                            'type',
                            'uuid'
                        ],
                        'properties': {
                            'version': {
                                'type': 'array',
                                'items': {
                                    'type': 'integer'
                                },
                                'minItems': 3,
                                'maxItems': 3
                            },
                            "type": {
                                'type': 'string'
                            },
                            "uuid": {
                                'type': 'string'
                            },
                            'path': {
                                'type': 'string'
                            }
                        },
                        'additionalProperties': False
                    }
                },
                "dependencies": {
                    'type': 'array',
                    'items': {
                        'type': 'object',
                        'required': [
                            'uuid'
                        ],
                        'anyOf': [
                            {'required': ['version']},
                            {'required': ['min_version']}
                        ],
                        'properties': {
                            'uuid': {
                                'type': 'string'
                            },
                            'version': {
                                'type': 'array',
                                'items': {
                                    'type': 'integer'
                                },
                                'minItems': 3,
                                'maxItems': 3
                            },
                            'min_version': {
                                'type': 'array',
                                'items': {
                                    'type': 'integer'
                                },
                                'minItems': 3,
                                'maxItems': 3
                            },
                            'description': {
                                'type': 'string'
                            }
                        },
                        'additionalProperties': False
                    }
                }
            },
            'additionalProperties': False
        }

    def join(self, *paths:str):
        """
        Joins all paths realitive to this packs path.
        """
        return os.path.join(self.path, re.sub(r'^/|^\\|^./|^.\\', '', os.path.join(*paths))).replace('/', '\\')

class Script:
    def __init__(self, app, name:str, fp:str):
        """
        WARNING: Do not use! use App.add_script(name, fp)

        Arguments
        ---
        `app` - The root App.

        `name` - Name of the script.

        `fp` - File path to the Python script.

        Methods
        ---
        load, on_enable, on_disable
        """
        self.app = app
        self.name = name
        self.fp = fp
        self.module = None

        if os.path.isdir(self.fp): self.fp = os.path.join(self.fp, '__init__.py')
        if os.path.exists(self.fp)==False: logger.warning(f"'{self.fp}' Script not found!")

    def load(self):
        """
        Runs the Python script
        """
        global loading_script
        spec = importlib.util.spec_from_file_location(self.name, self.fp)
        foo = importlib.util.module_from_spec(spec)
        sys.modules[self.name] = foo
        spec.loader.exec_module(foo)
        self.app.loading_script = foo
        self.module = foo
        self.on_enable()

    def on_enable(self):
        """
        Runs the Python scripts on_enable method if defined.
        """
        try: self.module.on_enable(self.app)
        except (TypeError): pass
        return self
    
    def on_disable(self):
        """
        Runs the Python scripts on_disable method if defined.
        """
        try: self.module.on_disable(self.app)
        except (TypeError): pass
        return self

class _node:
    def __init__(self, module, pathname, cls, mimetype:str=None, resourcepath_command=None):
        """Internal class"""
        self.app = getApp()
        self.module = module
        self.src = '' # Python file that created this node
        self.path = pathname
        self.path_args = {}
        self.cls = cls
        self.traits = self.cls.traits # Traits are used for the JSON schema
        self._mimetype = mimetype
        self.resourcepath_command = resourcepath_command
        self.name = str(cls.__name__).lower()
        if mimetype is None: self._mimetype = 'application/json'

        if resourcepath_command is None: self.resourcepath_command = self.resourcepath

    @property
    def ref(self):
        return ResourcePath(self.module.module_type, self.name)

    @property
    def path(self):
        return self._path
    
    @path.setter
    def path(self, value):
        self._path = value

    @property
    def mimetype(self):
        for m in self.app.mimetypes:
            mime = self._mimetype.split('/')
            if len(mime) == 2:
                if m.type == mime[0]:
                    if m.subtype is None: return m.func
                    elif m.subtype == mime[1]: return m.func
            elif len(mime) == 1:
                if m.type == mime[0]:
                    return m.func
                
        logger.warning(f"mimetype '{self._mimetype}' is not defined!")
        return None

    @property
    def schema(self):
        """Returns the JSON schema for this node."""
        return schema(self, self.cls, self.traits)

    def resourcepath(self, node:Node, path:str, manifest:Manifest, **kw):
        """Returns the namespace id of this item"""
        res = os.path.dirname(self.path).replace('*', '')
        return os.path.relpath(path, manifest.join(res)).replace('\\','/').replace(os.path.splitext(path)[1], '')
        
    # REGISTER COMPONENTS
    def add_component(self, func, name:str=None):
        """
        Adds a component to the node.

        Arguments
        ---
        `func` - The function to run when this component is defined.

        `name` - Name of the component to add.
        """
        com = _component(Context(self, self.module), func, name)
        try:
            self.__components__[com.name] = com
        except AttributeError:
            self.__components__ = {com.name: com}

        return self

    def remove_component(self, name:str):
        """
        Removes a component at a specified name.

        Arguments
        ---
        `name` - Name of the component to remove.
        """
        try:
            del self.__components__[name]
        except (AttributeError, IndexError):
            pass

        return self
        
    def clear_components(self):
        """
        Removes all components from this node.
        """
        try:
            self.__components__.clear()
        except AttributeError:
            self.__components__ = {}
        return self

    def component(self, name:str=None):
        """
        Register a new component for this node.

        Arguments
        ---
        `name` - Name of the node to register.
        """
        def wrapper(func):
            return self.add_component(func, name)
        return wrapper

class _event:
    def __init__(self, ctx:Context, func, name:str=None):
        """Internal class"""
        self.ctx = ctx
        self.app = getApp()
        self.src = '' # Python file that created this event
        self.func = func
        self.name = name
        self.on_error = None
        if name is None: self.name = str(func.__name__)

    def error(self, func):
        self.on_error = func

    @property
    def schema(self):
        return schema(None, self.func, {}, True, skiparg=0)

    def call(self, options:dict, extra:dict={}):
        try:
            ctx = self.ctx.copy().add_extras(**extra)
            return self.func(ctx, **options)

        except Exception as err:
            if self.on_error is not None:
                self.on_error(self, err)
            else:
                raise err
    
class _component:
    def __init__(self, ctx:Context, func, name:str=None):
        """Internal class"""
        self.ctx = ctx
        self.src = '' # Python file that created this component
        self.func = func
        self.on_error = None
        if name is None: self.name = self.ctx.module.namespace+':'+func.__name__
        else: self.name = self.ctx.module.namespace+':'+name
        
    def error(self, func):
        self.on_error = func

    @property
    def schema(self):
        return schema(None, self.func, {}, True, skiparg=0)

    def call(self, options:dict, extra:dict={}):
        try:
            ctx = self.ctx.copy().add_extras(**extra)
            return self.func(ctx, **options)
        except Exception as err:
            if self.on_error is not None:
                self.on_error(self, err)
            else:
                raise err
    
class AppProxy:
    def __init__(self, layer: dict):
        self.__dict__.update(layer)

    def __len__(self) -> int:
        return len(self.__dict__)

    def __repr__(self) -> str:
        inner = ', '.join((f'{k}={v!r}' for k, v in self.__dict__.items() if not k.startswith('_')))
        return f'AppProxy({inner})'

    def __getattr__(self, attr: str) -> None:
        return None

    def __eq__(self, other: object) -> bool:
        return isinstance(other, AppProxy) and self.__dict__ == other.__dict__

class App:
    def __init__(self, default_namespace:str='default'):
        """
        The root app.

        Arguments
        ---
        `default_namespace` - The default namespace for components. if namespace is "foo" then a component can be defined "foo:bar" or "bar"

        Methods
        ---
        bind, unbind, call_bind_event, get_node, add_module, remove_module, clear_modules, add_mimetype, remove_mimetype, clear_mimetypes, add_script, remove_script, clear_scripts, add_path, remove_path, clear_paths, reload, unload, load, dump_registries, run
        """
        global __root_app__
        __root_app__ = self
        self.logger = logger
        self.default_namespace = default_namespace
        self.packs = {}
        self.alive:bool = False
        self.loading_script = None # script that is currently being loaded
        self.bind_events = {}
        self.cache = Cache()

        # reg
        self.nodes = {}
        self.items = {} # registry from packs
        self.nodes = {}
        self.events = {}
        self.packs = {}
    
    def builtins(self):
        """
        Load builtin mimetypes
        
        Supported: https://developer.mozilla.org/en-US/docs/Web/HTTP/Basics_of_HTTP/MIME_types
        - application/json
        - application/yaml (Needs PyYAML)
        - application/zip
        - font/* TODO
        - text/* TODO (css, html, javascript)
        - video/* TODO
        - image/* (Needs Pillow)
        """
        import zipfile
        import tarfile
        # xml
        @self.mimetype('application', 'json')
        def application_json(file, node, subtype) -> Node:
            valid, data = validate(file, node.schema, 'json')
            if valid:
                n = node.cls.from_dict(data)
                n.__file__ = file
                return n
        
        @self.mimetype('application', 'zip')
        def application_zip(file, node, subtype) -> Node:
            zip = zipfile.ZipFile(file)
            n = node.cls.from_dict({'zip': zip})
            n.__file__ = file
            return n
            
        @self.mimetype('application', 'tar')
        def application_tar(file, node, subtype) -> Node:
            tar = tarfile.TarFile(file)
            n = node.cls.from_dict({'tar': tar})
            n.__file__ = file
            return n
            
        try:
            import yaml
            @self.mimetype('application', 'yaml')
            def application_yaml(file, node, subtype) -> Node:
                valid, data = validate(file, node.schema, 'yaml')
                if valid:
                    n = node.cls.from_dict(data)
                    n.__file__ = file
                    return n
        except ImportError: pass
        
        try:
            from PIL import Image
            import imghdr
            @self.mimetype('image')
            def image(file, node, subtype) -> Node:
                ext = imghdr.what(file)
                if ext is not None and (subtype is not None and ext==subtype):
                    img = Image.open(file)
                    n = node.cls.from_dict({'image': img})
                    n.__file__ = file
                    return n
                else: logging.warning(f"'{file}' Failed to load image! Expected a {str(subtype).upper()} but got a {ext.upper()}")
        except ImportError: pass

    def bind(self, event:str, func):
        """
        Run a function when a certain event triggers.

        Arguments
        ---
        `event` - The event type to bind to.
        
        `func` - The function to run.

        Events
        ---
        `BeforeLoad` - Before all packs have been loaded.

        `AfterLoad` - After all packs have been loaded.
        """
        try: self.bind_events[str(event)].append(func)
        except KeyError: self.bind_events = {event: [func]}
        return self
    
    def unbind(self, event:str):
        """
        Removes a bind event.

        Arguments
        ---
        `event` - The event type to remove.
        """
        del self.bind_events[str(event)]

    def trigger_bind(self, event:str):
        """
        Runs the bind event callbacks.
        """
        funcs = self.bind_events.get(str(event))
        if funcs is not None:
            for f in funcs: f(self)
        return self

    def get_node(self, name) -> Node:
        """
        Returns with the Node.

        Arguments
        ---
        `name` - The name of the node to get.
        """
        if isinstance(name, Node):
            name = name.__class__.__name__.lower()

        for module_type, nodes in self.nodes.items():
            node = nodes.get(name)
            if node is not None: return node

    @property
    def modules(self) -> dict:
        return getattr(self, '_modules', [])
    
    def add_module(self, module_type:str, namespace:str, cls):
        """
        Adds a module to the app.

        Arguments
        ---

        `module_type` - The module type.

        `namespace` - Namespace of this modules items.

        `cls` - The Module class. 
        """
        try:
            self._modules[module_type][namespace] = cls
        except AttributeError:
            self._modules = {module_type: {namespace: cls}}

        except KeyError:
            self._modules[module_type] = {namespace: cls}
        return cls
    
    def remove_module(self, name:str):
        """
        Removes a module at a specified name.

        Arguments
        ---
        `name` - Name in App.modules to delete.
        """
        try:
            del self._modules[name]
        except (AttributeError, KeyError):
            pass
        return self

    def clear_modules(self):
        """
        Removes all modules from this app.
        """
        try:
            self._modules.clear()
        except AttributeError:
            self._modules = {}
        return self
    
    @property
    def mimetypes(self) -> list:
        return [AppProxy(d) for d in getattr(self, '_mimetypes', [])]
    
    def add_mimetype(self, func, type:str, subtype:str=None):
        """
        Adds a mimetype to the app.

        WARNING: Use App.mimetype decorator function instead.

        Arguments
        ---
        `func` - The function to call.

        `type` - The type of mimetype. type/subtype

        `subtype` - The subtype of mimetype. type/subtype
        """
        mimetype = {'func': func, 'type': type, 'subtype': subtype}
        try:
            self._mimetypes.append(mimetype)
        except AttributeError:
            self._mimetypes = [mimetype]
        return AppProxy(mimetype)
    
    def remove_mimetype(self, index:int):
        """
        Removes a mimetype at a specified index.

        Arguments
        ---
        `index` - Index in App.mimetypes to delete.
        """
        try:
            del self._mimetypes[index]
        except (AttributeError, KeyError):
            pass
        return self

    def clear_mimetypes(self):
        """
        Removes all scripts from this app.
        """
        try:
            self._mimetypes.clear()
        except AttributeError:
            self._mimetypes = []
        return self
    
    def mimetype(self, type, subtype:str=None):
        """
        Adds a mimetype to the app.

        Arguments
        ---
        `type` - The type of mimetype. type/subtype

        `subtype` - The subtype of mimetype. type/subtype
        """
        def decorator(func):
            return self.add_mimetype(func, type, subtype)
        return decorator

    @property
    def scripts(self) -> dict[Script]:
        return getattr(self, '_scripts', {})
    
    def add_script(self, name:str, fp:str):
        """
        Adds a script to the app.

        Arguments
        ---

        `name` - Name of the script.

        `fp` - Path to the Python FILE or Python PACKAGE.
        """
        script = Script(self, name, fp)
        try:
            if script.name not in self._scripts:
                self._scripts[script.name] = script
            else:
                logger.warning(f"'{script.fp}' Duplicate script found '{script.name}'")
        except AttributeError:
            self._scripts = {script.name: script}
        return script
    
    def remove_script(self, name:str):
        """
        Removes a script at a specified name.

        Arguments
        ---
        `name` - Name in App.scripts to delete.
        """
        try:
            del self._scripts[name]
        except (AttributeError, KeyError):
            pass
        return self

    def clear_scripts(self):
        """
        Removes all scripts from this app.
        """
        try:
            self._scripts.clear()
        except AttributeError:
            self._scripts = {}
        return self
    
    @property
    def paths(self) -> list:
        return [AppProxy(d) for d in getattr(self, '_paths', [])]  # type: ignore
    
    def add_path(self, path, scripts:bool=False):
        """
        Adds a path to the app.

        Arguments
        ---

        `path` - Folder to load all packs.

        `scripts` - When true all packs in this pack can use scripts.
        """
        try:
            os.makedirs(path, exist_ok=True)
            self._paths.append({'path':path, 'scripts': scripts})
        except AttributeError:
            self._paths = [{'path':path, 'scripts': scripts}]
        return self

    def remove_path(self, index:int):
        """
        Removes a path at a specified index.

        Arguments
        ---
        `index` - Index in App.paths to delete.
        """
        try:
            del self._paths[index]
        except (AttributeError, IndexError):
            pass
        return self

    def clear_paths(self):
        """
        Removes all paths from this app.
        """
        try:
            self._paths.clear()
        except AttributeError:
            self._paths = []
        return self
    
    def reload(self, threaded:bool=True):
        """
        Reload all packs

        Arguments
        ---
        `threaded` - When true it will reload all packs in a new thread.
        """
        logger.info('Reloading!')
        self.unload()
        if threaded: threading.Thread(target=self.load, args=(), daemon=True).start()
        else: self.load()

    def unload(self):
        """
        Unloads all packs.
        """
        # Unload all nodes
        for module_name, modules in self.items.items():
            for node_name, nodes in modules.items():
                for name, node in nodes.items():
                    node.on_unload(Context(node, None))
            
        self.cache.clear('images') # Clear cached images
        self.clear_mimetypes()
        self.clear_modules()
        self.events = {}
        self.nodes = {}
        self.items = {}

        for name, script in self.scripts.items(): script.on_disable()
        self.clear_scripts()

    def load(self):
        """
        Load all packs from the configured paths.
        
        WARNING: If you need to reload all packs use App.reload instead!
        """
        self.builtins()
        self.trigger_bind('BeforeLoad')
        start = time.time()
        # Validate packs
        for p in self.paths:
            for name in os.listdir(p.path):
                path = os.path.join(p.path, name)
                manifest_path = os.path.join(path, 'manifest.json')
                if os.path.exists(manifest_path):
                    valid, data = validate(manifest_path, Manifest.schema())
                    if valid:
                        manifest = Manifest.from_dict(data)
                        manifest.__file__ = manifest_path
                        manifest.enable_scripts(p.scripts)
                        manifest.set_path(path=path)
                        icon = os.path.join(path, 'pack_icon.png')
                        # if os.path.isfile(icon):
                        #     manifest.set_icon(fp=icon)
                        # manifest.set_icon()
                        self.packs[str(manifest.uuid)] = manifest
         
        # TODO algrithm to re-order path list for depcies
        # pack1 requires pack2. so it should order them [pack2, pack1] that way pack2 loads first, then pack1
        
        # Check dependencies
        for uuid, manifest in self.packs.items():
            for dep in manifest.dependencies:
                res = self.packs.get(dep.uuid)
                if res is None:
                    logger.warning(f"'{manifest.path}' Missing dependency with ID '{dep.uuid}' and version {dep.version}")
                
                else:
                    if dep.version is not None:
                        if manifest.version != dep.version:
                            logger.warning(f"'{manifest.path}' Missing dependency with ID '{dep.uuid}' and version {dep.version}")

                    elif dep.min_version is not None:
                        if manifest.version < dep.min_version:
                            logger.warning(f"'{manifest.path}' Missing dependency with ID '{dep.uuid}' and version {dep.min_version}")

        # Load scripts
        for uuid, manifest in self.packs.items():
            for module in manifest.modules:
                if module.type == 'script': # Built-in module type 'script'
                    if manifest.scripts:
                        script_fp = manifest.join(module.path)
                        script = self.add_script(module.uuid[0:8], script_fp)
                        script.load()
                    else:
                        logger.warning(f"'{manifest.path}' Could not load module as scripts are disabled!")

        self.loading_script = None
        # Load modules and nodes
        for uuid, manifest in self.packs.items():
            for module in manifest.modules:
                if module.type != 'script':
                    regs = self.nodes.get(module.type)
                    if regs is not None:
                        for name, node in regs.items(): # Search for nodes
                            files = glob.glob(manifest.join(node.path), recursive=True)
                            for file in files:
                                if node.mimetype is not None:
                                    types = node._mimetype.split('/')
                                    subtype = None
                                    if len(types) == 2: subtype = types[1]
                                    reg = node.mimetype(file, node, subtype)
                                    if reg is not None:
                                        reg._app = self
                                        reg.on_load(Context(reg, None))
                                        name = node.resourcepath_command(node, file, manifest)
                                        try:
                                            self.items[module.type][node.name][name] = reg
                                        except KeyError:
                                            self.items[module.type][node.name] = {name: reg}


                    else:
                        logger.warning(f"'{manifest.path}' {module.type} is not a valid module type! Allowed values: {', '.join(self.nodes)}, script")

        tme = round(time.time() - start, 2)
        logger.info(f'Done! ({tme} ms)')
        self.trigger_bind('AfterLoad')

    def dump_registries(self, path:str=''):
        """
        Generates a folder of files that list all loaded registries.

        Arguments
        ---
        `path` - Path to dump all registries
        """
        if self.alive:
            for module_type, module in self.items.items():
                node_path = os.path.join(path, 'gen', str(module_type))
                os.makedirs(node_path, exist_ok=True)
                result = {}
                for node_name, node in module.items():
                    result[node_name] = {'entries': {}}
                    index = 0
                    for name in node:
                        result[node_name]['entries'][name] = {'protocol_id': index}
                        index +=1
                with open(os.path.join(node_path, 'registries.json'), 'w') as w:
                    w.write(json.dumps(result, indent=4))
        else:
            raise RuntimeError('App must be running before you can run this method!')

    def run(self, threaded:bool=False, logger:bool=True):
        """
        Runs the app.
        
        Arguments
        ---
        `threaded` - When true it will load all packs on a thread. (Mainly used for tkinter apps which would otherwise freeze).

        `multithreaded` - When true it will load all packs using multiple threads for faster loading times.

        `logger` - When false it will disable the built-in logger.
        """
        if self.alive is False:
            if logger is False: logger.disabled = True
            if threaded: threading.Thread(target=self.load, args=(), daemon=True).start()
            else: self.load()
            self.alive = True

class ModuleProxy:
    def __init__(self, layer: dict):
        self.__dict__.update(layer)

    def __len__(self) -> int:
        return len(self.__dict__)

    def __repr__(self) -> str:
        inner = ', '.join((f'{k}={v!r}' for k, v in self.__dict__.items() if not k.startswith('_')))
        return f'ModuleProxy({inner})'

    def __getattr__(self, attr: str) -> None:
        return None

    def __eq__(self, other: object) -> bool:
        return isinstance(other, ModuleProxy) and self.__dict__ == other.__dict__

class Module:
    def __init__(self, module_type:str, namespace:str):
        """
        Defines a modules nodes when defined in the packs manifest.json.

        Arguments
        ---
        `namespace` - The namespace used for components. `<namespace>:<component_name>`

        `module_type` - The type of module this is. example; "data" for server side modules, "resources" is for client side modules.

        Methods
        ---
        add_node, remove_node, clear_nodes, node, add_event, remove_event, clear_events, event
        """
        self.app = getApp()

        self.src = self.app.loading_script.__file__ if self.app.loading_script is not None else '?'
        self.namespace = str(namespace)
        self.module_type = str(module_type)

        if self.module_type not in self.app.items: self.app.items[self.module_type] = {}

        self.app.add_module(self.module_type, self.namespace, self)

    @property
    def nodes(self) -> list:
        return [str(d) for d in getattr(self, '_nodes', [])]  # type: ignore

    def add_node(self, cls:Node, *, pathname:str, mimetype:str=None, resourcepath_command=None):
        """
        Creates a node from a regular class.

        WARNING: Do not use! Use Module.node decorator method instead.

        Arguments
        ---
        `path` - The glob path to load these file(s) from.

        `mimetype` - The mimetype to except for this node.

        `resourcepath_command` - The command to generate the resrouce path.
        """
        node = _node(self, pathname, cls, mimetype, resourcepath_command)
        node.src = self.src
        try:
            if node.name not in self.app.nodes[self.module_type]:
                self.app.nodes[self.module_type][node.name] = node
            else:
                logger.warning(f"'{node.src}' Duplicate node found '{node.name}'")
        except KeyError:
            self.app.nodes[self.module_type] = {node.name: node}

        return node

    def remove_node(self, name:str):
        """
        Removes a node with the specified name.

        Arguments
        ---
        `name` - Name of the node to remove.
        """
        try:
            del self._nodes[name]
        except (AttributeError, IndexError):
            pass
        return self

    def clear_nodes(self):
        """
        Removes all nodes from this module.
        """
        try:
            self._nodes.clear()
        except AttributeError:
            self._nodes = []
        return self

    def node(self, pathname:str, mimetype:str=None, resourcepath_command=None):
        """
        Creates a node from a regular class.

        Arguments
        ---
        `path` - The glob path to load these file(s) from.

        `mimetype` - The mimetype to except for this node.

        `resourcepath_command` - The command to generate the resrouce path.
        """
        def decorator(cls):
            return self.add_node(cls, pathname=pathname, mimetype=mimetype, resourcepath_command=resourcepath_command)
        return decorator
    
    @property
    def events(self) -> list:
        return [str(d) for d in getattr(self, '_events', [])]  # type: ignore
    
    def add_event(self, func, name:str=None):
        """
        Creates an event from a regular function.

        WARNING: Do not use! Use Module.event decorator method instead.

        Arguments
        ---
        `name` - Name of this event.
        """
        ctx = Context(None, self)
        event = _event(ctx, func, name)
        event.src = self.src
        if event.name not in self.app.events:
            self.app.events[event.name] = event
        else:
            logger.warning(f"'{event.src}' Duplicate event found '{event.name}'")
        return event

    def remove_event(self, name:str):
        """
        Removes an event with the specified name.

        Arguments
        ---
        `name` - Name of the event to delete.
        """
        try:
            del self._events[name]
        except (AttributeError, IndexError):
            pass
        return self

    def clear_events(self):
        """
        Removes all events from this module.
        """
        try:
            self._events.clear()
        except AttributeError:
            self._events = {}
        return self

    def event(self, name:str=None):
        """
        Creates an event from a regular function.

        Arguments
        ---
        `name` - Name of this event.
        """
        def decorator(func):
            return self.add_event(func, name)
        return decorator
    
class Version:
    __slots__ = (
        'major',
        'minor',
        'patch'
    )

    def __init__(self, major:int=0, minor:int=0, patch:int=0):
        """
        Describes a pack version using [Semantic Versioning](https://semver.org/spec/v2.0.0.html)
        
        Arguments
        ---
        `major` - version when you make incompatible API changes

        `minor` - version when you add functionality in a backward compatible manner

        `path` - version when you make backward compatible bug fixes

        Methods
        ---
        __str__, __eq__, __le__, __ge__, __lt__, __gt__
        """
        self.major = int(major)
        self.minor = int(minor)
        self.patch = int(patch)

    def __str__(self):
        return f'{self.major}.{self.minor}.{self.patch}'
    
    def __eq__(self, other):
        return isinstance(other, Version) and (self.major, self.minor, self.patch) == (other.major, other.minor, other.patch)
    
    def __le__(self, other):
        return isinstance(other, Version) and (self.major, self.minor, self.patch) <= (other.major, other.minor, other.patch)

    def __ge__(self, other):
        return isinstance(other, Version) and (self.major, self.minor, self.patch) >= (other.major, other.minor, other.patch)
    
    def __lt__(self, other):
        return isinstance(other, Version) and (self.major, self.minor, self.patch) < (other.major, other.minor, other.patch)
    
    def __gt__(self, other):
        return isinstance(other, Version) and (self.major, self.minor, self.patch) > (other.major, other.minor, other.patch)

def validate(fp:str, schema:dict, type:str='json') -> tuple[bool, dict]:
    """
    Tests if instances passes the schema.

    Arguments
    ---
    `fp` - Path to the JSON file to open and validate.

    `schema` - The JSON schema to validate with.

    `type` - The type of validation. json, yaml

    Returns
    `tuple` - Returns a 2 length tuple. The first value is whether it passed the test. The second is the parsed isntance.
    """
    if os.path.isfile(fp):
        with open(fp, 'r') as r:
            try:
                match type.lower():
                    case 'json':  instance = json.load(r)
                    case 'yaml': 
                        import yaml
                        instance = yaml.safe_load(r)
                    case _:
                        raise KeyError(f"'{type}' is not a supported validation type. Must be json or yaml")
                jsonschema.validate(instance, schema)
                return (True, instance)
            except json.JSONDecodeError as err:
                logger.warning(f"'{fp}' DecodeError: {err}")

            except jsonschema.ValidationError as err:
                pos = ''
                index=0
                for p in err.absolute_path:
                    if isinstance(p, int): pos+=f'[{p}]'
                    else:
                        if index!=0: pos+='.'
                        pos+=str(p)
                    index+=1
                att = f" at '{pos}'"
                if pos=='': att = ''
                logger.warning(f"'{fp}' ValidationError: {err.message}"+att)

            except Exception as err:
                logger.warning(f"'{fp}' {err}: {err}")

    return (False, None)

# DEPRIVED use App.mimetype
def mimetype(type:str, subtype:str=None):
    def decorator(func):
        return getApp().add_mimetype(func, type, subtype)
    return decorator

def to_json_type(v):
    if v == dict: return 'object'
    elif v == list: return 'array'
    elif v == str: return 'string'
    elif v == int: return 'integer'
    elif v == float: return 'number'
    elif v == bool: return 'boolean'
    elif v == inspect._empty: return None
    elif isinstance(v, ResourcePath):
        return 'string'
    logger.info(f"Could not convert annotation type to JSON '{v}'")
    return None

def schema(node, cls_or_func, traits:list, child:bool=False, skiparg:int=-1) -> dict:
    """
    Creates a jsonschema from a class or function.

    Arguments
    ---
    `node` - The jsonpack._node.

    `cls_or_func` - A class or function to create a jsonschema from.

    `traits` - A list of traits for this schema. components, events, images.

    `child` - Whether or not this is a child event.

    `skiparg` - Argument index to skip. (used to skip the first CONTEXT arg for nodes and events).
    """
    app = getApp()
    result = {
        '$schema': 'http://json-schema.org/draft-07/schema',
        'type': 'object',
        'required': [],
        'properties': {},
        'patternProperties': {
            '^\\$': True
        },
        'additionalProperties': False
    }
    if child:
        result = {
            'type': 'object',
            'required': [],
            'properties': {},
            'additionalProperties': False
        }
    para = inspect.signature(cls_or_func).parameters
    i = 0
    for k, v in para.items():
        if i != skiparg:
            result['properties'][k] = {}
            prop = result['properties'][k]

            if v.default == inspect._empty: result['required'].append(k)

            type = to_json_type(v.annotation)
            if type is not None:
                prop['type'] = type
                match type:
                    case 'object':
                        prop['properties'] = {}
                        prop['additionalProperties'] = False
                    case 'array':
                        prop['items'] = {}
                    

            if 'components' in traits and k=='components':
                if isinstance(node, _node) and prop['type'] == 'object':
                    for k,v in node.__components__.items():
                        prop['properties'][str(k)] = v.schema

            if 'events' in traits and k=='events':
                prop['additionalProperties'] = {
                    'type': 'object',
                    'properties': {},
                    'additionalProperties': False
                }
                for k,v in app.events.items():
                    prop['additionalProperties']['properties'][str(k)] = v.schema
            
        i+=1
    # Get all args
    return result
