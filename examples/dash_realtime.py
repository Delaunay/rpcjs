import altair as alt
from vega_datasets import data

from rpcjs.dashboard import Dashboard
from rpcjs.page import Page
from rpcjs.binded import realtime_altair_plot

source = data.cars()


def streamed_car():
    import time
    time.sleep(1)

    streamed = source.to_dict('records')
    for row in streamed:
        time.sleep(0.25)
        yield row


class MyRealTimePage(Page):
    def routes(self):
        return ['/']

    def main(self):
        xlabel, ylabel = 'Horsepower', 'Miles_per_Gallon'

        chart = alt.Chart(source).mark_circle().encode(
            alt.X(xlabel, type='quantitative'),
            alt.Y(ylabel, type='quantitative'),
            color='Origin:N'
        ).properties(
            width=500,
            height=500
        ).interactive()

        return realtime_altair_plot(chart, streamed_car)


if __name__ == '__main__':
    # To see the list of columns
    #   go to http://127.0.0.1:5000/
    with Dashboard(__name__) as dash:
        dash.add_page(MyRealTimePage())
        dash.run()
