import pandas as pd
import matplotlib.pyplot as plt

def main():
    # Import flights dataset
    flights = pd.read_csv('flights.csv', sep=';')

    # Plottin by time of the day
    flights_time = flights.dropna(subset=['dep_time'])
    hours = flights_time['dep_time'].str.replace(':', '').astype(int)
    day_time = []
    for x in hours:
        if (x >= 500 and x < 1200):
            day_time.append('Mannana')
        elif (x >= 1200 and x < 1800):
            day_time.append('Tarde')
        else:
            day_time.append('Noche')

    data = pd.DataFrame(data=day_time, columns=['dep_time'])
    day = data['dep_time'].value_counts()
    day.plot(kind = 'bar', title = 'Cantidad de vuelos por horario',legend = False)
    plt.xlabel('Horario del dia')
    plt.ylabel('Cantidad de vuelos')
    plt.show()

    # Plotting Total/Freq per airport on National flies
    group_aerop = flights.loc[flights['arr_int'] == False]
    group_aerop = group_aerop['arr_airport_code'].value_counts(normalize=True)
    group_aerop.plot(kind = 'bar', title = 'Vuelos por aeropuerto', legend = False)
    plt.xlabel('Aeropuertos')
    plt.ylabel('Frecuencia de vuelos recibidos')
    plt.show()

    # Plotting Total/Freq per type of flight (National/International)
    inter = flights['arr_int'].value_counts(normalize=True)
    colors = ['black', 'white']
    labels = 'Internacionales', 'Nacionales'
    inter.plot(kind = 'pie',autopct='%1.1f%%',labels=labels,legend = False)
    plt.title('Frecuencia vuelos Nacionales Internacionales')
    plt.show()

    # Weather
    weather = flights['dep_weather_desc'].value_counts(normalize=True)
    weather.plot(kind = 'bar', legend = False);
    plt.title('Frecuencia del estado del tiempo a la salida del vuelo')
    plt.xlabel('Clima')
    plt.ylabel('Frecuencia de vuelos efectuados')
    plt.show()

    # Weather delay
    delay = flights['dep_delay'] > 30
    df_big_delay = flights[delay]
    weather_delay = df_big_delay['dep_weather_desc'].value_counts()
    weather_delay.plot(kind = 'bar', legend = False);
    plt.title('Clima en grandes retrasos')
    plt.xlabel('Clima')
    plt.ylabel('Cantidad de vuelos demorados mas de 30 mins')
    plt.show()

    # Companies
    companies = flights['company'].value_counts();
    filter_company = companies.head(8)
    if len(companies) > 8:
        filter_company['Otras {0} compañías'.format(len(companies) - 8)] = sum(companies[8:])
    filter_company.plot(kind='pie', autopct='%1.1f%%', legend=False , y =None)
    plt.title('Porciento de vuelos por compannia')
    plt.ylabel("")
    plt.show()


main()



