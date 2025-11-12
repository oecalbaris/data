# pip install "fastapi[standard]"

# To Run the Fast API Server -->  im Terminal :  uvicorn fastapi_model:app --reload



# Open in Browser: http://127.0.0.1:8000


import os
from pathlib import Path
import pickle

from sklearn.datasets import load_iris




os.chdir(Path(__file__).parent)

from fastapi import FastAPI


# Create the APP
app = FastAPI()


# Function for loading the model
def load_model():
    with open("./models/best_model.pkl", mode="rb") as file:
        model = pickle.load(file)
        return model

# Function for getting the iris name from int
def get_target_name(prediction:int):
    iris = load_iris()
    target_name = iris.target_names
    predicted_name = target_name[prediction]
    return predicted_name

@app.get("/")  # Main Domain Name www.apfel.com , local: 127.0.0.1
async def root():
    return {"message": "Welcome to Iris prediction system"}

@app.get("/irispredict")
def iris_predict(sepal_length: float, sepal_width: float, petal_length: float, petal_width: float):
    model = load_model()
    data = [[sepal_length, sepal_width, petal_length, petal_width]]
    prediction = model.predict(data)[0]
    species_name = get_target_name(prediction)
    return {"Prediction": species_name}


