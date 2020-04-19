from flask import Flask
from flask_socketio import SocketIO

from rpcjs.binding import set_socketio, handshake_event, disconnect_event


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

    def run(self):
        """Run the flask App"""
        return self.socket.run(self.app)

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
        self.socket.on(event, namespace)(handler)

