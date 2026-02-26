import pandas as pd
import matplotlib.pyplot as plt

def calculate_average(file_path):
    average=[]
    for rows in pd.read_csv(file_path,chunksize=24):
        # Optimized logic: Vectorized operations
        df = rows

        # Convert 'PM2.5' column to numeric, coercing errors (strings like 'NoData', 'PwrFail', etc.) to NaN
        # The original code logic effectively treated invalid strings as 0 (skipping addition).
        # pd.to_numeric(errors='coerce') converts invalid strings to NaN.
        numeric_series = pd.to_numeric(df['PM2.5'], errors='coerce')

        # sum() treats NaN as 0 by default.
        total = numeric_series.sum()

        # Calculate average over 24 hours (chunk size)
        avg = total / 24
        average.append(avg)
    return average

def avg_data_2013():
    return calculate_average('Data/AQI/aqi2013.csv')

def avg_data_2014():
    return calculate_average('Data/AQI/aqi2014.csv')

def avg_data_2015():
    return calculate_average('Data/AQI/aqi2015.csv')

def avg_data_2016():
    return calculate_average('Data/AQI/aqi2016.csv')

def avg_data_2017():
    return calculate_average('Data/AQI/aqi2017.csv')

def avg_data_2018():
    return calculate_average('Data/AQI/aqi2018.csv')


if __name__=="__main__":
    lst2013=avg_data_2013()
    lst2014=avg_data_2014()
    lst2015=avg_data_2015()
    lst2016=avg_data_2016()
    lst2017=avg_data_2017()
    lst2018=avg_data_2018()
    plt.plot(range(0,365),lst2013,label="2013 data")
    plt.plot(range(0,364),lst2014,label="2014 data")
    plt.plot(range(0,365),lst2015,label="2015 data")

    # Fix: lst2016 has 365 entries (full year), but range is only 121. Slice list to match.
    plt.plot(range(0,121),lst2016[:121],label="2016 data")

    plt.xlabel('Day')
    plt.ylabel('PM 2.5')
    plt.legend(loc='upper right')
    plt.show()
