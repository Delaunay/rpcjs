"""HTML elements that are binded to python through javascript remote function calls"""
import time
import threading
import json
import io
import logging

from .elements import select_dropdown as static_select
from .elements import text_input as static_text_input, div

from .dashboard import host, port
from .binding import bind, send_new_data_vega, display_vega
from .events import Events
from .utils import make_remote_call


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
    return 'F' + uid


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
        try:
            set_promise(options[value])
        except IndexError:
            set_promise(value)

    cb = index_to_options
    if len(options) == 0:
        cb = set_promise

    bind(id, 'change', cb, property='selectedIndex')
    return FutureValue(id), select_html


def text_input(placeholder='', callback=None, id=None):
    id = _gen_sym(id)
    input_html = static_text_input(placeholder, id)
    bind('study_prefix', 'change', set_symbol_callback(id, callback), property='value')
    return FutureValue(id), input_html


class ThreadFlag:
    def __init__(self):
        self.running = True


RUNNING = None


def stop_update_thread():
    global RUNNING

    # set the flag of the previous thread to false
    if RUNNING is not None:
        RUNNING.running = False

    # Make a new flag for the new thread
    RUNNING = ThreadFlag()
    return RUNNING


def streaming_iterator(id: str, name: str, callback, delay=1):
    """

    Parameters
    ----------
    id: str
        DOM id of the plot

    name: str
        Name of the dataset the data is appended to

    callback: Callable
        Function that returns an iterator with the data to append

    delay: int
        Sleep time in second before sending data to the browser

    Notes
    -----

    Only on update thread can exist at any given time.
    If a new thread is spawn the old one will exit.
    """
    from datetime import datetime

    def to_dict(a):
        if isinstance(a, datetime):
            return a.timestamp()

        raise TypeError(f'type {type(a)} not json serializable')

    def run():
        time.sleep(delay)

        import socketio
        socket = socketio.Client()
        socket.connect(f'http://{host()}:{port()}')

        flag = stop_update_thread()
        for fragment in callback():
            # Get rid of non jsonable stuff
            good_json = json.loads(json.dumps(fragment, default=to_dict))

            socket.emit(event='remote_process_result', data=make_remote_call(
                send_new_data_vega, id, name, good_json))

            if not flag.running:
                break

    t = threading.Thread(target=run)
    t.start()


def realtime_altair_plot(chart, generator, id=None, dataset_name=None):
    import altair as alt

    if dataset_name is None:
        dataset_name = 'table'

    if id is None:
        id = _gen_sym(id)

    chart.data = alt.Data(name=dataset_name)
    buffer = io.StringIO()
    chart.save(buffer, 'json')
    json_spec = json.loads(buffer.getvalue())

    # Send the spec to javascript
    display_vega(id, json_spec)

    # Start sending data to the browser
    streaming_iterator(id, dataset_name, generator)

    # reply a dummy div that will hold the chart
    return div(id=id)
