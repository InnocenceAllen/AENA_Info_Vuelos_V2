import pandas as pd
import operator
from datetime import datetime, date

from pylab import figure, title, xlabel, ylabel, xticks, bar, \
                  legend, axis, savefig











def analyze( flights,parameter,col_delay):
    flightsDict=dict()
    for index, row in flights.iterrows():
        tempDict = dict()
        if row[parameter] in flightsDict:
            tempDict= flightsDict.get(row[parameter])
            if row[col_delay]<=0: # cuando pone esto entiendo que sale de forma puntual 5+- min (revisar)
                tempDict['positivo']=tempDict['positivo']+1
            else:
                tempDict['negativo'] = tempDict['negativo'] + 1
                #pos=row['dep_status'].find(':')
                #horaSalida=row['dep_status'][pos - 2:pos + 3]
                #horaPrevista=row['dep_time']
                #horaSalida = datetime.strptime(horaSalida, "%H:%M").time()
                #horaPrevista = datetime.strptime(horaPrevista, "%H:%M").time()
                #delay = datetime.combine(date.today(), horaSalida) - datetime.combine(date.today(), horaPrevista)
                delay=row[col_delay]
                tempDict['retraso'] = tempDict['retraso'] + delay
        else:

            if row[col_delay]<=0:  # cuando pone esto entiendo que sale de forma puntual 5+- min (revisar)
                tempDict.setdefault('positivo',1)
                tempDict.setdefault('negativo', 0)
                tempDict.setdefault('retraso',0)

            else:
                tempDict.setdefault('positivo', 0)
                tempDict.setdefault('negativo', 1)
                #horaSalida = row['dep_status'][pos - 2:pos + 3]
                #horaPrevista = row['dep_time']
                #horaSalida=datetime.strptime(horaSalida, "%H:%M").time()
                #horaPrevista = datetime.strptime(horaPrevista, "%H:%M").time()
                #delay=datetime.combine(date.today(), horaSalida) - datetime.combine(date.today(), horaPrevista)
                delay = row[col_delay]
                tempDict.setdefault('retraso',delay)

        flightsDict[row[parameter]]=tempDict
    return flightsDict

#Si se pasan muchos valores se ve muy apretado. Revisar.
def plot(parameter,keyList,positiveList,negativeList):
    nucleotides = keyList
    counts = [
        positiveList,
        negativeList,
    ]
    figure(num=None, figsize=(10, 7.5), dpi=100 )
    title('Retraso de vuelos por '+parameter)
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
    savefig(parameter+'_plot.png')




def result(flightsDict,printable):
    keyList = []
    positiveList = []
    negativeList = []
    for key, value in flightsDict.items():
        positivo = 0
        negativo = 0;
        retrasoMedio = 0;
        positivo = value['positivo']
        negativo = value['negativo']
        if (negativo != 0):
            retrasoMedio = round((value['retraso'] / negativo), 2)
        else:
            retrasoMedio: 0

        positivoPercent = round(positivo / float(positivo + negativo) * 100, 2)
        negativoPercent = round(negativo / float(positivo + negativo) * 100, 2)
        keyList.append(key)
        positiveList.append(round(positivoPercent, 2))
        negativeList.append(round(negativoPercent, 2))
        if printable:
            print(key + " ->Positivos: " + str(positivoPercent) + "% Negativos " + str(
                negativoPercent) + "% Retraso medio " + str(retrasoMedio) + " Min");

    return keyList,positiveList,negativeList;

def training(flightsDict):
    trainingDict = dict()
    item = analyze(flightsDict, 'flightNumber', 'dep_delay');
    trainingDict.setdefault('flightNumber',item);

    item = analyze(flightsDict, 'dep_airport_code', 'dep_delay');
    trainingDict.setdefault('dep_airport_code', item);

    return trainingDict;

#flightDic pasar como el anterior, con parametro / en este caso trainingDict no se ha calculado con ninguno del training
def calculate(trainingDict,flights):
    tmpDict = dict()

    #parametro dep_airport_code,flightNumber etc

    for paramKey in trainingDict.keys():
        for index, row in flights.iterrows():
            try:
              if  paramKey in trainingDict:
                vuelo=trainingDict[paramKey][row[paramKey]]
                positive=vuelo['positivo']
                negative = vuelo['negativo']
                pdelay=negative/float(positive+negative)
                if row['flightNumber'] in tmpDict:
                    tmpDict[row['flightNumber']]=tmpDict[row['flightNumber']]*pdelay
                else:
                    tmpDict.setdefault(row['flightNumber'],pdelay)
            except:
                pass #significa que de este parametro no tenemos informacion. (cambiar)

    return tmpDict;


def validation(resultDict, validatioDict):

    truePositive=0
    trueNegative=0
    falsePositive=0
    falseNegative=0


    for flightKey, pdelay in resultDict.items():
            total=validatioDict[flightKey]['positivo']+validatioDict[flightKey]['negativo']
            if (total==0):#valor por defecto que damos si no hay datos
                total=0.5
            pdelayValidation=validatioDict[flightKey]['negativo']/float(total)
            if pdelay>0.5:
                if pdelayValidation>0.5:
                    truePositive+=1
                else:
                    falsePositive+=1

            else:
                if pdelayValidation<=0.5:
                    trueNegative+=1
                else:
                    falseNegative+=1



    print("truePositive: "+str(truePositive)+" trueNegative "+str(trueNegative)+" falsePositive "+str(falsePositive)+" falseNegative "+str(falseNegative));
    accuracy=(truePositive+trueNegative)/float(truePositive+trueNegative+falsePositive+falseNegative)
    print("accuracy: "+str(accuracy));
    return truePositive,trueNegative,falsePositive,falseNegative;







if __name__ == "__main__":


    flights = pd.read_table('flights.csv', sep=';')
    flights = flights.drop_duplicates(['flightNumber', 'dep_date'], keep='last')
    '''  flightsDict=analyze(flights,'flightNumber','dep_delay');
    resultado = sorted(flightsDict.items(), key=lambda x: x[1]['negativo'], reverse=True)
    print(resultado)
    keyList, positiveList, negativeList = result(flightsDict,1)
    plot('flightNumber',keyList[:6],positiveList[:6],negativeList[:6])


    flightsDict = analyze(flights, 'dep_airport_code', 'dep_delay');
    resultado = sorted(flightsDict.items(), key=lambda x: x[1]['negativo'], reverse=True)
    print(resultado)
    keyList, positiveList, negativeList = result(flightsDict, 1)
    plot('dep_airport_code', keyList, positiveList, negativeList)'''
    flightsDict = analyze(flights, 'flightNumber', 'dep_delay');
    trainingDic= training(flights[50:])
    resultDict=calculate(trainingDic,flights[:49])
    validation=validation(resultDict,flightsDict)



