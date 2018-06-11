import logging as log
import pandas as pd
import sys

from pathlib import Path

from info_vuelos_analysis import constants
from info_vuelos_analysis.classifier import dataset_split, encode_cat_ordinals, encode_cat_one_hot, \
    apply_knn_classifier, scale_data
from info_vuelos_analysis.infovuelos_preprocessing import get_airports, preprocessing
from info_vuelos_analysis.model import DelayLevel, TimeLevel

def get_delay_level(delay_in_minutes):
    if delay_in_minutes <= constants.DELAY_LEVEL_THRESHOLDS['NO_DELAY']:
        return DelayLevel.NO_DELAY.value
    elif delay_in_minutes <= constants.DELAY_LEVEL_THRESHOLDS['LOW_DELAY']:
        return DelayLevel.LOW_DELAY.value
    elif delay_in_minutes <= constants.DELAY_LEVEL_THRESHOLDS['MEDIUM_DELAY']:
        return DelayLevel.MEDIUM_DELAY.value
    else:
        return DelayLevel.HIGH_DELAY.value


def get_time_level(time):
    hour = int(time.split(":")[0])
    if hour <= constants.TIME_LEVEL_THRESHOLDS['NIGHT']:
        return TimeLevel.NIGHT.value
    elif hour <= constants.TIME_LEVEL_THRESHOLDS['MORNING']:
        return TimeLevel.MORNING.value
    elif hour <= constants.TIME_LEVEL_THRESHOLDS['AFTERNOON']:
        return TimeLevel.AFTERNOON.value
    else:
        return TimeLevel.EVENING.value


def select_data_fields(flights, fields):
    # df = flights[fields].dropna()
    df = flights[fields].copy().dropna()
    # Rename columns
    df.columns = constants.FEATURE_NAMES
    # Discretize delay into few categories (see class model.DelayLevel)
    # valid_rows = df['delay'].notnull()
    # df.loc[df['delay'].notnull(), 'delay'] = df.apply(lambda row: get_delay_level(row['delay']), axis=1)
    df.loc[:, 'delay'] = df.apply(lambda row: get_delay_level(row['delay']), axis=1)
    df.loc[:, 'time'] = df.apply(lambda row: get_time_level(row['time']), axis=1)
    return df


def main():
    log.info('Loading airports')
    airports = get_airports()

    # load preprocessed dataset
    filename = 'flights.csv'
    datafile = Path(filename);
    if not datafile.exists(): preprocessing()

    log.info('Loading flights')
    flights = pd.read_csv(filename, sep=constants.CSV_DELIMITER)
    log.info('Flights loaded: {} rows x {} columns'.format(flights.shape[0], flights.shape[1]))

    # Prepare data for classification

    # split data to deal separately with departures and arrivals. Due to the lack of
    # data when an airport is international we will consider only Spanish airports, either at the departure
    # or at the arrival

    national_departures = flights['dep_int'] == False
    departures = select_data_fields(flights[national_departures], constants.DEPARTURE_FIELDS)
    # departures.info()
    log.info('Departures: {} rows x {} columns'.format(departures.shape[0], departures.shape[1]))

    national_arrivals = flights['arr_int'] == False
    arrivals = select_data_fields(flights[national_arrivals], constants.ARRIVAL_FIELDS)
    # arrivals.info()
    log.info('Arrivals:  {} rows x {} columns'.format(arrivals.shape[0], arrivals.shape[1]))

    # Scaling temperatures
    # temps = ['t_min','t_max']
    # departures.loc[:, temps] = scale_data(departures[temps])
    # arrivals.loc[:, temps] = scale_data(arrivals[temps])
    # Converting categorical variables to numerical ones
    
    features, target = encode_cat_ordinals(departures)
    X_train, X_test, y_train, y_test = dataset_split(features, target, constants.TEST_SIZE, constants.RANDOM_SEED)
    apply_knn_classifier(X_train, X_test, y_train, y_test)

    features, target = encode_cat_one_hot(departures)
    X_train, X_test, y_train, y_test = dataset_split(features, target, constants.TEST_SIZE, constants.RANDOM_SEED)
    apply_knn_classifier(X_train, X_test, y_train, y_test)


if __name__ == "__main__":
    sys.setrecursionlimit(10000)
    log.basicConfig(filename='../log/analysis.log',
                    level=log.INFO,
                    format='%(asctime)s %(message)s',
                    datefmt='%d/%m/%Y %I:%M:%S')
    log.getLogger().addHandler(log.StreamHandler())
    main()
