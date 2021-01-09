import cv2
import random
import imutils
from glob import glob
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
from sklearn import svm
import numpy as np
import matplotlib.pyplot as plt
import pickle


target_img_size = (100, 100)
sample_count = 350


def extract_raw_pixels(img):
    resized = cv2.resize(img, target_img_size)
    return resized.flatten()


def extract_hsv_histogram(img):
    resized = cv2.resize(img, target_img_size)
    hsv = cv2.cvtColor(resized, cv2.COLOR_BGR2HSV)
    hist = cv2.calcHist([hsv], [0, 1, 2], None, [8, 8, 8],
                        [0, 180, 0, 256, 0, 256])
    if imutils.is_cv2():
        hist = cv2.normalize(hist)
    else:
        cv2.normalize(hist, hist)
    return hist.flatten()


def extract_features(img, feature_set='raw'):
    if feature_set == 'hog':
        return extract_hog_features(img)
    elif feature_set == 'raw':
        return extract_raw_pixels(img)
    else:
        return extract_hsv_histogram(img)


def load_dataset(feature_set='raw', dir_names):
    features = []
    labels = []
    for dir_name in dir_names:
        print(dir_name)
        imgs = glob(f'{dataset_path}/{dir_name}/*.png')
        subset = random.sample([i for i in range(len(imgs))], sample_count)
        for i in subset:
            img = cv2.imread(imgs[i])
            labels.append(dir_name)
            features.append(extract_features(img, feature_set))

    return features, labels


def load_classifiers():
    random_seed = 42
    random.seed(random_seed)
    np.random.seed(random_seed)

    classifiers = {
        'SVM': svm.LinearSVC(random_state=random_seed),
        'KNN': KNeighborsClassifier(n_neighbors=7),
        'NN': MLPClassifier(solver='sgd', random_state=random_seed, hidden_layer_sizes=(500,), max_iter=20, verbose=1)
    }
    return classifiers


def run_experiment(classifier='SVM', feature_set='hog', dir_names=[]):
    print('Loading dataset. This will take time ...')
    features, labels = load_dataset(feature_set, dir_names)
    print('Finished loading dataset.')

    train_features, test_features, train_labels, test_labels = train_test_split(
        features, labels, test_size=0.2, random_state=random_seed)

    classifiers = load_classifiers()

    model = classifiers[classifier]
    print('############## Training', classifier, "##############")
    model.fit(train_features, train_labels)
    accuracy = model.score(test_features, test_labels)
    print(classifier, 'accuracy:', accuracy*100, '%')

    return model, accuracy


def train(model_name, feature_name, saved_model_name):
    dataset_path = 'train_data/data'
    dir_names = [path.split('/')[2] for path in glob(f'{dataset_path}/*')]

    model, accuracy = run_experiment(model_name, feature_name)

    filename = f'trained_models/{saved_model_name}.sav'
    pickle.dump(model, open(filename, 'wb'))


if __name__ == "__main__":
    train('SVM', 'hog', 'svm_trained_model_hog')
