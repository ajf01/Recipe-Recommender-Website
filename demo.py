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
about_text="Food is the perfect gateway to introduce yourself to the variety of cuisines that there are to experience, and cooking recipes is one way that we can engage with the cultures that they come from."
st.sidebar.markdown(about_text)

st.title("Personalized-Plates")
st.image("https://www.goya.com/media/4173/creole-spaghetti.jpg?quality=80")

st.header("Introduction")
st.write("With our hectic and unpredictable daily schedules, it can be easy to rely on convenient and unhealthy foods that detriment our health. Or oftentimes, indecisiveness in meal preparation can lead to monotonous and unenjoyable meals. Our goal is to generate recipes that are inspired by your favorite meals, and hopefully we can even suggest some new ones that you would like.")



st.header("Recipe Recommender")
st.write("Select your preferences below and hit generate to get your recipes!")


sample = pd.read_csv('sample.csv')

#Widgets
#cuisines = st.multiselect("What cuisine are you loooking for?", ('greek','southUS','filipino','indian','jamaican','spanish','italian','mexican','chinese','british','thai','vietnamese','cajun_creole','brazilian','french','japanese','irish','korean','moroccan','russian'))
cuisines = st.multiselect("What cuisine are you loooking for?", (sample['cuisine'].unique()))

#slider
#level = st.slider("What is your cooking mastery?",1,5)
level = st.slider("What is the longest time you want to spend cooking?",1,65)

sortby = st.radio("Sort By", ("None", "Shortest cook time", "Least Calories", "Number of Ingredients", "Most Popular"))

#ingredients = st.multiselect("Ingredients", ("Chicken", "Pasta", "Soy Sauce"))
#st.write("You selected", len(ingredients), "ingredients")

#st.write("Select Your Allergies")
#st.checkbox("Peanuts")
#st.checkbox("Fish")
#st.checkbox("Egg")

#Recommender
def run_rec(userIn,samp):
    with open('test_set.data', 'rb') as filehandle:
    # read the data as binary data stream
        test = pickle.load(filehandle)

    mlb = MultiLabelBinarizer()
    mlb.fit(test)
    
    if userIn:
        # Turn input into a proper list of lists
        input_vector = [[x.strip().lower() for x in userIn.split(",")]]
    
    ingredients_transformed = mlb.transform(test)
    recipe_test_trans = mlb.transform(input_vector)

    sims = []
    for recipe in ingredients_transformed:
        sim = cosine_similarity(recipe_test_trans,recipe.reshape(-1,len(recipe)))
        sims.append(sim)

    samp['sim'] = [x[0][0] for x in sims]

    return samp.sort_values('sim',ascending=False)

def sort_col(dataset,sortOrder):
    if sortOrder == "Shortest cook time":
        dataset = dataset.sort_values(by=['minutes'], ascending = True)
    elif sortOrder == "Least Calories":
        dataset = dataset.sort_values(by=['calories'], ascending = True)
    elif sortOrder == "Number of Ingredients":
        dataset = dataset.sort_values(by=['n_ingredients'], ascending = True)
    elif sortOrder == "Most Popular":
        dataset = dataset.sort_values(by=['mean_rating'], ascending = False)
    return dataset

user_input = st.text_input("Ingredients")
generate = st.button("Generate my Recipes!")
if generate:
    if user_input:
        with st.spinner("Asking the head chef..."):
            #Run the recommender here
            recommendations = run_rec(user_input,sample)
        #This sleep is needed because the spinner animation drags on
        time.sleep(0.5)
        if len(cuisines) > 0:
            recommendations = recommendations[recommendations['cuisine'].isin(cuisines)]
        recommendations = recommendations.set_index('name')[:5]
        recommendations = sort_col(recommendations,sortby)
        st.success("Dinner is served!")
        st.table(recommendations)
        st.balloons()
    else:
        errorM = st.empty()
        errorM.error('Please Enter Ingredients Into The Search Field!')
        time.sleep(0.7)
        errorM.empty()
