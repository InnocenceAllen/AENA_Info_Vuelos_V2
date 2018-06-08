import pandas as pd
import matplotlib.pyplot as plt

#Import flights dataset
flights = pd.read_csv('flights.csv',sep=';');

#Time of the day
flights_time = flights.dropna(subset=['dep_time'])
hours = flights_time['dep_time'].str.replace(':', '').astype(int)
day_time = []
for x in hours:
    print(x)
    if (x >= 500 and x < 1200):
        day_time.append('Mannana')
    elif (x >= 1200 and x < 1800):
        day_time.append('Tarde')
    else:
        day_time.append('Noche')

data = pd.DataFrame(data = day_time,columns=['dep_time'])
day = data['dep_time'].value_counts();
#day.plot(kind = 'bar', title = 'Cantidad de vuelos por horario',legend = False);
#plt.xlabel('Horario del dia')
#plt.ylabel('Cantidad de vuelos')
#plt.show();

# Total/Freq per airport on National flies
group_aerop = flights.loc[flights['arr_int'] == False];
group_aerop = group_aerop['arr_airport_code'].value_counts(normalize = True);
#group_aerop.plot(kind = 'bar', title = 'Vuelos por aeropuerto', legend = False);
#plt.xlabel('Aeropuertos')
#plt.ylabel('Frecuencia de vuelos recibidos')
#plt.show();


#Total/Freq per type of flight (National/International)
inter =flights['arr_int'].value_counts(normalize=True);
#colors = ['black', 'white']
labels = 'Internacionales', 'Nacionales'
inter.plot(kind = 'pie',autopct='%1.1f%%',labels=labels,legend = False);
plt.title('Frecuencia vuelos Nacionales Internacionales')
plt.show();



