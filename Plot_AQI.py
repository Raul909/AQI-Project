import pandas as pd
import matplotlib.pyplot as plt


def get_avg_data_by_year(year):
    """
    Calculates the average PM2.5 for each day (24-hour chunk) in the given year.
    Uses vectorized operations for improved performance.
    """
    average = []
    filepath = 'Data/AQI/aqi{}.csv'.format(year)
    for chunk in pd.read_csv(filepath, chunksize=24):
        # Convert PM2.5 to numeric, invalid entries (e.g., 'NoData', 'PwrFail') become NaN
        pm25 = pd.to_numeric(chunk['PM2.5'], errors='coerce')
        # Sum of numeric values (NaN are skipped by default).
        # Divide by 24 as per the original logic (average per day).
        avg = pm25.sum() / 24
        average.append(avg)
    return average


def avg_data_2013():
    return get_avg_data_by_year(2013)


def avg_data_2014():
    return get_avg_data_by_year(2014)


def avg_data_2015():
    return get_avg_data_by_year(2015)


def avg_data_2016():
    return get_avg_data_by_year(2016)


def avg_data_2017():
    return get_avg_data_by_year(2017)


def avg_data_2018():
    return get_avg_data_by_year(2018)


if __name__ == "__main__":
    lst2013 = avg_data_2013()
    lst2014 = avg_data_2014()
    lst2015 = avg_data_2015()
    lst2016 = avg_data_2016()
    lst2017 = avg_data_2017()
    lst2018 = avg_data_2018()
    plt.plot(range(0, 365), lst2013, label="2013 data")
    plt.plot(range(0, 364), lst2014, label="2014 data")
    plt.plot(range(0, 365), lst2015, label="2015 data")
    plt.plot(range(0, 121), lst2016, label="2016 data")
    plt.xlabel('Day')
    plt.ylabel('PM 2.5')
    plt.legend(loc='upper right')
    plt.show()
