
# First: run the py file
# second: python -m streamlit run streamlit_model.py

import streamlit as st
import requests


url = "http://127.0.0.1:8000/irispredict"


def main():

    st.markdown("Predict iris flower")


    # input field
    sepal_length = st.number_input("Sepal Length (cm)", min_value= 4.01, max_value = 8.49, value = 5.4)
    sepal_width = st.number_input("Sepal Width (cm)", min_value= 2.01, max_value = 4.40, value = 3.4)
    petal_length = st.number_input("Petal Length (cm)", min_value= 1.01, max_value = 7.00, value = 1.3)
    petal_width = st.number_input("Petal Width (cm)", min_value= 0.11, max_value = 2.50, value = 0.2)

    #button for prediction
    if st.button("Predict"):

        response = requests.get(url,params={"sepal_length":sepal_length,"sepal_width":sepal_width,"petal_length":petal_length,"petal_width":petal_width})
        prediction = response.json()

        st.write(f"The predicted flower is: {prediction['Prediction']}")

if __name__ == "__main__":
    main()