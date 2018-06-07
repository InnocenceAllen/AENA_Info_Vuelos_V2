import pandas as pd
import matplotlib.pyplot as plt


flights = pd.read_csv('flights.csv',sep=';');
#print(flights);

#Getting unique values from attribute
#inter =flights['arr_int'].value_counts(normalize=True);
group_aerop =flights['arr_airport_code'].value_counts();

#Plotting attributes
#inter.plot(kind = 'pie', title = 'Frecuencia vuelos Nacionales Internacionales');
group_aerop.plot(kind = 'hist', title = 'Vuelos por aeropuerto', legend = True);
print(group_aerop)
plt.show();


