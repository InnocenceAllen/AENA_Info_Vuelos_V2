import pandas as pd









#podemos añadir tambien en el dict el tiempo de retraso.

def analyze( flights,parameter):
    flightsDict=dict()
    for index, row in flights.iterrows():
        tempDict = dict()
        if row[parameter] in flightsDict:
            tempDict= flightsDict.get(row[parameter])
            if row['dep_status'].find("Salida prevista"): # cuando pone esto entiendo que sale de forma puntual 5+- min (revisar)
                tempDict['positivo']=tempDict['positivo']+1
            else:
                tempDict['negativo'] = tempDict['negativo'] + 1
        else:
            if row['dep_status'].find("Salida prevista"):  # cuando pone esto entiendo que sale de forma puntual 5+- min (revisar)
                tempDict.setdefault('positivo',1)
                tempDict.setdefault('negativo', 0)

            else:
                tempDict.setdefault('positivo', 0)
                tempDict.setdefault('negativo', 1)

        flightsDict[row[parameter]]=tempDict
    return flightsDict


if __name__ == "__main__":

    flights = pd.read_table('infovuelos_sample.csv', sep=';')
    # Eliminamos vuelos duplicados
    flights = flights.drop_duplicates('flightNumber')

    #flightsDict=analyze(flights,'flightNumber');
    #print("{" + "\n".join("{}: {}".format(k, v) for k, v in flightsDict.items()) + "}")

    flightsDict = analyze(flights, 'dep_airport_name');
    print("{" + "\n".join("{}: {}".format(k, v) for k, v in flightsDict.items()) + "}")