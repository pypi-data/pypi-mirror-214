import os
import importlib
from typing import List, Any
from collections import defaultdict
# from osintbuddy.utils import slugify
from osintbuddy.elements.base import BaseNode
from osintbuddy.errors import OBPluginError
from osintbuddy.utils import to_snake_case


class OBRegistry(type):
    plugins = []
    labels = []
    ui_labels = []

    def __init__(cls, name, bases, attrs):
        """
        Initializes the OBRegistry metaclass by adding the plugin class
        and its label if it is a valid plugin.
        """
        if name != 'OBPlugin' and name != 'Plugin' and issubclass(cls, OBPlugin):
            label = cls.label.strip()
            if cls.show_label is True:
                OBRegistry.ui_labels.append(label)
            else:
                OBRegistry.ui_labels.append(None)
            OBRegistry.labels.append(label)
            OBRegistry.plugins.append(cls)

    @classmethod
    async def get_plugin(cls, plugin_label: str):
        """
        Returns the corresponding plugin class for a given plugin_label or
        'None' if not found.

        :param plugin_label: The label of the plugin to be returned.
        :return: The plugin class or None if not found.
        """
        for idx, label in enumerate(cls.labels):
            if label == plugin_label:
                return cls.plugins[idx]
        return None

    def __getitem__(self, i):
        return self.get_plugin[i]


def discover_plugins(
    dir_path: str = '/plugins.osintbuddy.com/src/osintbuddy/core/',
):
    """
    Scans the specified 'dir_path' for '.py' files, imports them as plugins,
    and populates the OBRegistry with classes.

    :param dir_path: The directory path where the plugins are located.
    :return: List of plugin classes
    """
    for r, _, files in os.walk(dir_path):
        for filename in files:
            modname, ext = os.path.splitext(filename)
            if ext == '.py':
                try:
                    modpath = r.replace("/app/", "")
                    if 'osintbuddy/core' in dir_path:
                        modpath = r.replace("/plugins.osintbuddy.com/src/", "")
                    modpath = modpath.replace("/", ".")
                    importlib.import_module(f'{modpath}{modname}')
                except ImportError as e:
                    print(f"Error importing plugin '{modpath}{modname}': {e}")

    return OBRegistry.plugins


def transform(label, icon='list', prompt=None):
    """
    A decorator add transforms to an osintbuddy plugin.

    Usage:
    @transform(label=<label_text>, icon=<tabler_react_icon_name>)
    def transform_to_ip(self, node, **kwargs):
        # Method implementation

    :param label: str, A string representing the label for the transform
        method, which can be utilized for displaying in the context menu.
    :param icon: str, Optional icon name, representing the icon associated
        displayed by the transform label. Default is "list".
    :return: A decorator for the plugin transform method.
    """
    def decorator_transform(func):
        async def wrapper(self, node, **kwargs):
            return await func(self=self, node=node, **kwargs)
        wrapper.label = label
        wrapper.icon = icon
        if prompt is not None:
            wrapper.prompt = prompt

        return wrapper
    return decorator_transform


class OBPlugin(object, metaclass=OBRegistry):
    """
    OBPlugin is the base class for all plugin classes in this application.
    It provides the required structure and methods for a plugin.
    """
    node: List[BaseNode]
    name: str = 'Plugin Node'
    color: str = '#145070'
    label: str = ''
    icon: str = 'atom-2'
    transform_icons: dict = {}
    show_label = True
    style: dict = {}

    def __init__(self):
        transforms = self.__class__.__dict__.values()
        self.transforms = {
            func.label: func for func in transforms if hasattr(func, 'label')
        }
        self.transform_labels = [
            {'label': func.label, 'icon': func.icon} for func in transforms
            if hasattr(func, 'icon') and hasattr(func, 'label')
        ]

    def __call__(self):
        return self.blueprint()

    @staticmethod
    def _map_node_elements(element, kwargs):
        label = to_snake_case(element['label'])
        for passed_label in kwargs:
            if passed_label == label:
                if type(kwargs[label]) is str:
                    element['value'] = kwargs[label]
                elif type(kwargs[label]) is dict:
                    for t in kwargs[label]:
                        element[t] = kwargs[label][t]
        return element

    @classmethod
    def blueprint(cls, **kwargs):
        """
        Generate and return a dictionary representing the plugins node.
        Includes label, name, color, icon, and a list of all elements
        for the node/plugin.
        """
        node = defaultdict(None)
        node['label'] = cls.label
        node['name'] = cls.name
        node['color'] = cls.color
        node['icon'] = cls.icon
        node['style'] = cls.style
        node['elements'] = []
        for element in cls.node:
            if type(element) is list:
                e = []
                for elm in element:
                    e.append(cls._map_node_elements(elm.json(), kwargs))
                node['elements'].append(e)
            else:
                e = cls._map_node_elements(element.json(), kwargs)
                node['elements'].append(e)
        return node

    async def _get_transform(self, transform_type: str, node, **kwargs) -> Any:
        """ Return output from a function accepting node data.
            The function will be called with a single argument, the node data
            from when a node context menu action is taken - and should return
            a list of Nodes.
            None if the plugin doesn't provide a transform
            for the transform_type.
        """
        if self.transforms and self.transforms[transform_type]:
            try:
                transform = await self.transforms[transform_type](
                    self=self,
                    node=node,
                    **kwargs
                )
                if type(transform) != list:
                    return [transform]
                return transform
            except OBPluginError as e:
                raise OBPluginError(e)
        return None
