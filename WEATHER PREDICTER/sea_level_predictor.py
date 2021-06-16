import pandas as pd    #adilkhan
import matplotlib.pyplot as plt
from scipy.stats import linregress

def draw_plot():
    # Read data from file
    df = pd.read_csv(
    'epa-sea-level.csv') #First task [reading]

    # Create scatter plot
    x = df['Year'] #first column[Year]
    y = df['CSIRO Adjusted Sea Level']#sea level[]          #adilkhan

    # Create first line of best fit from 1800-2050 #Assanali
    slope = linregress(x, y).slope #finding regression
    intercept = linregress(x, y).intercept
    print(slope)
    print(intercept)
    print(df)
    def myfunc(x):
      return slope * x + intercept

    plt.scatter(x, y)

    x_pred = pd.Series([i for i in range(1880,2050)])
    y_pred = slope * x_pred + intercept

    # Create second line of best fit from year 2000-2050
    x_2000 = df[ df['Year'] >= 2000 ]['Year']
    y_2000 = df[ df['Year'] >= 2000 ]['CSIRO Adjusted Sea Level']  #Assanali

    fit2 = linregress(x_2000, y_2000)  #Zhanibek
    slope_2000 = fit2.slope
    intercept_2000 = fit2.intercept

    x_pred2 = pd.Series([i for i in range(2000,2050)])
    y_pred2 = slope_2000 * x_pred2 + intercept_2000
    #plt.scatter(x, y)
    plt.plot(x_pred, y_pred, x_pred2, y_pred2, "g") #Zhanibek

    # Add labels and title       #adilkhan
    plt.xlabel("Year")
    plt.ylabel("Sea Level (inches)")
    plt.title("Rise in Sea Level")

    # Save plot and return data for testing (DO NOT MODIFY)
    plt.savefig('sea_level_plot.png')
    return plt.gca()          #adilkhan