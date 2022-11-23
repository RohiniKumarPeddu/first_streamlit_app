import streamlit as st
import pandas
import requests
import snowflake.connector

st.title("My first streamlit App")

st.header("Required:")
st.text("❄️Snowflake Account")
st.text("📧GMail Account")
st.text("GitHub Account")
st.text("Streamlit Account")
st.text("Snowflake Connector")

st.header("My Fruits List")

# read fruit list from S3 bucket
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index("Fruit")

# display fruit list
st.dataframe(my_fruit_list)

# create a pick list for user to pick one or more fruits
fruits_selected = st.multiselect("Pick some fruits: ", list(my_fruit_list.index), ["Avocado", "Strawberries"])
fruits_to_show = my_fruit_list.loc[fruits_selected]

# display the selected list
st.dataframe(fruits_to_show)

# header for fruityvice API response
st.header("Fruityvice Fruit Advice!")

# add a text entry box and send the input to fruityvice as part of the API call
fruit_choice = st.text_input("What fruit would you like information about?", "kiwi")
st.write("The user entered", fruit_choice)

# display fruitvice api resonse
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
#st.text(fruityvice_response.json())

# normalize the json data
fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
# display normalized data
st.dataframe(fruityvice_normalized)

# Initialize connection.
# Uses st.experimental_singleton to only run once.
@st.experimental_singleton
def init_connection():
    return snowflake.connector.connect(
        **st.secrets["snowflake"], client_session_keep_alive=True
    )

conn = init_connection()

# Perform query.
# Uses st.experimental_memo to only rerun when the query changes or after 10 min.
@st.experimental_memo(ttl=600)
def run_query(query):
    with conn.cursor() as cur:
        cur.execute(query)
        return cur.fetchall()

#rows = run_query("select current_user(), current_account(), current_region();")
rows = run_query("select * from fruit_load_list;")

st.header("Hello from Snowflake:")
st.header("The Fruit Load List:")
st.dataframe(rows)
