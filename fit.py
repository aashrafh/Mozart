import cv2
import numpy as np
from box import Box
from train import *
import os
import pickle


def _match(img, templates, sscale, escale, thresh):
    count = -1
    locations = []
    final_scale = 1

    for scale in [s/100.0 for s in range(sscale, escale+1, 3)]:
        cur_locations = []
        cur_count = 0
        for template in templates:
            template = cv2.resize(template, None, fx=scale,
                                  fy=scale, interpolation=cv2.INTER_CUBIC)
            result = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)
            result = np.where(result >= thresh)
            cur_count += len(result[0])
            locations += [result]

        if cur_count > count:
            count = cur_count
            locations = cur_locations
            final_scale = scale
        elif cur_count < count:
            pass

    return locations, final_scale


def match(img, templates, sscale, escale, thresh):
    locations, scale = _match(img, templates, sscale, escale, thresh)
    img_locations = []
    for i in range(len(templates)):
        w, h = templates[i].shape[::-1]
        w *= scale
        h *= scale
        img_locations.append([Box(pt[0], pt[1], w, h)
                              for pt in zip(*locations[i][::-1])])
    return img_locations


def remove_repeated_matches(recs, threshold):
    filtered_recs = []
    while len(recs) > 0:
        r = recs.pop(0)
        recs.sort(key=lambda rec: rec.distance(r))
        overlapped = True
        while(overlapped):
            overlapped = False
            i = 0
            for _ in range(len(recs)):
                if r.overlap(recs[i]) > threshold or recs[i].overlap(r) > threshold:
                    r = r.merge(recs.pop(i))
                    overlapped = True
                elif recs[i].distance(r) > r.w/2 + recs[i].w/2:
                    break
                else:
                    i += 1
        filtered_recs.append(r)
    return filtered_recs


def predict(img):
    # if not os.path.exists('trained_models/svm_trained_model_hog.sav'):
    #     print('Please wait while training the SVM-HOG model....')
    #     train('SVM', 'hog', 'svm_trained_model_hog')
    # if not os.path.exists('trained_models/svm_trained_model_raw.sav'):
    #     print('Please wait while training the SVM-RAW model....')
    #     train('SVM', 'raw', 'svm_trained_model_raw')
    if not os.path.exists('trained_models/nn_trained_model_hog.sav'):
        print('Please wait while training the NN-HOG model....')
        train('NN', 'hog', 'nn_trained_model_hog')

    # models = [pickle.load(open('trained_models/svm_trained_model_hog.sav', 'rb')), pickle.load(open(
    #     'trained_models/svm_trained_model_raw.sav', 'rb')), pickle.load(open('trained_models/nn_trained_model_hog.sav', 'rb'))]
    # models_feature = ['hog', 'raw', 'hog']

    # features = extract_features(img, models_feature[0])
    # labels = models[0].predict([features])
    # print(np.max(models[0].decision_function([features])), labels)

    # features = extract_features(img, models_feature[1])
    # labels = models[1].predict([features])
    # print(np.max(models[1].decision_function([features])), labels)

    model = pickle.load(open('trained_models/nn_trained_model_hog.sav', 'rb'))
    features = extract_features(img, 'hog')
    labels = model.predict([features])
    # print(np.max(models[2].predict_proba([features])), labels)
    return labels


if __name__ == "__main__":
    img = cv2.imread('testresult/0_6.png')
    labels = predict(img)
    print(labels)
