import os
import streamlit as st
from flask import Flask, render_template, request, redirect
#from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
#db = SQLAlchemy(app)

#class Todo(db.Model):
#    id = db.Column(db.Integer, primary_key=True)
#    content = db.Column(db.String(200), nullable=False)
#    date_created = db.Column(db.DateTime, default=datetime.utcnow)

#    def __repr__(self):
#        return '<Task %r>' % self.id

@app.route('/')#, methods=['POST','GET'])
def hello():
#    return "Hello Team!"
#    return render_template('index.html')
#    return render_template('example.html')
#    return render_template('trial.html')

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

    st.button("Generate my Recipes!")
    if st.button:
        st.write(run_rec())
        st.balloons()

#if __name__ == "__main__":
#    app.run(debug=True)