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
st.sidebar.markdown("**All recipes recommended can be found at [Food.com](https://www.food.com/?ref=nav)**")

st.title("Plates4U")
st.image("https://www.goya.com/media/4173/creole-spaghetti.jpg?quality=80")

st.header("Introduction")
st.write("With our hectic and unpredictable daily schedules, it can be easy to rely on convenient and unhealthy foods that detriment our health. Or oftentimes, indecisiveness in meal preparation can lead to monotonous and unenjoyable meals. Our goal is to generate recipes that are inspired by your favorite meals, and hopefully we can even suggest some new ones that you would like.")

st.header("Recipe Recommender")
st.write("Select your preferences below and hit generate to get your recipes!")

sample = pd.read_csv('sample.csv')

#Widgets
#cuisines = st.multiselect("What cuisine are you loooking for?", ('greek','southUS','filipino','indian','jamaican','spanish','italian','mexican','chinese','british','thai','vietnamese','cajun_creole','brazilian','french','japanese','irish','korean','moroccan','russian'))

#slider
#level = st.slider("What is your cooking mastery?",1,5)
#level = st.slider("What is the longest time you want to spend cooking?",1,65)

#ingredients = st.multiselect("Ingredients", ("Chicken", "Pasta", "Soy Sauce"))
#st.write("You selected", len(ingredients), "ingredients")

# Widget for user to input preferred cuisines
cuisines = st.multiselect("What cuisine are you loooking for?", (sample['cuisine'].unique()))

# Widget for user to input cooking duration preference
dura = st.radio("What is the longest time you want to spend cooking?", ("No Preference", "30 Minutes Or Less", "1 Hour Or Less", "2 Hours Or Less"))

# Widget for user to input how to sort recommendations
sortby = st.radio("Sort By", ("None", "Shortest cook time", "Least Calories", "Number of Ingredients", "Most Popular"))

# Widget for user to input number of recommendations to display
num_recs = st.number_input('How many recommendations would you like?', min_value =1, max_value = 15, value = 5)

# Widget for user to input ingredients
user_input = st.text_input("Ingredients")

#Recommender

def run_rec(userIn,samp):
    """
    Runs the recommender given userIn ingredients and a dataset.
    Returns dataframe with similarity score column appended in desc order
    """
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
    """
    Sorts a dataframe using a given column to sort by
    Returns sorted dataframe
    """
    if sortOrder == "Shortest cook time":
        dataset = dataset.sort_values(by=['minutes'], ascending = True)
    elif sortOrder == "Least Calories":
        dataset = dataset.sort_values(by=['calories'], ascending = True)
    elif sortOrder == "Number of Ingredients":
        dataset = dataset.sort_values(by=['n_ingredients'], ascending = True)
    elif sortOrder == "Most Popular":
        dataset = dataset.sort_values(by=['mean_rating'], ascending = False)
    return dataset

def filter_time(dataset,duration):
    """
    Filters a dataframe given a max cooking duration
    Returns recommendations excluding certain cooking durations
    """
    if duration == "30 Minutes Or Less":
        dataset = dataset[dataset['minutes'] <= 30]
    elif duration == "1 Hour Or Less":
        dataset = dataset[dataset['minutes'] <= 60]
    elif duration == "2 Hours Or Less":
        dataset = dataset[dataset['minutes'] <= 120]
    return dataset

# Widget for user to generate recommendations
generate = st.button("Generate my Recipes!")

# Once the user clicks the button...
if generate:
    if user_input:
        with st.spinner("Asking the head chef..."):
            #Run the recommender here
            recommendations = run_rec(user_input,sample)
        #This sleep is needed because the spinner animation drags on
        time.sleep(0.5)

        #If user exlucded any cuisines, filter them out
        if len(cuisines) > 0:
            recommendations = recommendations[recommendations['cuisine'].isin(cuisines)]

        recommendations = filter_time(recommendations, dura)
        recommendations = sort_col(recommendations,sortby)

        #Clean up appearance of the dataframe
        recommendations['name'] = recommendations['name'].str.capitalize()
        recommendations = recommendations.set_index('name').drop(columns=['sim'])
        recommendations['cuisine'] = recommendations['cuisine'].str.capitalize()
        recommendations = recommendations.rename(columns={'minutes': 'Minutes','ingredients': 'Ingredients','n_ingredients': '# Ingredients','calories': 'Calories','mean_rating': 'Mean Rating','cuisine': 'Cuisine'})

        #Only show first num_recs results according to user input
        recommendations = recommendations[:num_recs]

        st.success("Dinner is served!")

        #Round values to 2 decimal places for calories and 1 for mean rating
        st.table(recommendations.style.format({"Calories": "{:.2f}","Mean Rating": "{:.1f}"}))
        st.balloons()
    else:
        errorM = st.empty()
        errorM.error('Please Enter Ingredients Into The Search Field!')
        time.sleep(0.7)
        errorM.empty()
