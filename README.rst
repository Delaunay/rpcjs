RPC js
======




Life time of a Request
~~~~~~~~~~~~~~~~~~~~~~

* User sends HTTP request to server
* Server receives requests
    * Queues work on the worker pool
    * Returns empty page to be filled
* User sees page, pending some portion loading
* Work is finished, it is passed to the server through SocketIO
* Server forward the result to the client through SocketIO
* User can interact with the full page
* Javascript events are forwarded to the server through SocketIO
* Server can reply to events through SocketIO

