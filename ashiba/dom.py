import re
import json
import copy
import collections
from ashiba import utils

class GenericDomElement(dict):
    def __init__(self, *args, **kwargs):
        super(GenericDomElement, self).__init__(*args, **kwargs)
        if self.get('_meta') is None:
            self['_meta'] = {}
    
    def __getitem__(self, key):
        try:
            return super(GenericDomElement, self).__getitem__(key)
        except KeyError:
            return None
    
    def __repr__(self):
        return "{}({})".format(self.__class__.__name__,
                               dict(self.items()))
    
    def inner_html(self):
        return None

    def add_class(self, class_name):
        if class_name not in self['_meta'].setdefault('class', []):
            self['_meta']['class'].append('+' + class_name)

    def remove_class(self, class_name):
        self['_meta'].setdefault('class', []).append('-' + class_name)

    def style(self, prop=None, val=None):
        if prop is None:
            return self['_meta'].get('style', {})
        elif val is None:
            return self['_meta'].get('style', {}).get(prop)
        else:
            self['_meta'].setdefault('style', {})[prop] = val

    @classmethod
    def from_dict(cls, in_dict):
        return cls(in_dict)
    
    @classmethod
    def from_json(cls, in_json):
        return cls.from_dict(json.loads(in_json))
    
    def to_dict(self):
        inner_html = self.inner_html()
        if inner_html:
            self['_meta']['innerHTML'] = inner_html
        return dict(self)
    
    def to_json(self):
        return json.dumps(self.to_dict)

_translate_node_name = {}

def DomElement(node_name, *args, **kwargs):
    base_dict = dict(*args, **kwargs)
    cls = None
    if node_name.lower() in _translate_node_name:
        cls = _translate_node_name[node_name.lower()]
    else:
        for class_name in base_dict.get('_meta', {}).get('class', []):
            if class_name in _translate_node_name:
                cls = _translate_node_name[class_name]
                break
        else:
            cls = GenericDomElement

    obj = cls(*args, **kwargs)
    if node_name:
        obj['_meta']['nodeName'] = node_name
    return obj

def nodeName(node_name):
    def decorator(cls):
        _translate_node_name[node_name.lower()] = cls
        return cls
    return decorator

@nodeName('SELECT')
class Select(GenericDomElement):
    """
    A dropdown box. Add items to the dropdown with add_item/add_items.
    
    Recommended events to bind:
        change
    """
    # Superclass methods
    def __init__(self, *args, **kwargs):
        super(Select, self).__init__(*args, **kwargs)
        # Could probably be replaced with attr later
        self._list_items = []
        list_item_template = '<option value=["\'](.*?)["\']>(.*?)</option>'
        self._list_items = re.findall(list_item_template,
                                      self['_meta']['innerHTML'])
        
    def inner_html(self):
        list_item_template = '<option value="{}">{}</option>'
        inner_html = ""
        for pair in self._list_items:
            inner_html += list_item_template.format(*pair)
        return inner_html
    
    # Non-superclass methods
    def add_item(self, value, text=None):
        """
        Add an item to the dropdown.
        Args:
            value: This is the value that the select object will take on.
            text : (Optional) This is the display text.
        Example:
        >>> s.add_item('benz', 'Mercedes Benz')
        """
        if isinstance(value, (list, tuple)):
            if len(value) == 2:
                value, text = value
            elif len(value) == 1:
                value = text = value[0]
            else:
                raise TypeError("add_item takes at most 2 values (%i given)" \
                                % len(value))
        elif text is None:
            text = value
        self._list_items.append((value, text))
        
    def add_items(self, items):
        """
        Add multiple items to a dropdown. Accepts a list of items, either
        singletons or pairs.
        Example:
        >>> s.add_items([('benz', 'Mercedes Benz'), 'ford'])
        """
        for item in items:
            self.add_item(item)
    
    def empty(self):
        """
        Remove all items from the dropdown.
        """
        self._list_items = []
    
    def remove_item(self, value):
        """
        Remove an item from the dropdown list by specifying its value.
        This will fail silently if that item is not in the list.
        """
        self._list_items = [x for x in self._list_items if x[0] != value]
        
    def list_items(self):
        return self._list_items

@nodeName('jqui-dialog')
class Dialog(GenericDomElement):
    def __init__(self, *args, **kwargs):
        super(Dialog, self).__init__(*args, **kwargs)

    @property
    def title(self):
        return self.get('title', '')

    @title.setter
    def title(self, t):
        self['title'] = t

    @property
    def body(self):
        return self['_meta'].get('innerHTML', '')

    @body.setter
    def body(self, b):
        self['_meta']['innerHTML'] = b

class Dom(collections.defaultdict):
    def __init__(self, *args, **kwargs):
        super(Dom, self).__init__(lambda: DomElement(''), *args, **kwargs)
        for k in self:
            self[k] = DomElement(self[k]['_meta']['nodeName'], self[k])
        # Should this be in the to_dict method?
        self.init_state = copy.deepcopy(self.to_dict())
        
    def __repr__(self):
        return "Dom(%s)" % dict(self.items())

    def changes(self):
        cur_state = self.to_dict()
        return utils.dict_diff(cur_state, self.init_state)

    def to_dict(self):
        return {k:v.to_dict() for k,v in self.items()}
