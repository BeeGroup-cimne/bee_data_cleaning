# bee_data_cleaning
BeeDataCleaning is a outlayer detection library for energy and temperature timeseries.

it is organized in two modules:

1. data_cleaning
2. visualization

## data_cleaning

This module contains the data cleaning functions to detect the outliers and clean their data.

### functions:

##### detect_min_threshold_outliers(series, threshold)
Detects the values that are lower than the threshold passed
    
    series : series, mandator
      
        The series where to detect the outliers
        
    threshold : integer, float, mandatory
    
        The threshold of the minimum value that will be considered outliers.

##### detect_znorm_outliers(series, threshold, mode="global", **kwargs)
Detects the outliers usin the znorm technique.
    
    
    series : series, mandatory
        The series where to detect the outliers
        
    threshold : integer, float, mandatory
        The threshold of the maximum znorm value to considere as outliers.
        
    mode: string, mandatory
        Indicate the mode to perform the znorm outlier detection; possible values are:
        'global': considere all the series at once
        'rolling': use a window and slide it through the time series
        
    window: integer, only when 'rolling'
        The size of the window used when rolling
        
    lowq: float, default=2.5
        The lower percentile to not considere when performing the mean and std for the znorm
        
    highq float, default=97.5
        The higher percentile to not considere when performing the mean and std for the znorm
    

##### detect_max_threshold_outliers(series, threshold)
Detects the values that are higer than the threshold passed
        
    series : series, mandatory
        The series where to detect the outliers
        
    threshold : integer, float, mandatory
        The threshold of the maximum value that will be considered outliers.
   

##### detect_outliers(series, threshold, method, **kwargs)
Deprecated due to its complexity

Detects all outliers with the different methods by order on the lists
    
    
    series : series, mandatory
        The series where to detect the outliers
        
    threshold : list of integer, float, mandatory
        The threshold of the maximum value that will be considered outliers for each method.
        
    threshold : list of strings, mandatory
        The threshold of the maximum value that will be considered outliers for each method.


##### clean_series(series, bool_outliers)
Cleans the series by setting its outliers to 'NaN'

This function should be used with the results of the the "detect_x" functions, to clean the outliers from the timeseries

    series : series, mandatory
        The series to clean
    bool_outlier : array or series, mandatory

  
##### percentage_of_gaps(series)
Returns the percentage of nans found in the series'

    series : series, mandatory
        The series to calculate the percentage of NaN



##### summary(series, **kwargs)
Returns information about the timeseries passed
"dateStart", "dateEnd", "frequency", "mean", "sd", "min", "max", "p1",
"p5", "p25", "p50", "p75", "p95", "p99"

    series : series, mandatory
        The series to get the information
   
  
## Visualization

This module contains the visualization functions to analyze the dataframe.


### functions:


##### plot_dataframe(df_to_plot, pdf, height=None, width=None, title="Dataset")
Plots the dataframes

    df_to_plot: pandas.DataFrame, mandatory
        dataframe to plot
    pdf: PDFobject or string, mandatory
        file where the plot will be stored
    height: int, optional
        height of the plot
    width: int, optional
        width of the plot
    title: string, default="Dataset"
        title of the plot
 


##### plot_timeseries(series, names_series, pdf, series_labels=None, series_outliers=None, series_negatives=None, ylabel="Value", title="Time series plot")

Plot high frequency time series of data.

    :param series: pandas.Series of List of pandas.Series with DateTime index.
        the time series which will be drawn in the plot.
    :param names_series: list of strings
        the names of the series. In the same order to the series list.
    :param pdf: PDFobject or string
        file where the plot will be stored
    :param series_labels: pandas.Series with datetime index
        This series will be represented by labels painted on the main series, so is recommended to contain very few items.
    :param series_outliers: pd.Series with datetime index and Boolean values
         If true, that element is an outlier
    :param series_negatives:
        Boolean Pandas series with datetime index
        If true, that element is negative.
    :param ylabel: str
        The Y axis label name
    :param title: str
        Title of the plot
    :return:
 

##### plot_histogram(series, pdf, title="Histogram"):
Plot histogram of a series.

    :param series: Pandas series object
    :param pdf: PDF object or PDF filename where the plot will be stored
    :param title: Title of the plot
    :return:


##### initialize_plotly_by_rows(nrows, titles):
Initiates a plotly to plot the timeseries.

    nrows: integer, mandatory
        the number of rows to add in the plot
    titles: list of strings,mandatory
        the titles to add to each row


##### add_plotly_timeseries(fig, series, label, unit):
Adds a new timeseries to the plotly objecs

    fig: plotly figure, mandatory
        the plotly figure to add the timeseries
    series:  a series
        The series to add to the data.
    label: string,
        A label indicating information about the data
    unit: string,
        The unit of the data
    
