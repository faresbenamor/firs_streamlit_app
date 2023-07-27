import streamlit
import requests
import pandas
import snowflake.connector

streamlit.title('My Parents New Healty Dinner')
streamlit.header('🥣 Breakfast Menu')
streamlit.text('🥗 Omega 3 & Blueberry Oatmeal')
streamlit.text('🐔 Kale, Spinach & Rocket Smoothie')
streamlit.text('🥑🍞 Hard-Boiled Free-Range Egg')
streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

# Pandas
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

# Requests
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + "kiwi")
fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())

# Text entry box 1
fruit_choice = streamlit.text_input('What fruit would you like information about?')
streamlit.write('The user entered ', fruit_choice)

# Display the table on the page.
streamlit.dataframe(fruits_to_show)
streamlit.header("Fruityvice Fruit Advice!")
streamlit.dataframe(fruityvice_normalized)

# Snowflake
my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("use role accountadmin")
my_cur.execute("insert into fruit_load_list values('test')")
my_data_rows = my_cur.fetchall()
streamlit.header("The fruit load list contains :")
streamlit.dataframe(my_data_rows)

# Text entry box2
fruit_choice = streamlit.text_input('What fruit would you like to do?')
streamlit.write('Thanks for adding ', fruit_choice)