import streamlit as st

#sidebars
st.sidebar.header("About")
st.sidebar.text("Food is the perfect gateway to introduce oneself to the variety of cuisines that there are to experience, and cooking recipes is just one way through which we can engage with those cultures that they come from.")

st.title("Personalized-Plates")

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


st.checkbox("Peanuts")
st.checkbox("Fish")
st.checkbox("Egg")





#I think this is where the recommender goes 

def run_rec():
    return 123456789

st.button("Generate my Recipes!")
if st.button("Generate my Recipes!"):
    st.write(run_rec())
    st.balloons()
