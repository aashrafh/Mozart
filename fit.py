import cv2
import numpy as np
from box import Box


def fit(img, templates, sscale, escale, thresh):
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
    locations, scale = fit(img, templates, sscale, escale, thresh)
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
        merged = True
        while(merged):
            merged = False
            i = 0
            for _ in range(len(recs)):
                if r.overlap(recs[i]) > threshold or recs[i].overlap(r) > threshold:
                    r = r.merge(recs.pop(i))
                    merged = True
                elif recs[i].distance(r) > r.w/2 + recs[i].w/2:
                    break
                else:
                    i += 1
        filtered_recs.append(r)
    return filtered_recs
