import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError
streamlit.title('My Mom New Healthy Diner')

streamlit.header( 'Breakfast fav')
streamlit.text( ' omega 3 and blueberry oatmeal')
streamlit.text('kale, spinach and smoothie')
streamlit.text('hard-boiled free-range egg')

streamlit.header( 'BUILD YOUR OWN SMOOTHIE')

#import pandas
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')


# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected=streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show=my_fruit_list.loc[fruits_selected]

#Display the table on the page.
streamlit.dataframe(fruits_to_show)

def get_fruityvice_data(this_fruit_choice):
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+this_fruit_choice)
    fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
    return fruityvice_normalized
      
   
streamlit.header("Fruityvice Fruit Advice!")
try:
   fruit_choice = streamlit.text_input('What fruit would you like information about?')
   if not fruit_choice:
    streamlit.error("please slect a fruit to get information.")
   else:
    back_from_function=get_fruityvice_data(this_fruit_choice)
    streamlit.dataframe(back_from_function)
#streamlit.write('The user entered ', fruit_choice)
except URLError as e:
  streamlit.error()



streamlit.header("VIEW OUR FRUIT LIST-ADD YOUR FAVOURITES!")
#snowflake-related functions
def get_fruit_load_list():
    with my_cnx.cursor() as my_cur:
         my_cur.execute("SELECT * from fruit_load_list")
         return my_cur.fetchall()
    
    #add a button to load a fruit
if streamlit.button('Get fruit list'):
     my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
     my_data_rows = get_fruit_load_list()
     my_cnx.close()
     streamlit.dataframe(my_data_rows)
#allow the end user to add fruit to the list
def insert_row_snowflake(new_fruit):
    with my_cnx.cursor() as my_cur:
         my_cur.execute("insert into fruit_load_list values(' "+add_my_fruit+" ')")
         return "Thanks for adding"+ new_fruit

add_my_fruit = streamlit.text_input('What  would you like to add?')
if streamlit.button('add a fruit to the list'):
     my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
     back_from_function=insert_row_snowflake(add_my_fruit)
     streamlit.text(back_from_function)                                
     streamlit.write('The user entered ', add_my_fruit)

#streamlit.write('Thanks for adding','jackfruit')
#streamlit.write('The user entered ', jackfruit)
streamlit.stop() 
