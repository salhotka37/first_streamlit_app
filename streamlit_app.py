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

fruit_choice = st.text_input('What fruit would you like information about?', 'Apple')
st.write('The user entered', fruit_choice)
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
fruityvice_normalized = pd.json_normalize(fruityvice_response.json())

st.header("Fruityvice Fruit Advice!")
st.dataframe(fruityvice_normalized)

st.stop()

my_cnx = snowflake.connector.connect(**st.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("select * from fruit_load_list")
my_data_row = my_cur.fetchall()
st.text("The Fruit Load List contains:")
st.dataframe(my_data_row)

fruit_to_add = st.text_input("What Fruit Would You Like to Add?")
st.write('Thanks for Adding', fruit_to_add)

my_cur.execute("insert into fruit_load_list values ('from streamlit')")


