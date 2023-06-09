import streamlit
import pandas
import requests
import snowflake.connector

streamlit.title('🥣 My Parents New Healthy Diner')
streamlit.header(' 🥗 Breakfast Menu')
streamlit.text('🐔 Omega 3 & Blueberry Oatmeal')
streamlit.text(' 🥑 Kale, Spinach & Rocket Smoothie')
streamlit.text('🍞 Hard-Boiled Free-Range Egg')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')
fruits_selected=streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index))
fruits_to_show = my_fruit_list.loc[fruits_selected]

streamlit.dataframe(fruits_to_show)
# Let's put a pick list here so they can pick the fruit they want to include 
streamlit. header ('Fruityvice Fruit Advice!')
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
  if fruit_choice:
    streamlit.write('The user entered ', fruit_choice)
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+fruit_choice)
    fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
    streamlit.dataframe(fruityvice_normalized)
  else:
      streamlit.error("Please select fruit to get info")
except URLError as e:
  streamlit.error()

my_cnx = snowflake.connector.connect(**streamlit.secrets ["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("select * from pc_rivery_db.public.fruit_load_list")
my_data_rows = my_cur.fetchall() 
streamlit. header ("The fruit load list contains ")
streamlit.dataframe (my_data_rows)
fruit_choice_1=streamlit. text_input ("What fruit do you like to add ")
if(fruit_choice_1):
  with my_cnx.cursor() as my_cur:
    my_cur.execute ("insert into pc_rivery_db.public.fruit_load_list values ('"+fruit_choice_1 +"')")
    streamlit.write('Thanks for adding ', fruit_choice_1)


def insert_row_snowflake (new_fruit):
  with my_cnx.cursor() as my_cur:
    my_cur.execute ("insert into pc_rivery_db.public.fruit_load_list values ('"+new_fruit +"')")
    return "Thanks for adding "+new_fruit


