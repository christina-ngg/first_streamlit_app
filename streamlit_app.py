import streamlit
import pandas as pd

streamlit.title("My Parents' New Healthy Diner")
streamlit.header('Breakfast Menu')
streamlit.text('Omega 3 & Blueberry Oatmeal')
streamlit.text('Kale, Spinach & Rocket Smoothie')
streamlit.text('Hard-Boiled Free-Range Egg')


streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')
my_fruit_list = pd.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')


#select fruit
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado', 'Strawberries'])

#selected fruit shown on table
fruits_to_show = my_fruit_list.loc[fruits_selected]

if len(fruits_selected) >0:
  streamlit.dataframe(fruits_to_show)
else:
  streamlit.dataframe(my_fruit_list)

  
import requests
streamlit.header("Fruityvice Fruit Advice!")
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")

# normalise json into a flat table
fruityvice_normalized = pd.json_normalize(fruityvice_response.json())

# converts data into a dataframe
streamlit.dataframe(fruityvice_normalized)
