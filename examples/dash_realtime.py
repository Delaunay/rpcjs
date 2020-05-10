import altair as alt
from vega_datasets import data

from rpcjs.dashboard import Dashboard, host, port
import rpcjs.elements as html
from rpcjs.page import Page
import rpcjs.binding as js
from rpcjs.utils import make_remote_call

import time
import threading
import json
import io
from datetime import datetime

source = data.cars()
columns = list(source.columns)


def to_dict(a):
    if isinstance(a, datetime):
        return a.timestamp()

    raise TypeError(f'type {type(a)} not json serializable')


def stream_data(id, name):

    def stream():
        import socketio
        socket = socketio.Client()
        socket.connect(f'http://{host()}:{port()}')

        time.sleep(1)

        for row in source.to_dict('records'):
            print(row)
            socket.emit(event='remote_process_result', data=make_remote_call(
                js.send_new_data_vega, id, name, json.dumps([row], default=to_dict)
            ))
            time.sleep(0.5)

    return stream


class MySimplePage(Page):
    def routes(self):
        return ['/']

    def main(self):
        xlabel, ylabel = 'Horsepower', 'Miles_per_Gallon'

        data = alt.Data(name='table')
        chart = alt.Chart(data).mark_circle().encode(
            alt.X(xlabel, type='quantitative'),
            alt.Y(ylabel, type='quantitative'),
            color='Origin:N'
        ).properties(
            width=500,
            height=500
        ).interactive()

        buffer = io.StringIO()
        chart.save(buffer, 'json')
        json_spec = json.loads(buffer.getvalue())
        js.display_vega('my_plot', json_spec)

        print(json.dumps(json_spec, indent=2))
        t = threading.Thread(target=stream_data('my_plot', 'table'))
        t.start()

        return html.div(id='my_plot')


if __name__ == '__main__':
    # To see the list of columns
    #   go to http://127.0.0.1:5000/
    with Dashboard(__name__) as dash:
        dash.add_page(MySimplePage())
        dash.run()
