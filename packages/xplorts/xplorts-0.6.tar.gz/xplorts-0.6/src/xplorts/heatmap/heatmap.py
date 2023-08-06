"""
Make standalone interactive heatmaps for categorical time series data

Functions
---------
grouped_heatmap
    Add a heatmap to a figure, with color map and hover tooltip.
"""
# See https://docs.bokeh.org/en/latest/docs/user_guide/topics/categorical.html#heatmaps


#%%

from math import pi
import pandas as pd

from bokeh.models import BasicTicker, PrintfTickFormatter
from bokeh.plotting import figure
from bokeh.transform import linear_cmap

## Imports from this package
from ..base import (add_hover_tool, extend_legend_items)

#%%

def heatmap(data,
            x,
            y,
            values,
            *,
            title="(untitled)",
            suppress_factors = None,
            color_map=None,
            widget=None,
            tooltips=[],  # optional
            figure_options={},
            **kwargs):
    """
    Make interactive heatmap of categorical data
    
    Parameters
    ----------
        
    Returns
    -------
    Bokeh Figure
    
    Examples
    --------

    """

    x_values = data[x].unique()
    y_values = list(reversed(data[y].unique()))

    TOOLS = "hover,save,pan,box_zoom,reset,wheel_zoom"
    
    fopts = dict(
                    title=title,
                     x_range=x_values,
                     y_range=y_values,
                     x_axis_location="above", width=900, height=400,
                     tools=TOOLS, toolbar_location='below',
                     tooltips=[(f'{x} {y}', f'@{x} @{y}'), ('value', f'@{values}')],
                     )
    fopts.update(figure_options)
        
    fig = figure(**fopts)

    fig.grid.grid_line_color = None
    fig.axis.axis_line_color = None
    fig.axis.major_tick_line_color = None
    fig.axis.major_label_text_font_size = "7px"
    fig.axis.major_label_standoff = 0
    fig.xaxis.major_label_orientation = pi / 3

    colors = ???
    if color_map is None:
        color_map = linear_cmap(values, colors, 
                                low=data[values].min(), 
                                high=data[values].max())
    
    r = fig.rect(x=x, y=y, width=1, height=1, source=data,
               fill_color=color_map,
               line_color=None)
    
    fig.add_layout(r.construct_color_bar(
        major_label_text_font_size="7px",
        ticker=BasicTicker(desired_num_ticks=len(colors)),
        formatter=PrintfTickFormatter(format="%d%%"),
        label_standoff=6,
        border_line_color=None,
        padding=5
    ), 'right')
    
    return fig
