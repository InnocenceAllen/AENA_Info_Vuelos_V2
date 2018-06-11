from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
import matplotlib.pyplot as plt
import numpy as np
import logging as log

from sklearn.preprocessing import OneHotEncoder

from info_vuelos_analysis.model import DelayLevel


def dataset_split(features, target, test_size, random_seed):
    # Make a train/test split using predefined test size and seed
    return train_test_split(features, target, test_size=test_size, random_state=random_seed)


def encode_cat_ordinals(data):
    log.info("Applying Label Encoder to categorical features")
    encoders = []
    features = data[['company', 'plane', 'airport', 'weather', 't_min', 't_max', 'time']].values
    for i in range(4):
        encoder = LabelEncoder()
        encoder.fit(features[:, i])
        features[:, i] = encoder.transform(features[:, i])
        encoders.append(encoder)

    target = data['delay'].values

    return features, target


def encode_cat_one_hot(data):
    log.info("Applying OneHot Encoder to categorical features")
    features, target = encode_cat_ordinals(data)
    categorical_features = range(4)
    encoder = OneHotEncoder(categorical_features=categorical_features, handle_unknown='error')
    one_hot_features = encoder.fit_transform(features)
    target = data['delay'].values
    return one_hot_features, target


def scale_data(data):
    log.info("Applying Scaling to features")
    scaler = StandardScaler(copy=False)
    scaled_data = scaler.fit_transform(data)
    return scaled_data


def apply_knn_classifier(X_train, X_test, y_train, y_test):
    log.info("Applying Knn Classifier")
    # print("{} : {}".format(DelayLevel.NO_DELAY, len(y_test[y_test == DelayLevel.NO_DELAY.value])))
    # print("{} : {}".format(DelayLevel.LOW_DELAY, len(y_test[y_test == DelayLevel.LOW_DELAY.value])))
    # print("{} : {}".format(DelayLevel.MEDIUM_DELAY, len(y_test[y_test == DelayLevel.MEDIUM_DELAY.value])))
    # print("{} : {}".format(DelayLevel.HIGH_DELAY, len(y_test[y_test == DelayLevel.HIGH_DELAY.value])))
    # print("Total : {}".format(len(y_test)))
    model = KNeighborsClassifier(n_neighbors=3)
    model.fit(X_train, y_train)
    log.info("Training accuray: {}".format(model.score(X_train, y_train)))

    target = model.predict(X_test)
    # print("{} : {}".format(DelayLevel.NO_DELAY, len(target[target == DelayLevel.NO_DELAY.value])))
    # print("{} : {}".format(DelayLevel.LOW_DELAY, len(target[target == DelayLevel.LOW_DELAY.value])))
    # print("{} : {}".format(DelayLevel.MEDIUM_DELAY, len(target[target == DelayLevel.MEDIUM_DELAY.value])))
    # print("{} : {}".format(DelayLevel.HIGH_DELAY, len(target[target == DelayLevel.HIGH_DELAY.value])))
    # print("Total : {}".format(len(target)))
    log.info("Test accuray: {}".format(model.score(X_test, y_test)))
    accuracy_plot(X_train, y_train, model, 'Training')
    accuracy_plot(X_test, y_test, model, 'Testing')


def accuracy_plot(features, target, model, concept):
    # Find the training and testing accuracies by target value (delay encoded as DelayLevel)
    scores = dict()
    for delay in DelayLevel:
        scores[delay.name] = model.score(features[target == delay.value], target[target == delay.value])

    # Plot the scores as a bar chart
    plt.figure()
    bars = plt.bar(np.arange(4), scores.values(), color=['g', 'b', 'y', 'r'])

    # directly label the score onto the bars
    for bar in bars:
        height = bar.get_height()
        plt.gca().text(bar.get_x() + bar.get_width() / 2, height * .90, '{0:.{1}f}'.format(height, 2),
                       ha='center', color='w', fontsize=11)
    # remove the frame of the chart
    for spine in plt.gca().spines.values():
        spine.set_visible(False)
    plt.xticks([0, 1, 2, 3], scores.keys(), alpha=0.8);
    plt.title('Accuracies predicting Delay Levels at {}'.format(concept), alpha=0.8)
    plt.show()


def classify(data):
    # clf = svm.SVC(gamma=0.001, C=100.)
    # clf.fit(features, target)
    return 0
