import panel as pn
import pandas as pd
import hvplot
import hvplot.pandas
import datetime as dt

class PlotDf:
    """
    A cell with code snippet and _output data.
    TBD convert to a class with panel param based design pattern
    """
    def __init__(self, df: pd.DataFrame, time_field: str):
        """
        Create a plot from the given dataframe
        """
        self._df=df
        self._time_field=time_field

    @property
    def df(self):
        return self._df
    
    def head(self):
        return self._df.head()

    def dashboard(self):
        time_field = self._time_field
        title = pn.pane.Markdown(f'## Data Plot ')
        subtitle = pn.pane.Markdown(f'### Select a ticker and date range')
        field = pn.widgets.Select(name='Field', options=list(self._df.columns))
        date_range_slider = pn.widgets.DateRangeSlider(
            name='Date Range Slider',
            start=dt.datetime(2001, 1, 1),
            end=dt.datetime(2024, 1, 1),
            value=(dt.datetime(2001, 1, 1), dt.datetime(2024, 1, 1))
        )
        @pn.depends(field.param.value, date_range_slider.param.value)
        def get_plot(field_type, date_range):
            # Load and format the data
            df = self._df # define df
            df[time_field] = pd.to_datetime(df[time_field])
            # create date filter using values from the range slider
            # store the first and last date range slider value in a var
            start_date = date_range_slider.value[0] 
            end_date = date_range_slider.value[1]
            field_name = field.value
            # create filter mask for the dataframe
            mask = (df[time_field] > start_date) & (df[time_field] <= end_date)
            df = df.loc[mask] # filter the dataframe
            chart=df.hvplot.line(x=time_field,y=field_name, title=f'{field_name} over time')
            return chart
        dashboard = pn.Row('dashboard', 
                           pn.Column(title, subtitle, field, date_range_slider), 
                           get_plot)
        return dashboard
    