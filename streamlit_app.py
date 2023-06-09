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

#new section to display fruityvice api response

def get_fruityvice_data (this_fruit_choice):
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + this_fruit_choice)
    # normalise json into a flat table
    fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
    # converts data into a dataframe
    return fruityvice_normalized
  
  
streamlit.header("Fruityvice Fruit Advice!")
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
    streamlit.error("Please select a fruit to get information")
  else:
    back_from_function = get_fruityvice_data(fruit_choice)
    streamlit.dataframe(back_from_function)
 
except URLError as e:
  streamlit.error()

streamlit.header("View Our Fruit List- Add Your Favourites!")

def get_fruit_load_list():
  with my_cnx.cursor() as my_cur:
    my_cur.execute("SELECT * FROM fruit_load_list")
    return my_cur.fetchall()

#add a button to load the fruit
if streamlit.button('Get Fruit List'):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  my_data_rows = get_fruit_load_list()
  my_cnx.close()
  streamlit.dataframe(my_data_rows)

def insert_row_snowflake(new_fruit):
  with my_cnx.cursor() as my_cur:
    my_cur.execute("insert into fruit_load_list values ('"+ new_fruit + "')")
    return "Thanks for adding " + new_fruit

fruit_choice2 = streamlit.text_input('What fruit would you like to add?')
if streamlit.button('Add a Fruit to the list'):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  back_from_function = insert_row_snowflake(fruit_choice2)
  streamlit.text(back_from_function)
  
streamlit.stop()

fruit_choice2 = streamlit.text_input('What fruit would you like to add?')
streamlit.write('Thanks for adding ', fruit_choice2)

#this will not work for now
my_cur.execute("insert into fruit_load_list values ('test')")
