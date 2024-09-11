# Import python packages
import requests
import streamlit as st
from snowflake.snowpark.functions import col


# Write directly to the app
st.title(":cup_with_straw: Customize your Smoothie :cup_with_straw:")
st.write(
    """
    Choose the fruits you want in your custome smoothie!.
    """
)


name_on_order = st.text_input("Name on smoothie")
st.write("The name on smoothiew will be :", name_on_order)


cnx = st.connection("snowflake")
session = cnx.session()
#session = get_active_session()

my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'),col('SEARCH_ON'))
st.dataframe(data=my_dataframe, use_container_width=True)



ingredients_string = ('')
ingredients_list=st.multiselect("choose 5 items ",my_dataframe , max_selections=5)

if ingredients_list:
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '
        st.subheader(fruit_chosen + 'Nutritional infrormation ')
        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
        st.write('The search value for ', fruit_chosen,' is ', search_on, '.')
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_chosen )
        fv_df = st.dataframe(data=fruityvice_response.json() , use_container_width=True )




    
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
                values ('""" + ingredients_string + """' 
                        ,
                        '""" + name_on_order + """')           
                """
    session.sql(my_insert_stmt).collect()
    st.success('Your Smoothie is ordered , '+ name_on_order +' !' ,icon="✅")
    
