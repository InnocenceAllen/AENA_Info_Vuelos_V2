import datetime
import logging as log
from datetime import datetime, date, timedelta
import pandas as pd
import numpy as np
import io
import requests

from info_vuelos_analysis import constants


def get_airports():
    airports = pd.read_csv("airports.csv", sep=';')
    return airports


def is_international(airport_code, airports):
    international = not any(airports.code == airport_code)
    return international


def get_delay(time, status):
    items = status.replace(':', ' ').split()
    numbers = [int(s) for s in items if s.isdigit()]
    if len(numbers) == 2:
        programmed_time = datetime.strptime(time, "%H:%M")
        actual_time = datetime(1900, 1, 1, numbers[0], numbers[1], 0)
        elapsedTime = actual_time - programmed_time
        delay_in_minutes = elapsedTime / timedelta(minutes=1)
        if delay_in_minutes < - 120:
            # Seguramente se ha producido un cambio de día, hay que recalcular incrementando en 1 el día
            actual_time = datetime(1900, 1, 2, numbers[0], numbers[1], 0)
            elapsedTime = actual_time - programmed_time
            delay_in_minutes = elapsedTime / timedelta(minutes=1)
        return delay_in_minutes
    else:
        return np.nan;

def get_departure_delay(row):
    delay = get_delay(row['dep_time'], row['dep_status'])
    return delay

def get_arrival_delay(row):
    delay = get_delay(row['arr_time'], row['arr_status'])
    return delay


def preprocessing():
    airports = get_airports()
    log.info('Loading airports info')
    log.info(''.join(str(a) + '; ' for a in airports))

    # load original dataset
    url = "https://raw.githubusercontent.com/InnocenceAllen/AENA_Info_Vuelos/master/infovuelos_sample.csv"
    log.info('Loading data from url: {}'.format(url))
    content = requests.get(url).content
    # flights_raw = pd.read_table('../infovuelos_sample.csv', sep=';')
    flights_raw = pd.read_table(io.StringIO(content.decode('utf-8')), sep=';')
    log.info('Original data has {} rows'.format(len(flights_raw.index)))

    # Eliminamos vuelos duplicados
    log.info("Removing duplicates")
    flights = flights_raw.drop_duplicates(['flightNumber', 'dep_date'], keep='last')
    log.info("Cleaned data has {} rows".format(len(flights.index)))

    log.info("Adding derived data")
    # Añadimos campos que indican si se trata de un vuelo internacional
    flights.loc[:, 'dep_int'] = flights.apply(lambda row: is_international(row['dep_airport_code'], airports), axis=1)
    flights.loc[:, 'arr_int'] = flights.apply(lambda row: is_international(row['arr_airport_code'], airports), axis=1)

    # Añadimos campos que contienen el retardo (diferencia entre hora real y hora programada)
    flights.loc[:, 'dep_delay'] = flights.apply(get_departure_delay, axis=1)
    flights.loc[:, 'arr_delay'] = flights.apply(get_arrival_delay, axis=1)

    # Nos quedamos solo con los campos (columnas del dataframe) que nos interesan
    log.info("Keeping selected fields")
    flights = flights[constants.DATA_FIELDS]
    # flights.drop(constants.FIELDS_DISCARDED)

    # Asignamos NaN a los valores "-"
    log.info("Marking NaN values")
    flights = flights.replace('-', np.nan)

    # Guardamos los datos modificados en un archivo
    filename = 'flights.csv'
    log.info("Saving modified dataset to file {}".format(filename))
    flights.to_csv(filename, sep=constants.CSV_DELIMITER, index=False)


if __name__ == "__main__":
    log.basicConfig(filename='../log/preprocessing.log',
                    level=log.INFO,
                    format='%(asctime)s %(message)s',
                    datefmt='%d/%m/%Y %I:%M:%S')
    preprocessing()
