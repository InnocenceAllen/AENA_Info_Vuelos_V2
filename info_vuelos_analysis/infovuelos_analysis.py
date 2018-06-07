from info_vuelos_analysis import constants
from info_vuelos_analysis.infovuelos_preprocessing import get_airports, preprocessing
import logging as log
import pandas as pd
from pathlib import Path
import numpy as np


def main():
    log.info('Loading airports')
    airports = get_airports()


    # load preprocessed dataset
    filename = 'flights.csv'
    datafile = Path(filename);
    if not datafile.exists(): preprocessing()

    log.info('Loading flights')
    flights = pd.read_csv(filename, sep=constants.CSV_DELIMITER)
    flights_shape = flights.shape
    log.info('Loaded: {} rows x {} columns'.format(flights_shape[0], flights_shape[1]))

    # Perform analysis


if __name__ == "__main__":
    log.basicConfig(filename='../log/analysis.log',
                    level=log.INFO,
                    format='%(asctime)s %(message)s',
                    datefmt='%d/%m/%Y %I:%M:%S')
    main()
