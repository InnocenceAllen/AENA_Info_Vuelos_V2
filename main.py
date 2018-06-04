import pandas as pd

from pylab import figure, title, xlabel, ylabel, xticks, bar, \
                  legend, axis, savefig









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

#Si se pasan muchos valores se ve muy apretado. Revisar.
def plot(keyList,positiveList,negativeList):
    nucleotides = keyList

    counts = [
        positiveList,
        negativeList,
    ]

    figure(num=None, figsize=(80, 60), dpi=400, facecolor='w', edgecolor='k')

    title('Retraso de vuelos por dep_airport_name')
    ylabel('%')



    N = len(keyList)
    x = range(N)
    x2 = [x3 - 0.25 for x3 in x]
    x4 = [x3 - 0.125 for x3 in x]
    xticks(x4, nucleotides)
    xticks(rotation=90)
    bar(x, counts[0], width=0.2, color="#0c04e5", label="Sin Retraso %")

    bar(x2,counts[1], width=0.2, color="#ef0202", label="Con Retraso %")

    legend()

    savefig('barplot.png')

if __name__ == "__main__":


    flights = pd.read_table('infovuelos_sample.csv', sep=';')
    # Eliminamos vuelos duplicados
    flights = flights.drop_duplicates('flightNumber')

    #flightsDict=analyze(flights,'flightNumber');
    #print("{" + "\n".join("{}: {}".format(k, v) for k, v in flightsDict.items()) + "}")

    flightsDict = analyze(flights, 'dep_airport_name');
    #print("{" + "\n".join("{}: {} ->".format(key, value,) for key, value in flightsDict.items()) + "}")
    keyList=[]
    positiveList=[]
    negativeList=[]
    for key, value in flightsDict.items():

        positivo=value['positivo']
        negativo = value['negativo']
        positivoPercent = positivo / float(positivo + negativo)*100
        negativoPercent = negativo / float(positivo + negativo)*100
        keyList.append(key)
        positiveList.append(round(positivoPercent,2))
        negativeList.append(round(negativoPercent,2))

        print (key +" ->Positivos: "+str(positivoPercent)+"% Negativos "+str(negativoPercent)+"%");
    plot(keyList,positiveList,negativeList)
