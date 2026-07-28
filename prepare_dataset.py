import json
import os
import csv
import numpy as np


ANNOTATION_PATH = "archive/ann_train_val"

GESTURES = {
    "fist": "fist",
    "palm": "open_palm",
    "one": "point",
    "peace": "peace",
    "like": "thumbs_up",
    "dislike": "thumbs_down",
    "ok": "pinch"
}


OUTPUT_FILE = "gesture_landmarks.csv"



def normalize_landmarks(points):

    points = np.array(points)


    # wrist origin
    points = points - points[0]


    # scale normalization
    scale = np.linalg.norm(points[9])

    if scale > 0:
        points = points / scale


    features = points.flatten().tolist()



    def dist(a,b):
        return np.linalg.norm(points[a]-points[b])


    # Important pinch features
    distances = [

        dist(4,8),    # thumb-index

        dist(4,12),   # thumb-middle

        dist(4,16),

        dist(4,20),

        dist(8,12),

        dist(12,16),

        dist(16,20)

    ]


    features.extend(distances)


    return features




def process_json(path,label):

    samples=[]


    with open(path) as f:
        data=json.load(f)



    for item in data.values():

        if "landmarks" not in item:
            continue


        hand=item["landmarks"][0]


        if len(hand)!=21:
            continue



        features=normalize_landmarks(hand)


        samples.append(
            [label]+features
        )


    print(
        label,
        len(samples)
    )


    return samples




samples=[]


for file,label in GESTURES.items():

    path=os.path.join(
        ANNOTATION_PATH,
        file+".json"
    )


    samples.extend(
        process_json(
            path,
            label
        )
    )



header=["label"]


for i in range(21):

    header += [
        f"x{i}",
        f"y{i}"
    ]



header += [

"thumb_index_dist",
"thumb_middle_dist",
"thumb_ring_dist",
"thumb_pinky_dist",
"index_middle_dist",
"middle_ring_dist",
"ring_pinky_dist"

]



with open(
    OUTPUT_FILE,
    "w",
    newline=""
) as f:

    writer=csv.writer(f)

    writer.writerow(header)

    writer.writerows(samples)



print()
print("Dataset created")
print("Samples:",len(samples))