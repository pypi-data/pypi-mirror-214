import jsonpack

class NodeProxy:
    def __init__(self, layer: dict):
        self.__dict__.update(layer)

    def __len__(self) -> int:
        return len(self.__dict__)

    def __repr__(self) -> str:
        inner = ', '.join((f'{k}={v!r}' for k, v in self.__dict__.items() if not k.startswith('_')))
        return f'NodeProxy({inner})'

    def __getattr__(self, attr: str) -> None:
        return None

    def __eq__(self, other: object) -> bool:
        return isinstance(other, NodeProxy) and self.__dict__ == other.__dict__
    
class Node(object):
    """
    Helper class used for creating nodes.

    Methods
    ---
    to_dict, from_dict, on_load, on_unload, __str__
    """
    traits = {}
    __slots__ = []
    __file__ = None

    def __init__(self):
        self._app = None

    def to_dict(self):
        """
        Converts a :class:`Node` to a :class:`dict`
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
        Converts a :class:`dict` to a :class:`Node`
        """
        self = cls.__new__(cls)
        
        for n,v in data.items():
            setattr(self, n, v)

        # try to fill in the more rich fields

        for attr in self.__slots__:
            if attr[0] == '_':
                n = attr[1:]
                try:
                    value = data[n]
                except KeyError:
                    continue
                else:
                    setattr(self, n, value)
        return self

    def on_load(self, ctx):
        """
        Should be overridden. Triggers when this node is loaded.
        """
        pass

    def on_unload(self, ctx):
        """
        Should be overridden. Triggers when this node is unloaded.
        """
        pass

    def __str__(self):
        inner = ', '.join((f'{k}={v!r}' for k, v in self.__class__.__dict__.items() if not k.startswith('_')  ))
        return f'{self.__class__.__name__}({inner})'

class Componentable(object):
    """
    Helper class used for creating nodes with dynamic components.

    Arguments
    ---
    `components` - All components for this node.

    Methods
    ---
    get_component, trigger_component
    """
    @property
    def components(self) -> NodeProxy:
        return NodeProxy(getattr(self, '_components', {}))

    @components.setter
    def components(self, value):
        if isinstance(value, dict):
            self._components = value
        else:
            raise TypeError(f'Expected dict but received {value.__class__.__name__} instead.')
            
    def get_component(self, name:str) -> NodeProxy:
        """
        Returns the component.

        Argumnets
        ---
        `name` - Name of the component to get.
        """
        res = self._components.get(name)
        if res is not None: return NodeProxy(res)

    def trigger_component(self, name:str, **extra):
        """
        Returns the result of the component function when called.

        Arguments
        ---
        `name` - Name of the component to call.

        **extra - Extra arguments to pass to the component.
        """
        node = self._app.get_node(self)
        com = node.__components__.get(name)
        kw = self._components.get(name)
        if com is not None and kw is not None:
            return com.call(kw, extra)
            
class Eventable(object):
    """
    Helper class used for creating nodes with dynamic events.

    Arguments
    ---
    `events` - All events for this node.

    Methods
    ---
    add_event, remove_event, clear_events, event, trigger_event
    """

    @property
    def events(self) -> dict:
        result = {}
        res = getattr(self, '_events', {})
        for k, v in res.items():
            result[k] = NodeProxy(v)
        return result
    
    @events.setter
    def events(self, value):
        if isinstance(value, dict):
            self._events = value
        else:
            raise TypeError(f'Expected dict but received {value.__class__.__name__} instead.')

    def add_event(self, name:str, **kw):
        """
        Adds an event to the node.
        
        Arguments
        ---
        `name` - Name of the event to create.
        """
        try:
            self._events[name] = kw
        except AttributeError:
            self._events = {name: kw}

        return self

    def remove_event(self, name:str):
        """
        Removes an event at a specified name.

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
        Removes all events from this node.
        """
        try:
            self._events.clear()
        except AttributeError:
            self._events = {}
        return self

    def get_event(self, name:str) -> NodeProxy:
        """
        Get the event from the name.

        Arguments
        ---
        `name` - Name of the event to get.
        """
        return self.events.get(name)

    def trigger_event(self, name:str):
        """
        Runs this event from the name.

        Arguments
        ---
        `name` - Name of the event to run.
        """
        res = self.event(name)
        if res is not None:
            for k, v in res.__dict__.items():
                event:jsonpack._event = self._app.events.get(k)
                if event is not None:
                    event.call(v)
        else:
            jsonpack.logger.warning(f"'{self.__file__}': Event '{name}' does not exist!")
        return self
