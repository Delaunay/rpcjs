from flask import Flask
from flask_socketio import SocketIO

from threading import Thread
from multiprocessing import Process, Pool

from .binding import set_socketio, handshake_event, disconnect_event
from .utils import exec_remote_call

import traceback
import logging
log = logging.Logger(__name__)


_host = None
_port = None
_pool = None


def host():
    return _host


def port():
    return _port


def _decorated_mp(host, port, fun, *args, **kwargs):
    import socketio

    r = None
    exception = None
    try:
        r = fun(*args, **kwargs)
    except:
        exception = traceback.format_exc()

    if 'module' in r and 'function' in r:
        # make a client to the flask server
        socket = socketio.Client()
        try:
            socket.connect(f'http://{host}:{port}')

            if r is not None:
                socket.emit(event='remote_process_result', data=r)

            if exception is not None:
                socket.emit(event='remote_process_error', data=exception)

        except:
            exception = traceback.format_exc()
            socket.emit(event='remote_process_error', data=exception)

    else:
        log.error(f'(result: {r}) is is not a remote call')


def async_thread_call(fun, *args, **kwargs):
    """Runs a function async and execute the resulting remote function call"""
    t = Thread(
        target=_decorated_mp,
        args=(host(), port(), fun) + args,
        kwargs=kwargs)

    t.start()
    return t


def async_process_call(fun, *args, **kwargs):
    p = Process(
        target=_decorated_mp,
        args=(host(), port(), fun) + args,
        kwargs=kwargs)

    p.start()
    return p


def async_call(fun, *args, **kwargs):
    if _pool is not None:
        return _pool.apply_async(
            _decorated_mp,
            args=(host(), port(), fun) + args,
            kwds=kwargs)
    else:
        log.error('Pool was not created, restart your server')


def handle_error(msg):
    print(msg)


class Dashboard:
    """Dashboard entry point"""
    def __init__(self, name=__name__, secret='__secret__'):
        import os
        self.app = Flask(name, static_folder=os.path.join(os.path.dirname(__file__), 'static'))
        self.app.debug = True
        self.app.config['SECRET_KEY'] = secret
        self.socket = SocketIO(self.app)
        self.routes = []

        set_socketio(self.socket)
        self.on_event('handshake', handshake_event)
        self.on_event('disconnect', disconnect_event)
        self.on_event('remote_process_result', exec_remote_call)
        self.on_event('remote_process_error', handle_error)

    @staticmethod
    def init_worker():
        # Make the worker ignore KeyboardInterrupts
        # since the master process is going to do the cleanup
        import signal
        signal.signal(signal.SIGINT, signal.SIG_IGN)

    def __enter__(self):
        global _pool
        _pool = Pool(4, self.init_worker)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if _pool is not None:
            _pool.close()
            _pool.terminate()

    def run(self, host='127.0.0.1', port=5000):
        """Run the flask App"""
        global _host, _port

        _port = port
        _host = host
        return self.socket.run(self.app, host, port)

    def add_page(self, page, route=None, header=None, **kwargs):
        """Add a new page to the dashboard

        Parameters
        ----------
        page: Page
            page object

        route: str
            Route specification to reach the page
            Will default to the page route if left undefined

        header: str
            HTML header to insert onto the page
        """
        route = route or page.routes()

        if not isinstance(route, list):
            route = [route]

        for r in route:
            self.routes.append((r, type(page).__name__))
            self.app.add_url_rule(r, type(page).__name__, page, **kwargs)

        if header is not None:
            page.header = header

    def on_event(self, event, handler, namespace='/'):
        """Register an handler for a givent event"""
        assert callable(handler)
        self.socket.on(event, namespace)(handler)

