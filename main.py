import pandas as pd
from datetime import datetime, date

from pylab import figure, title, xlabel, ylabel, xticks, bar, \
                  legend, axis, savefig











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
                pos=row['dep_status'].find(':')
                horaSalida=row['dep_status'][pos - 2:pos + 3]
                horaPrevista=row['dep_time']
                horaSalida = datetime.strptime(horaSalida, "%H:%M").time()
                horaPrevista = datetime.strptime(horaPrevista, "%H:%M").time()
                delay = datetime.combine(date.today(), horaSalida) - datetime.combine(date.today(), horaPrevista)
                tempDict['retraso'] = tempDict['retraso'] + delay.seconds
        else:
            if row['dep_status'].find("Salida prevista"):  # cuando pone esto entiendo que sale de forma puntual 5+- min (revisar)
                tempDict.setdefault('positivo',1)
                tempDict.setdefault('negativo', 0)
                tempDict.setdefault('retraso',0)

            else:
                tempDict.setdefault('positivo', 0)
                tempDict.setdefault('negativo', 1)
                horaSalida = row['dep_status'][pos - 2:pos + 3]
                horaPrevista = row['dep_time']
                horaSalida=datetime.strptime(horaSalida, "%H:%M").time()
                horaPrevista = datetime.strptime(horaPrevista, "%H:%M").time()
                delay=datetime.combine(date.today(), horaSalida) - datetime.combine(date.today(), horaPrevista)
                tempDict.setdefault('retraso',delay.seconds)

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
    flights = flights.drop_duplicates(['flightNumber', 'dep_date'], keep='last')


    flightsDict=analyze(flights,'flightNumber');


    #print("{" + "\n".join("{}: {} ->".format(key, value,) for key, value in flightsDict.items()) + "}")
    keyList=[]
    positiveList=[]
    negativeList=[]
    for key, value in flightsDict.items():

        positivo=value['positivo']
        negativo = value['negativo']
        retrasoMedio = round((value['retraso']/negativo)/float(60),2)

        positivoPercent = round(positivo / float(positivo + negativo)*100,2)
        negativoPercent = round(negativo / float(positivo + negativo)*100,2)
        keyList.append(key)
        positiveList.append(round(positivoPercent,2))
        negativeList.append(round(negativoPercent,2))

        print (key +" ->Positivos: "+str(positivoPercent)+"% Negativos "+str(negativoPercent)+"% Retraso medio "+str(retrasoMedio)+" Min");
    #plot(keyList,positiveList,negativeList)
