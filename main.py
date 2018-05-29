import pandas as pd



flights = pd.read_table('infovuelos_sample.csv', sep=';')

#Eliminamos vuelos duplicados
flights=flights.drop_duplicates('flightNumber')



flightsDict = dict()

#parametrizar row['flightNumber' y convertir lo siguiente en una funcion,de esta forma podremos ir probando segun compañia,vuelo,aeropuerto o bien clima
#podemos añadir tambien en el dict el tiempo de retraso.
for index, row in flights.iterrows():
    tempDict = dict()
    if row['flightNumber'] in flightsDict:
        tempDict= flightsDict.get(row['flightNumber'])
        if row['dep_status'].find("Salida prevista"): # cuando pone esto entiendo que sale de forma puntual 5+- min (revisar)
            tempDict['positivo']=tempDict.get['positivo']+1
        else:
            tempDict['negativo'] = tempDict.get['negativo'] + 1
    else:
        if row['dep_status'].find("Salida prevista"):  # cuando pone esto entiendo que sale de forma puntual 5+- min (revisar)
            tempDict.setdefault('positivo',1)
            tempDict.setdefault('negativo', 0)

        else:
            tempDict.setdefault('positivo', 0)
            tempDict.setdefault('negativo', 1)

    flightsDict[row['flightNumber']]=tempDict



print("{" + "\n".join("{}: {}".format(k, v) for k, v in flightsDict.items()) + "}")
