"""Handles javascript remote function calls"""

_socketio = None
_socketio_ready = False


def set_socketio(socket):
    global _socketio
    _socketio = socket


def socketio():
    return _socketio


def register_event(event, handler, namespace='/'):
    """Register a socketio event to a python handler

    Parameters
    ----------
    event: str
        Name of the event

    handler: call
        Function to call when the event is fired
    """
    return socketio().on(event, namespace)(handler)


_pending_bind = []
_pending_attr = []


def set_attribute(id, attribute, value):
    """Set the attribute of an element on the webpage

    Parameters
    ----------
    id: str
        id of the DOM element

    attribute: str
        name of the attribute to set

    value: json
        new value of the attribute
    """
    if not _socketio_ready:
        _pending_bind.append((id, attribute, value))

    debug(f'set_attribute {attribute} of {id}')

    socketio().emit('set_attribute', dict(
        id=id,
        attribute=attribute,
        value=value
    ))


def get_element_size(id, callback):
    """Get the size of an element inside the webpage

    Parameters
    ----------
    id: str
        id of the DOM element

    callback: Call
        Function to call with the size information `{width: w, height: h}`
    """
    debug(f'get_element_size of {id}')
    socketio().emit('get_size', dict(
        id=id
    ))
    register_event(f'get_size_{id}', callback)


def bind(id, event, handler, attribute=None, property=None):
    """Bind an element event to a handler and return a property of an attribute of the element

    Parameters
    ----------
    id: str
        id of the DOM element

    event: str
        Name of the event we are listening too.
        The full list of supported events can be found `here <https://www.w3schools.com/jsref/dom_obj_event.asp>`_.

    handler: call
        function to callback when the event is fired

    attribute: str
        Attribute of the element to return

    property: str
        Property of the element to return
    """
    if not _socketio_ready:
        _pending_bind.append((id, event, handler, attribute, property))

    debug(f'binding `{id}` with `{event}` to `{handler}`')
    # ask javascript to listen to events for a particular kind of event on our element
    socketio().emit('bind', {'id': id, 'event': event, 'attribute': attribute, 'property': property})
    # when the event happen js will send us back the innerHTML of that element
    register_event(f'bind_{event}_{id}', handler)
    return


def handshake_event():
    """Called when socketIO connects to the server"""
    global _socketio_ready, _pending_attr, _pending_bind

    _socketio_ready = True
    info('SocketIO connected')

    if _pending_attr:
        for arg in _pending_attr:
            set_attribute(*arg)

        _pending_attr = []

    if _pending_bind:
        for arg in _pending_bind:
            bind(*arg)

        _pending_bind = []


def disconnect_event():
    """Called when socketIO disconnects from the server"""
    global _socketio_ready
    _socketio_ready = False
    info('SocketIO disconnected')
