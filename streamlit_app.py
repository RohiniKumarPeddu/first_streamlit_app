import streamlit as st
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

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

# get fruit of choice data from fruityvice
def get_fruityvice_data(this_fruit_choice):
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + this_fruit_choice)
    #st.text(fruityvice_response.json())

    # normalize the json data
    fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
    # display normalized data
    
    return fruityvice_normalized
    
# header for fruityvice API response
st.header("Fruityvice Fruit Advice!")

try:
    # add a text entry box and send the input to fruityvice as part of the API call
    fruit_choice = st.text_input("What fruit would you like information about?")

    if not fruit_choice:
        st.error("Please select a fruit to get the information.")
    else:
        st.write("The user entered", fruit_choice)
        # get fruit choice data
        fruityvice_data = get_fruityvice_data(fruit_choice)
        # display fruit choice data
        st.dataframe(fruityvice_data)
        
except URLError as e:
    st.error()
        
# snowflake section

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
#rows = run_query("select * from fruit_load_list;")

st.header("Hello from Snowflake:")
st.header("The Fruit Load List:")

# add button to get the fruit list
if st.button("Get Fruits List"):
    rows = run_query("select * from fruit_load_list;")
    st.dataframe(rows)

# Perform query.
# Uses st.experimental_memo to only rerun when the query changes or after 10 min.
@st.experimental_memo(ttl=600)
def run_insert(query):
    with conn.cursor() as cur:
        cur.execute(query)
        return "Thank you for adding"

# add a text entry box and send the input to fruityvice as part of the API call
fruit_to_add = st.text_input("Which fruit would you like add?")

st.text("insert into fruit_load_list values ('" + fruit_to_add + "');")
#st.stop()

if st.button("Add Fruit"):
    add_fruit = run_insert("insert into fruit_load_list values ('" + fruit_to_add + "');")
    st.write(add_fruit, fruit_to_add)
