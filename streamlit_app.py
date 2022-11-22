import streamlit
import pandas

streamlit.title("My first streamlit App")

streamlit.header("Required:")
streamlit.text("❄️Snowflake Account")
streamlit.text("📧GMail Account")
streamlit.text("GitHub Account")
streamlit.text("Streamlit Account")

streamlit.header("My Fruits List")

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
streamlit.dataframe(my_fruit_list)
