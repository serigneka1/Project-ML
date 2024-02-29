import streamlit as st
import pickle
import numpy as np

def load_model():
    with open('saved_steps.pkl', 'rb') as file:
        data = pickle.load(file)
    return data
data = load_model()

regressor=data["model"]
le_country=data["le_country"]
le_education=data["le_education"]

def show_predict_page():
    st.title("Prédiction de salaire pour les data scientist")

    st.write("""Il faut fournir quelques informations pour prédire le salaire""")

    countries = (
        'France',
        'Sweden',
        'Canada',
        'Spain',
        'Italy',
        'United States of America',
        'Germany',
        'Poland',
        'Brazil',
        'India',
        'Switzerland',
        'Australia',
        'Russian Federation',
        'Netherlands',
        'United Kingdom of Great Britain and Northern Ireland',
    )

    education = (
        'Inférieur au Bachelor',
        'Bachelor / Licence',
        'Master',
        'Post Master',

    )

    country = st.selectbox("Pays",countries)
    education = st.selectbox("education", education)
    experience = st.slider("Années d'expérience", 0, 50, 3)


    ok = st.button("Calculer le salaire")
    if ok:
        X = np.array([[country, education, experience]])
        X[:, 0] = le_country.transform(X[:, 0])
        X[:, 1] = le_education.transform(X[:, 1])
        X = X.astype(float)
        salary= regressor.predict(X)
        st.subheader(f"Le salaire est estimé à {salary[0]:.2f} €")
