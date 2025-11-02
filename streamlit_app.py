# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col, when_matched

# Write directly to the app
st.title(f":cup_with_straw: Customize Your Smoothie:cup_with_straw: ")
st.write(
  """Choose the fruits you want in your custom smoothie! """
)

name_on_order = st.text_input('Name on Smoothie:')
st.write('The name on yout Smoothie wil be:'), name_on_order 

cnx=st.connection("Snowflake")
session= cnx.session()

session = get_active_session()
my_dataframe=session.table("Smoothies.public.fruit_options").select(col("FRUIT_NAME"))
#st.dataframe(data=my_dataframe, use_container_width=True )

ingredients_list = st.multiselect (
"Choose up to 6 ingredientes:",
    my_dataframe,
    max_selections = 6
    
)

if ingredients_list:

    ingredients_string = ''

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '

    # st.write(ingredients_string)

    my_insert_stmt =  f"""
    INSERT INTO smoothies.public.orders(ingredients, name_on_order)
    VALUES ('{ingredients_string}', '{name_on_order}')
"""
   
    
    # st.write(my_insert_stmt)
    time_to_insert=st.button('Submit Order')
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")
        
    st.write(my_insert_stmt)
    st.stop()

    og_dataset = session.table("smoothies.public.orders")
    edited_dataset = session.create_dataframe(editable_df)
    og_dataset.merge(edited_dataset
                     , (og_dataset['ORDER_UID'] == edited_dataset['ORDER_UID'])
                     , [when_matched().update({'ORDER_FILLED': edited_dataset['ORDER_FILLED']})]
                    )
