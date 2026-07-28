import pandas as pd
import joblib


from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report



df=pd.read_csv(
    "gesture_landmarks.csv"
)



X=df.drop(
    "label",
    axis=1
)


y=df["label"]



X_train,X_test,y_train,y_test=train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)



model=RandomForestClassifier(

    n_estimators=300,

    max_depth=25,

    random_state=42,

    n_jobs=-1

)



print("Training...")


model.fit(
    X_train,
    y_train
)



pred=model.predict(
    X_test
)



print(
    classification_report(
        y_test,
        pred
    )
)



joblib.dump(
    model,
    "gesture_model.pkl"
)



print(
"Saved gesture_model.pkl"
)