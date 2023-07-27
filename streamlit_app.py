import streamlit
import requests
import pandas
import snowflake.connector
from urllib.error import URLError

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
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado', 'Banana'])
fruits_to_show = my_fruit_list.loc[fruits_selected]
streamlit.dataframe(fruits_to_show)

# Create API call function
def get_fruityvice_data(fruit_choice):
    # Requests
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
    fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
    return fruityvice_normalized

streamlit.header("Fruityvice Fruit Advice!")

try:
    # Text entry box 1
    fruit_choice = streamlit.text_input('What fruit would you like information about?')

    if not fruit_choice:
        streamlit.error("Pleaase select a fruit to get information")

    else:
        back_from_function = get_fruityvice_data(fruit_choice)
        # Display the table on the page.
        streamlit.dataframe(back_from_function)

except URLError as e:
    streamlit.error()

# Snowflake add fruit function
def insert_row_snowflake(new_fruit):
    with my_cnx.cursor() as my_cur:
         my_cur.execute("use role accountadmin")
         my_cur.execute("insert into fruit_load_list values(%s)", new_fruit)
         return 'Thanks for adding ' + new_fruit

# Text entry box 2
new_fruit_to_add = streamlit.text_input('What fruit would you like to add ?')

# Create button to add fruit
if streamlit.button('Add a fruit to the list'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    streamlit.text(insert_row_snowflake(new_fruit_to_add))

streamlit.header("The fruit load list contains :")

# Snowflake call function
def get_fruit_load_list():
    with my_cnx.cursor() as my_cur:
         my_cur.execute("use role accountadmin")
         my_cur.execute("select * from fruit_load_list")
         return my_cur.fetchall()

# Create button to load fruits
if streamlit.button('Get Fruit Load List'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    my_data_rows = get_fruit_load_list()
    streamlit.dataframe(my_data_rows)