import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError
streamlit.title('My Parents New Healthy Diner')
streamlit.header('Breakfast Menu')
streamlit.text('Idli, Dosa, Upma, Vada')
streamlit.text('🥑🍞Idli,Masala Dosa,Semya Upma,Vada')
streamlit.header('Breakfast Menu')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text(' 🐔 Hard-Boiled Free-Range Egg')
streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇') 

my_fruit_list = pandas.read_csv("https://urldefense.com/v3/__https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt)

my_fruit_list = my_fruit_list.set_index('Fruit')
#streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado','Strawberries'])
#streamlit.dataframe(my_fruit_list)
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado','Strawberries'])
fruits_show = my_fruit_list.loc[fruits_selected]
streamlit.dataframe(fruits_show)

#New Section to display fruityvice api response
#Create the repeatable code block (called function)
def get_fruityvice_data(this_fruit_choice):
     fruityvice_response = requests.get("https://urldefense.com/v3/__https://fruityvice.com/api/fruit/" + fruityvice_input )
     fruityvice_normalize = pandas.json_normalize(fruityvice_response.json())
     return fruityvice_normalize
     #streamlit.dataframe(fruityvice_normalize)
     
streamlit.header('Fruityvice Fruit Advice')
try: 
     fruityvice_input = streamlit.text_input('What fruit would you like information about?' , 'kiwi')
     if not fruityvice_input:
        streamlit.error("Please select a fruit to get information. ")
     else:  
          back_from_function = get_fruityvice_data(fruityvice_input)
          streamlit.dataframe(back_from_function)
except URLError as e:
    streamlit.error()
    
#streamlit.stop()

streamlit.header("The fruit load list contains:")
#snowflake related functions
def get_fruit_load_list():
    with my_cnx.cursor() as my_cur:
         my_cur.execute("select * from fruit_load_list")
         return my_cur.fetchall()

# Add a button to load the fruit
if streamlit.button('Get Fruit Load List'):
   my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
   my_data_rows = get_fruit_load_list()
   my_cnx.close()  
   streamlit.dataframe(my_data_rows)

# aLLOW THEE END USER to add a fruit to the list
def insert_row_snowflake(new_fruit):
     with my_cnx.cursor() as my_cur:
         my_cur.execute("insert into fruit_load_list values ('"+ new_fruit + "')")
         return "Thanks for adding " + new_fruit

    
add_my_fruit = streamlit.text_input('What fruit would you like to add?')
if streamlit.button('Add a Fruit to the List'): 
   my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])     
   back_from_function = insert_row_snowflake(add_my_fruit) 
   my_cnx.close()    
   streamlit.text(back_from_function)                     
#streamlit.write('Thanks for adding ', add_my_fruit)
#my_cur.execute("insert into fruit_load_list values('from streamlit')")
