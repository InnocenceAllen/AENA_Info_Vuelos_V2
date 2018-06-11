DATA_FIELDS = ['flightNumber', 'company', 'plane', 'dep_date', 'dep_time', 'dep_airport_code',
               'dep_weather_min', 'dep_weather_max', 'dep_weather_desc', 'arr_date', 'arr_time',
               'arr_airport_code', 'arr_weather_min', 'arr_weather_max', 'arr_weather_desc',
               'dep_delay', 'arr_delay', 'dep_int', 'arr_int']
CSV_DELIMITER = ';'
DATASET_FILENAME = '../dataset.csv'
DELAY_LEVEL_THRESHOLDS = {'NO_DELAY': 5, 'LOW_DELAY': 25, 'MEDIUM_DELAY': 60, 'HIGH_DELAY': 9999}
TIME_LEVEL_THRESHOLDS = {'NIGHT': 6, 'MORNING': 12, 'AFTERNOON': 18, 'EVENING': 24}

RANDOM_SEED = 99  # Seed
TEST_SIZE = 0.25

DEPARTURE_FIELDS = ['company', 'plane', 'dep_time', 'dep_airport_code',
                    'dep_weather_min', 'dep_weather_max', 'dep_weather_desc', 'dep_delay']
ARRIVAL_FIELDS = ['company', 'plane', 'arr_time', 'arr_airport_code',
                  'arr_weather_min', 'arr_weather_max', 'arr_weather_desc', 'arr_delay']
FEATURE_NAMES = ['company', 'plane', 'time', 'airport', 't_min', 't_max', 'weather', 'delay']
