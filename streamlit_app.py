import streamlit as st
import pandas as pd
import requests
import snowflake.connector
from urllib.error import URLError 

st.title('My Moms New Healthy Diner')
st.header('Breakfast Favorites')
st.text('🥣 Omega 3 and Blueberry Oatmeal')
st.text('🥗 Kale, Spinach and Rocket Smoothie')
st.text('🐔 Hard-Boiled, Free-Range Egg')
st.text('🥑🍞 Avocado Toast')

st.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')
my_fruit_list = pd.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

fruits_selected = st.multiselect("Pick Some Fruits:", list(my_fruit_list.index), ['Banana', 'Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]
st.dataframe(fruits_to_show)

st.header("Fruityvice Fruit Advice!")
def get_fruityvice_data(this_fruit_choice):
  fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + this_fruit_choice)
  fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
  return fruityvice_normalized
    
try:
  fruit_choice = st.text_input('What fruit would you like information about?')
  if not fruit_choice:
      st.error("Please select a fruit to get information")
  else:
      back_from_function = get_fruityvice_data(fruit_choice)
      st.dataframe(back_from_function)

except URLError as e:
  st.error()

st.header("The Fruit Load List contains:")

def get_fruit_load_list():
  with my_cnx.cursor() as my_cur:
       my_cur.execute("select distinct * from fruit_load_list")
       return my_cur.fetchall()

if st.button('Get Fruit Load List'):
  my_cnx = snowflake.connector.connect(**st.secrets["snowflake"])
  ret_fruit_load = get_fruit_load_list()
  st.dataframe(ret_fruit_load)

fruit_to_add = st.text_input("What Fruit Would You Like to Add?")
st.write('Thanks for Adding', fruit_to_add)

my_cur.execute("insert into fruit_load_list values" (fruit_to_add) )


