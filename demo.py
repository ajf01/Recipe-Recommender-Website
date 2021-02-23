import streamlit as st
import time

import pandas as pd
import os
import numpy as np
import pickle

from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.metrics.pairwise import cosine_similarity

#sidebars
st.sidebar.header("About")
about_text="Food is the perfect gateway to introduce oneself to the variety of cuisines that there are to experience, and cooking recipes is just one way through which we can engage with those cultures that they come from."
st.sidebar.markdown(about_text)

st.title("Personalized-Plates")
st.image("https://www.goya.com/media/4173/creole-spaghetti.jpg?quality=80")

st.header("Introduction")
st.write("With our hectic and unpredictable daily schedules, it can be easy to rely on convenient and unhealthy foods that detriment our health. Or oftentimes, indecisiveness in meal preparation can lead to monotonous and unenjoyable meals. Our goal is to generate recipes that are inspired by your favorite meals, and hopefully we can even suggest some new ones that you would like.")



st.header("Recipe Recommender")
st.write("Select your preferences below and hit generate to get your recipes!")


#Widgets

cuisines = st.radio("What cuisine are you loooking for?", ("Italian", "Asian", "Mexican", "Mediterranean"))

#slider
level = st.slider("What is your cooking mastery?",1,5)

sortby = st.radio("Sort By", ("Shortest cook time", "Least Calories", "Most Popular"))

sort_by_selectbox = st.selectbox("Sort By", ["Shortest cook time", "Least Calories", "Most Popular"])

ingredients = st.multiselect("Ingredients", ("Chicken", "Pasta", "Soy Sauce"))
st.write("You selected", len(ingredients), "ingredients")

st.write("Select Your Allergies")
st.checkbox("Peanuts")
st.checkbox("Fish")
st.checkbox("Egg")


#I think this is where the recommender goes 

def run_rec(user_input):
    sample = pd.read_csv('sample.csv')
    with open('test_set.data', 'rb') as filehandle:
    # read the data as binary data stream
        test = pickle.load(filehandle)

    mlb = MultiLabelBinarizer()
    mlb.fit(test)
    
    #User Input
    #recipe_test = [['sugar', 'unsalted butter', 'bananas', 'eggs','fresh lemon juice']]
    
    if user_input:
        # Turn input into a proper list of lists
        input_vector = [[x.strip() for x in user_input.split(",")]]
    
    ingredients_transformed = mlb.transform(test)
    recipe_test_trans = mlb.transform(input_vector)

    sims = []
    for recipe in ingredients_transformed:
        sim = cosine_similarity(recipe_test_trans,recipe.reshape(-1,5333))
        sims.append(sim)

    sample['sims'] = sims
    sample['sims_unpacked'] = sample['sims'].apply(lambda x: x[0][0])

    st.table(sample.sort_values('sims_unpacked',ascending=False)[:5])
    return

user_input = st.text_input("Ingredients")
generate = st.button("Generate my Recipes!")
if generate:
    with st.spinner("Asking the head chef..."):
        #Run the recommender here
        run_rec(user_input)
    #This sleep is needed because the spinner animation drags on
    time.sleep(0.5)
    st.success("Dinner is served!")
    st.balloons()
