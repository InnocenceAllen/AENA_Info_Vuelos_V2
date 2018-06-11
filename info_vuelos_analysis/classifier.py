from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

from info_vuelos_analysis import constants
from info_vuelos_analysis.model import DelayLevel


def prepare_data(data):
    # print(data.head())
    encoders = []
    company_encoder = preprocessing.LabelEncoder()
    company_encoder.fit(data['company'])
    plane_encoder = preprocessing.LabelEncoder()
    plane_encoder.fit(data['plane'])
    airport_encoder = preprocessing.LabelEncoder()
    airport_encoder.fit(data['airport'])
    weather_encoder = preprocessing.LabelEncoder()
    weather_encoder.fit(data['weather'])

    encoders.append(company_encoder)
    encoders.append(plane_encoder)
    encoders.append(airport_encoder)
    encoders.append(weather_encoder)

    features = data[['company', 'plane', 'airport', 'weather', 't_min', 't_max', 'time']].values
    for i in range(4):
        encoder = encoders[i]
        features[:, i] = encoder.transform(features[:, i])

    target = data['delay'].values

    # Make a train/test split using 30% test size
    X_train, X_test, y_train, y_test = train_test_split(features, target,
                                                        test_size=constants.TEST_SIZE,
                                                        random_state=constants.RANDOM_SEED)
    return X_train, X_test, y_train, y_test


def apply_knn_classifier(X_train, X_test, y_train, y_test):
    print("Applying Knn Classifier")
    # print("{} : {}".format(DelayLevel.NO_DELAY, len(y_test[y_test == DelayLevel.NO_DELAY.value])))
    # print("{} : {}".format(DelayLevel.LOW_DELAY, len(y_test[y_test == DelayLevel.LOW_DELAY.value])))
    # print("{} : {}".format(DelayLevel.MEDIUM_DELAY, len(y_test[y_test == DelayLevel.MEDIUM_DELAY.value])))
    # print("{} : {}".format(DelayLevel.HIGH_DELAY, len(y_test[y_test == DelayLevel.HIGH_DELAY.value])))
    # print("Total : {}".format(len(y_test)))
    model = KNeighborsClassifier(n_neighbors=3)
    model.fit(X_train, y_train)
    print("Training accuray: {}".format(model.score(X_train, y_train)))

    target = model.predict(X_test)
    # print("{} : {}".format(DelayLevel.NO_DELAY, len(target[target == DelayLevel.NO_DELAY.value])))
    # print("{} : {}".format(DelayLevel.LOW_DELAY, len(target[target == DelayLevel.LOW_DELAY.value])))
    # print("{} : {}".format(DelayLevel.MEDIUM_DELAY, len(target[target == DelayLevel.MEDIUM_DELAY.value])))
    # print("{} : {}".format(DelayLevel.HIGH_DELAY, len(target[target == DelayLevel.HIGH_DELAY.value])))
    # print("Total : {}".format(len(target)))
    print("Test accuray: {}".format(model.score(X_test, y_test)))


def classify(data):
    # clf = svm.SVC(gamma=0.001, C=100.)
    # clf.fit(features, target)
    return 0
