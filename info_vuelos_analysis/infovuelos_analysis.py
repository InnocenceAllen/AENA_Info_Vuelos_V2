from info_vuelos_analysis import constants
from info_vuelos_analysis.classifier import svm
from info_vuelos_analysis.infovuelos_preprocessing import get_airports, preprocessing
import logging as log
import pandas as pd
import numpy as np
from pathlib import Path
from info_vuelos_analysis.model import DelayLevel


def get_delay_level(delay_in_minutes):
    if delay_in_minutes <= constants.DELAY_LEVEL_THRESHOLDS['NO_DELAY']:
        return DelayLevel.NO_DELAY.value
    elif delay_in_minutes <= constants.DELAY_LEVEL_THRESHOLDS['LOW_DELAY']:
        return DelayLevel.LOW_DELAY.value
    elif delay_in_minutes <= constants.DELAY_LEVEL_THRESHOLDS['MEDIUM_DELAY']:
        return DelayLevel.MEDIUM_DELAY.value
    else:
        return DelayLevel.HIGH_DELAY.value


def select_data_fields(flights, fields):
    # df = flights[fields].dropna()
    df = flights[fields].copy().dropna()
    # Rename columns
    df.columns = constants.FEATURE_NAMES
    # Discretize delay into few categories (see class model.DelayLevel)
    # valid_rows = df['delay'].notnull()
    # df.loc[df['delay'].notnull(), 'delay'] = df.apply(lambda row: get_delay_level(row['delay']), axis=1)
    df.loc[:, 'delay'] = df.apply(lambda row: get_delay_level(row['delay']), axis=1)
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
    log.info('Loaded: {} rows x {} columns'.format(flights.shape[0], flights.shape[1]))

    # Prepare data for classification

    # flights.info()

    # split data to deal separately with departures and arrivals. Due to the lack of
    # data when an airport is international we will consider only Spanish airports, either at the departure
    # or at the arrival

    national_departures = flights['dep_int'] == False
    departures = select_data_fields(flights[national_departures], constants.DEPARTURE_FIELDS)
    departures.info()

    national_arrivals = flights['arr_int'] == False
    arrivals = select_data_fields(flights[national_arrivals], constants.ARRIVAL_FIELDS)
    arrivals.info()

    svm(departures)


if __name__ == "__main__":
    log.basicConfig(filename='../log/analysis.log',
                    level=log.INFO,
                    format='%(asctime)s %(message)s',
                    datefmt='%d/%m/%Y %I:%M:%S')
    main()
