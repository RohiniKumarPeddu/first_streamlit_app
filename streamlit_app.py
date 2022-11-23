import streamlit
import pandas
import requests
import snowflake.connector

streamlit.title("My first streamlit App")

streamlit.header("Required:")
streamlit.text("❄️Snowflake Account")
streamlit.text("📧GMail Account")
streamlit.text("GitHub Account")
streamlit.text("Streamlit Account")

streamlit.header("My Fruits List")

# read fruit list from S3 bucket
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index("Fruit")

# display fruit list
streamlit.dataframe(my_fruit_list)

# create a pick list for user to pick one or more fruits
fruits_selected = streamlit.multiselect("Pick some fruits: ", list(my_fruit_list.index), ["Avocado", "Strawberries"])
fruits_to_show = my_fruit_list.loc[fruits_selected]

# display the selected list
streamlit.dataframe(fruits_to_show)

# header for fruityvice API response
streamlit.header("Fruityvice Fruit Advice!")

# add a text entry box and send the input to fruityvice as part of the API call
fruit_choice = streamlit.text_input("What fruit would you like information about?", "kiwi")
streamlit.write("The user entered", fruit_choice)

# display fruitvice api resonse
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
#streamlit.text(fruityvice_response.json())

# normalize the json data
fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
# display normalized data
streamlit.dataframe(fruityvice_normalized)

