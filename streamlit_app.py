import streamlit
import pandas

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
streamlit.multiselect("Pick some fruits: ", list(my_fruit_list.index))

# display the list
