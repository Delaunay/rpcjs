"""HTML elements that are binded to python through javascript remote function calls"""
import logging

from .elements import select_dropdown as static_select
from .elements import text_input as static_text_input

from .binding import bind
from .events import Events

# Global symbol that holds future value
global_symbol = dict()
symbol_size = 16

log = logging.Logger(__name__)


# Generate a unique symbol to identify a DOM element
def _gen_sym(uid=None):
    import uuid
    global symbol_size, global_symbol

    if uid is None:
        uid = uuid.uuid4().hex[:symbol_size]

    if uid in global_symbol:
        symbol_size += 1
        return _gen_sym()

    global_symbol[uid] = None
    return uid


# Set the value of a DOM element after a js callback
def set_symbol_callback(name, callback):
    def set_symbol(value):
        global global_symbol
        global_symbol[name] = value

        if callback is not None:
            callback()

    return set_symbol


# Future like class that returns the value of a DOM element
class FutureValue:
    def __init__(self, uid, default=None):
        self.uid = uid
        self.default = default

    def get(self):
        global global_symbol
        return global_symbol.get(self.uid, None)


def select_dropdown(options, callback=None, id=None):
    id = _gen_sym(id)
    select_html = static_select(options, id)

    set_promise = set_symbol_callback(id, callback)

    def index_to_options(value):
        set_promise(options[value])

    bind(id, 'change', index_to_options, property='selectedIndex')
    return FutureValue(id), select_html


def text_input(placeholder='', callback=None, id=None):
    id = _gen_sym(id)
    input_html = static_text_input(placeholder, id)
    bind('study_prefix', 'change', set_symbol_callback(id, callback), property='value')
    return FutureValue(id), input_html
