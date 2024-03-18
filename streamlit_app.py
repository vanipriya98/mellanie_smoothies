import streamlit as st
from snowflake.snowpark.functions import col

st.title("Customize your smoothie 🥤")
st.write("Choose the fruits you want in your custom smoothie!")

name_on_order = st.text_input('Name on Smoothie')
st.write('The name on the smoothie will be:', name_on_order)
cnx=st.connection("snowflake")
session = cnx.session() 
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))

ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:',
    my_dataframe ,
    max_selections =5
)

if ingredients_list:
    ingredients_string = ', '.join(ingredients_list)
    st.write('You have chosen the following ingredients:', ingredients_string)

    my_insert_stmt = f"INSERT INTO smoothies.public.orders (ingredients, name_on_order) VALUES ('{ingredients_string}', '{name_on_order}')"
    time_to_inst = st.button('Submit Order')

    if time_to_inst:
        try:
            session.sql(my_insert_stmt)
            st.success('Your smoothie order has been successfully submitted! 🎉')
        except Exception as e:
            st.error(f"An error occurred while submitting your order: {e}")
