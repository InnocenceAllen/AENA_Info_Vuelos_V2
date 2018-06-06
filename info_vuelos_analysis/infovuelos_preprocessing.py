import datetime
import logging as log
import time
from datetime import datetime, date, timedelta
import pandas as pd
import numpy as np

from info_vuelos_analysis import constants


def get_airports():
    airports = pd.read_csv("airports.csv")
    return airports


def is_international(airport_code, airports):
    return not airport_code in airports.index


def get_delay(time, status):
    items = status.replace(':',' ').split()
    numbers = [int(s) for s in items if s.isdigit()]
    if len(numbers) == 2:
        programmed_time = datetime.strptime(time,"%H:%M")
        actual_time = datetime(1900, 1, 1, numbers[0], numbers[1], 0)
        elapsedTime = actual_time - programmed_time
        delay_in_minutes = elapsedTime / timedelta(minutes=1)
        return delay_in_minutes
    else:
        return np.nan;


def main():
    airports = get_airports()
    log.info('Loading airports info')
    log.info(''.join(str(a) + '; ' for a in airports))
    flights_raw = pd.read_table('../infovuelos_sample.csv', sep=';')

    # Eliminamos vuelos duplicados
    flights = flights_raw.drop_duplicates(['flightNumber', 'dep_date'], keep='last')

    # Añadimos campos que indican si se trata de un vuelo internacional
    flights.loc[:, 'dep_int'] = flights.apply(lambda row: is_international(row['dep_airport_code'], airports), axis=1)
    flights.loc[:, 'arr_int'] = flights.apply(lambda row: is_international(row['arr_airport_code'], airports), axis=1)

    # Añadimos campos que contienen el retardo (diferencia entre hora real y hora programada)
    flights.loc[:, 'dep_delay'] = flights.apply(lambda row: get_delay(row['dep_time'], row['dep_status']), axis=1)
    flights.loc[:, 'arr_delay'] = flights.apply(lambda row: get_delay(row['arr_time'], row['arr_status']), axis=1)

    # Nos quedamos solo con los campos (columnas del dataframe) que nos interesan
    flights = flights[constants.DATA_FIELDS]
    # flights.drop(constants.FIELDS_DISCARDED)

    # Asignamos NaN a los valores "-"
    flights = flights.replace('-', np.nan)

    filename = 'flights.csv'
    flights.to_csv(filename, sep=constants.CSV_DELIMITER)


if __name__ == "__main__":
    log.basicConfig(filename='../log/preprocessing.log',
                    level=log.WARNING,
                    format='%(asctime)s %(message)s',
                    datefmt='%d/%m/%Y %I:%M:%S')
    main()
