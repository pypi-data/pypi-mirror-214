## Make very simple bokeh app and display it.

from bokeh.plotting import figure, show

from bokeh.io import save, show
from bokeh.io import output_file
from bokeh.layouts import column, layout, row
from bokeh.models import Column, CustomJS, Div, Select, Slider

import sys

from xplorts.slideselect import SlideSelect


def ww_test(options=["A", "B", "C"], title="Selection"):
    option_keys = options
    bk_select = Select(options=option_keys, value=option_keys[0], title=title)
    bk_slider = Slider(start=0, end=len(options)-1, value=0, step=1, title=None)

    # Link select option to slider value.
    bk_select.js_on_change('value',
        CustomJS(args={"other": bk_slider},
                 code="other.value = this.options.indexOf(this.value) \n" \
                     + "console.log('Linking select to slider, ' + this.value + ' => ' + other.value)"
        )
    )

    # Link slider value to select option.
    bk_slider.js_on_change('value',
        CustomJS(args={"other": bk_select},
                 code="other.value = other.options[this.value] \n" \
                     + "console.log('Linking slider to other, ' + this.value + ' => ' + other.value)"
        )
    )

    children = [
        bk_select,
        bk_slider
    ]

    # Make a bokeh layout, and coerce the class type.
    obj = column(children=children)  # Force consistent child sizing.
    show(obj)


def widget_test():
    ss = SlideSelect(options=["a", "b", "c"])

    result = Div(
        text="""
            <p>?</p>
            """,
        width=200,
        height=30,
    )
    ss.js_link("value", result, "text")

    show(row(ss, result))


def main():
    print("hi")

    # some data
    x = [1, 2, 3, 4, 5]
    y = [6, 7, 2, 4, 5]

    output_file("tt.html", title="Test plot", mode='inline')

    # create a new plot with a title and axis labels
    p = figure(title="Simple line example", x_axis_label='x', y_axis_label='y')

    # add a line renderer with legend and line thickness to the plot
    p.line(x, y, legend_label="Temp.", line_width=2)
    show(p)

    return 0

sys.exit(widget_test())
