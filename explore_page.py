import  streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def sorten_categories(categories, cutoff):
    categorical_map={}
    for i in range(len(categories)):
        if categories.values[i]>= cutoff:
            categorical_map[categories.index[i]]= categories.index[i]
        else:
            categorical_map[categories.index[i]]= "Autre"
    return categorical_map

def clean_experience(x):
    if x == 'More than 50 years':
        return 50
    if x == 'Less than 1 year':
        return 0.5
    return float(x)

def clean_education(x):
    if 'Bachelor’s degree' in x:
        return "Bachelor / Licence"
    if "Master’s degree" in x:
        return "Master"
    if "Professional degree" in x or "Other doctoral" in x:
        return "Post Master"
    return "Inférieur au Bachelor"

@st.cache
def load_data():
    df = pd.read_csv("survey_results_public.csv")
    df = df[["Country", "EdLevel", 'Employment', "YearsCodePro", "ConvertedCompYearly"]]
    df = df.rename({"Country": "Pays", "EdLevel": "Niveau d'étude", "Employment": "Type d'emploi",
                    "YearsCodePro": "Année(s) d'expérience", "ConvertedCompYearly": "Salaire"}, axis=1)
    df = df[df["Salaire"].notnull()]
    df.dropna(inplace=True)
    df = df[df["Type d'emploi"] == "Employed, full-time"]
    df = df.drop("Type d'emploi", axis=1)

    country_map = sorten_categories(df.Pays.value_counts(), 400)
    df["Pays"] = df.Pays.map(country_map)

    df = df[(df["Salaire"] >= 10000)]
    df = df[df["Salaire"] <= 250000]
    df = df[df["Pays"] != "Autre"]

    df["Année(s) d'expérience"] = df["Année(s) d'expérience"].apply(clean_experience)
    df["Niveau d'étude"] = df["Niveau d'étude"].apply(clean_education)

    return df
df=load_data()

def show_explore_page():
    st.title("Salaires des Data Scientist dans le monde")


    data = df["Pays"].value_counts()

    fig1, ax1 = plt.subplots()
    ax1.pie(data, labels=data.index, autopct="%1.1f%%", shadow=True, startangle=90)
    ax1.axis("equal")

    st.write("""### Nombre de salaires renseignés par pays""")
    st.pyplot(fig1)

    st.write(
        """
        ### Salaire moyen par pays
        """
    )

    data = df.groupby(["Pays"])["Salaire"].mean().sort_values(ascending=True)
    st.bar_chart(data)

