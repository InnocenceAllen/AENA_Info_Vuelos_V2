import datetime
import logging as log
import time
import pandas as pd

from info_vuelos_analysis import util, constants

def get_airports():
    airports = pd.read_csv("airports.csv")
    return airports

def main():
    filename = 'flights-cleaned.csv'
    util.create_csv(filename, constants.DATA_FIELDS, constants.CSV_DELIMITER)
    airports = get_airports()
    log.info('Loading airports info')
    log.info(''.join(str(a) + '; ' for a in airports))
    current_time = datetime.datetime.now()




if __name__ == "__main__":
    log.basicConfig(filename='preprocessing{}.log'.format(time.strftime("%d-%m-%Y_%I-%M")), level=log.WARNING,
                    format='%(asctime)s %(message)s',
                    datefmt='%d/%m/%Y %I:%M:%S')
    main()
