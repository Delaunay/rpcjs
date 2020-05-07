RPC js
======

A lightweight dashboard framework built on top of Flask.


Life time of a Request
~~~~~~~~~~~~~~~~~~~~~~

1. User sends HTTP request to server
2. Server receives requests
    * Queues work on the worker pool
    * Returns empty page to be filled

3. User sees page, pending some portion loading
4. Work is finished, it is passed to the server through SocketIO
5. Server forward the result to the client through SocketIO
6. User can interact with the full page
7. Javascript events are forwarded to the server through SocketIO
8. Server can reply to events through SocketIO

