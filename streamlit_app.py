import streamlit
import pandas as pd
import snowflake.connector
import requests
from urllib.error import URLError

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

streamlit.header("Fruityvice Fruit Advice!")

try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
    streamlit.error("Please select a fruit to get information")
  else:
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
    # normalise json into a flat table
    fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
    # converts data into a dataframe
    streamlit.dataframe(fruityvice_normalized)
 
except URLError as e:
  streamlit.error()


streamlit.stop()

my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("SELECT * FROM fruit_load_list")
my_data_rows = my_cur.fetchall()
streamlit.header("The fruit load list contains:")
streamlit.dataframe(my_data_rows)


fruit_choice2 = streamlit.text_input('What fruit would you like to add?')
streamlit.write('Thanks for adding ', fruit_choice2)

#this will not work for now
my_cur.execute("insert into fruit_load_list values ('test')")
