"""HTML elements that are binded to python through javascript remote function calls"""
import rpcjs.elements as html
from rpcjs.attributes import Attributes
from rpcjs.events import Events

# Global symbol that holds future value
global_symbol = dict()
symbol_size = 16


# Generate a unique symbol to identify a DOM element
def _gen_sym():
    import uuid
    global symbol_size, global_symbol

    uid = uuid.uuid4().hex[:symbol_size]
    if uid in global_symbol:
        symbol_size += 1
        return _gen_sym()

    global_symbol[uid] = None
    return uid


# Set the value of a DOM element after a js callback
def set_symbol_callback(name):
    def set_symbol(value):
        global global_symbol
        global_symbol[value] = name

    return set_symbol


# Future like class that returns the value of a DOM element
class Value:
    def __init__(self, uid, default=None):
        self.uid = uid
        self.default = default

    def get(self):
        global global_symbol
        return global_symbol.get(self.uid, None)


# Represent a select input form and the value it is holding
class _Select(Value):
    class properties:
        selected_index = 'selectedIndex'

    def __init__(self, uid, html, default=None):
        super(_Select, self).__init__(uid, default)
        self.html = html

    def selected_index(self):
        """Return the index selected by the select form"""
        return self.get()

    def __str__(self):
        return self.html

    def __html__(self):
        return self.html


def select_dropdown(options):
    """

    Returns
    -------
    value: Future
        future value of the index that is going to be select by the user

    html: str
        the html of the form you need to send to the users
    """
    from rpcjs.dash import bind

    uid = _gen_sym()
    html_from = html.select_dropdown(options, uid)
    bind(uid, Events.change, set_symbol_callback(uid), property=_Select.properties.selected_index)
    return _Select(uid, html_from)
