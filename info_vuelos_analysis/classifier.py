from sklearn import svm
from sklearn import preprocessing
from sklearn.model_selection import train_test_split

from info_vuelos_analysis import constants


def svm(data):
    print(data.head())

    company_encoder = preprocessing.LabelEncoder()
    company_encoder.fit(data['company'])
    company_encoder.classes_
    company = company_encoder.transform(data['company'])

    plane_encoder = preprocessing.LabelEncoder()
    plane_encoder.fit(data['plane'])
    plane_encoder.classes_

    airport_encoder = preprocessing.LabelEncoder()
    airport_encoder.fit(data['airport'])
    airport_encoder.classes_
    airport = airport_encoder.transform(data['airport'])

    weather_encoder = preprocessing.LabelEncoder()
    weather_encoder.fit(data['weather'])
    weather_encoder.classes_
    weather = weather_encoder.transform((data['weather']))

    # Select data to be used in classification
    features = data[['company','airport','weather']].values
    target = data['delay'].values

    # Make a train/test split using 30% test size
    X_train, X_test, y_train, y_test = train_test_split(features, target,
                                                        test_size=constants.TEST_SIZE,
                                                        random_state=constants.RANDOM_SEED)

    # clf = svm.SVC(gamma=0.001, C=100.)
    # clf.fit(features, target)

