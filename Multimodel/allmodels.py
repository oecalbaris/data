from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split, StratifiedKFold
from sklearn.linear_model import LogisticRegression
import pandas as pd
import pickle
from sklearn.datasets import load_iris
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import Pipeline
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.preprocessing import StandardScaler

# load Iris dataset
data = load_iris(as_frame=True)
df = data.frame

#define target and features
X= df.drop(columns=['target'])
y= df['target']

# Test train split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)




# define models and hyper parameters
models = {
    "logisticregression": {
        "model": Pipeline([
            ("scaler", StandardScaler()),
            ("classifier", LogisticRegression())
        ]),
        "params": {
            'classifier__penalty': ['l2'],
            'classifier__solver': ['lbfgs', 'newton-cg'],
            'classifier__max_iter': [100, 1000, 2500, 5000]
        }
    },

    "randomforest": {
        "model": Pipeline([
            ("scaler", StandardScaler()),
            ("classifier", RandomForestClassifier())
        ]),
        "params": {
            'classifier__n_estimators': [20, 100, 200],
            'classifier__max_depth': [None, 10, 20],
            'classifier__min_samples_split': [2, 5],
            'classifier__min_samples_leaf': [1, 2],
            'classifier__bootstrap': [True, False]
        }
    },

    "decisiontree": {
        "model": Pipeline([
            ("scaler", StandardScaler()),
            ("classifier", DecisionTreeClassifier())
        ]),
        "params": {
            'classifier__max_depth': [10, 20, 30, None],
            'classifier__min_samples_split': [2, 5, 10],
            'classifier__min_samples_leaf': [1, 2, 4]
        }
    },

    "KNN": {
        "model": Pipeline([
            ("scaler", StandardScaler()),
            ("classifier", KNeighborsClassifier())
        ]),
        "params": {
            'classifier__n_neighbors': [5, 7, 9, 11, 13, 15],
            'classifier__weights': ['uniform', 'distance'],
            'classifier__metric': ['minkowski', 'euclidean', 'manhattan']
        }
    }
}

#Create K,folds
stratified_kfold = StratifiedKFold(n_splits = 10, shuffle = True)





model_summary = []
best_model_name = ""
best_model = None
best_accuracy = 0.0

for name, para in models.items():


    model = GridSearchCV(estimator=para["model"], param_grid =para["params"], cv=stratified_kfold, n_jobs=1, verbose=1)
    model.fit(X_train, y_train)


    #getting the accuracy
    best_estimator = model.best_estimator_
    y_pred = best_estimator.predict(X_test)
    acc = accuracy_score(y_test, y_pred)

    print(f"Best parameters for {name}:{model.best_params_}")
    print(f"Accuracy score for {name} with best parameters: {acc}")

    # prints the modelling results. Also save them as csv.
    df = pd.DataFrame(model.cv_results_)
    print(df.head())
    model_summary.append(df)
    df.to_csv(f"./models/{name}_summary.csv", index=False)

    #Saving all the models in pickle
    with open(f"./models/{name}_v1.pkl", mode = "wb") as file:
        pickle.dump(model.best_estimator_, file)

    # getting the best accuracy and name of the model
    if acc > best_accuracy:
        best_accuracy = acc
        best_model = best_estimator
        best_model_name = name

# Save best model separately
with open("models/best_model.pkl", "wb") as file2:
    pickle.dump(best_model, file2)

