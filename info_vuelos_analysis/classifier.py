from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.gaussian_process import GaussianProcessClassifier
from sklearn.gaussian_process.kernels import RBF
from sklearn.naive_bayes import GaussianNB
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
import matplotlib.pyplot as plt
import numpy as np
import logging as log

from sklearn.preprocessing import OneHotEncoder
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier

from info_vuelos_analysis.model import DelayLevel

names = ['Nearest Neighbors', 'Linear SVM', 'RBF SVM',
         # 'Gaussian Process',
         'Decision Tree', 'Random Forest', 'Neural Net', 'AdaBoost',
         'Naive Bayes', 'QDA']
no_sparse = ['Naive Bayes', 'QDA']

classifiers = [
    KNeighborsClassifier(3),
    SVC(kernel='linear', C=0.025),
    SVC(),
    # GaussianProcessClassifier(1.0 * RBF(1.0)),
    DecisionTreeClassifier(),
    RandomForestClassifier(),
    MLPClassifier(activation='logistic', solver='sgd', learning_rate='adaptive'),
    AdaBoostClassifier(),
    GaussianNB(),
    QuadraticDiscriminantAnalysis()]


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


def apply_classifiers(X_train, X_test, y_train, y_test, concept, sparse=False):
    scores = []
    for name, model in zip(names, classifiers):
        log.info("Applyng {} classifier".format(name))
        if not sparse or not name in no_sparse:
            model.fit(X_train, y_train)
            test_score = model.score(X_test, y_test)
            train_score = model.score(X_train, y_train)
            scores.append(test_score)
            log.info("Training accuray for {} = {}".format(name, train_score))
            log.info("Test accuray for {} = {}".format(name, test_score))
            # accuracy_plot(X_train, y_train, model, name, concept)
            accuracy_plot(X_test, y_test, model, name, concept)
    accuracy_comparison_plot(scores, concept)


def accuracy_plot(features, target, model, model_name, set):
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
    plt.title('{} Accuracy predicting Delay Levels ({})'.format(model_name, set), alpha=0.8)
    plt.show()


def accuracy_comparison_plot(scores, concept):
    plt.figure()
    plt.plot(scores)
    plt.ylabel('Accuracy')
    plt.xlabel('Classifier')
    # plt.xticks(names)
    plt.title("Comparison of testing accuracy for multiple classifiers\n{}".format(concept))
    plt.show()
