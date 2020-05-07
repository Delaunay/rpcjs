import altair as alt
from vega_datasets import data

from rpcjs.dashboard import Dashboard
import rpcjs.elements as html
from rpcjs.page import Page


source = data.cars()
columns = list(source.columns)


def make_plot(xlabel, ylabel):
    return alt.Chart(source).mark_circle().encode(
        alt.X(xlabel, type='quantitative'),
        alt.Y(ylabel, type='quantitative'),
        color='Origin:N'
    ).properties(
        width=500,
        height=500
    ).interactive()


class MySimplePage(Page):
    def routes(self):
        return ['/']

    def main(self):
        # if the xlabel is not set print the different options
        return html.async_altair_plot(make_plot, 'Horsepower', 'Miles_per_Gallon')


if __name__ == '__main__':
    # To see the list of columns
    #   go to http://127.0.0.1:5000/
    with Dashboard(__name__) as dash:
        dash.add_page(MySimplePage())
        dash.run()
