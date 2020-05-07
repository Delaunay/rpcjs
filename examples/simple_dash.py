import altair as alt
from vega_datasets import data

from rpcjs.dashboard import Dashboard
from rpcjs.page import Page
import rpcjs.elements as html


source = data.cars()
columns = list(source.columns)


class MySimplePage(Page):
    def routes(self):
        return [
            '/',
            '/<string:xlabel>/<string:ylabel>'
        ]

    def main(self, xlabel=None, ylabel=None):
        # if the xlabel is not set print the different options
        if xlabel is None or ylabel is None:
            return html.ul(columns)

        return html.altair_plot(
            alt.Chart(source).mark_circle().encode(
                alt.X(xlabel, type='quantitative'),
                alt.Y(ylabel, type='quantitative'),
                color='Origin:N'
            ).properties(
                width=500,
                height=500
            ).interactive())


if __name__ == '__main__':
    # To see the list of columns
    #   go to http://127.0.0.1:5000/

    # To visualize the graph
    #   go to http://127.0.0.1:5000/Miles_per_Gallon/Cylinders

    with Dashboard(__name__) as dash:
        dash.add_page(MySimplePage())
        dash.run()
