def main():
    airports = get_airports()
    log.info('Loading airports info')
    log.info(''.join(str(a) + '; ' for a in airports))

    # load original dataset
    url = "https://raw.githubusercontent.com/InnocenceAllen/AENA_Info_Vuelos/master/infovuelos_sample.csv"
    content=requests.get(url).content
    #flights_raw = pd.read_table('../infovuelos_sample.csv', sep=';')
    flights_raw = pd.read_table(io.StringIO(content.decode('utf-8')), sep=';')

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
    log.basicConfig(filename='../log/analysis.log',
                    level=log.WARNING,
                    format='%(asctime)s %(message)s',
                    datefmt='%d/%m/%Y %I:%M:%S')
    main()
