import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px


def shorten_categories(categories, cutoff):
    categorical_map = {}
    for i in range(len(categories)):
        if categories.values[i] >= cutoff:
            categorical_map[categories.index[i]] = categories.index[i]
        else:
            categorical_map[categories.index[i]] = 'Other'
    return categorical_map


def clean_experience(x):
    if x == "More than 50 years":
        return 50
    if x == "Less than 1 year":
        return 0.5
    return float(x)


def clean_education(x):
    if 'Bachelor’s degree (B.A., B.S., B.Eng., etc.)' in x:
        return 'Bachelor’s degree'
    if 'Master’s degree (M.A., M.S., M.Eng., MBA, etc.)' in x:
        return 'Master’s degree'
    if   'Professional degree (JD, MD, etc.)' in x or  'Other doctoral degree (Ph.D., Ed.D., etc.)' in x:
        return 'Post grad'
    return 'Less than a Bachelors'


@st.cache_data
def load_data():
    df = pd.read_csv("survey_results_public.csv")
   
    df = df[["Country", "EdLevel", "YearsCode", "Employment", "ConvertedCompYearly"]]
    df = df.rename({"ConvertedCompYearly":"Salary"}, axis=1)

    df = df.drop("Employment", axis=1)
    df = df.dropna()
    
    country_map = shorten_categories(df.Country.value_counts(), 400)
    df["Country"] = df["Country"].map(country_map)

    df = df[df["Salary"] <= 500000]
    df = df[df["Salary"] >= 10000]
    df = df[df["Country"] != 'Other']
    
    df["YearsCode"] = df["YearsCode"].apply(clean_experience)

    df['EdLevel'] = df['EdLevel'].apply(clean_education)

    return df

df = load_data()


def show_explore_page():

    st.title("Explore Developer Salary")
    st.write('''### Stack Overflow Developer Survey 2020''')

    country_data = df["Country"].value_counts()

    fig, ax = plt.subplots(figsize = (12,7))
    ax.pie(country_data, labels = country_data.index, autopct="%1.1f%%", shadow= True, startangle= 30)
    ax.axis("equal")
    st.write("""#### Number of Data from different Countries""")
    st.pyplot(fig)


    st.write("""#### Mean Salary Based on Country""")
    bar_chart_data = df.groupby(["Country"])["Salary"].mean().sort_values(ascending=True)
    fig1 = px.bar(bar_chart_data)
    st.plotly_chart(fig1)

    st.write("""#### Mean Salary based on Experience""")
    line_chart_data = df.groupby(["YearsCode"])["Salary"].mean()
    fig3 = px.line(line_chart_data)
    st.plotly_chart(fig3)


