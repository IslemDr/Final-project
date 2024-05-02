import pandas as pd 
import plotly.express as px
import streamlit as st
from urllib.request import urlopen
import json
import seaborn as sns
import matplotlib.pyplot as plt
#from mainapp import show_menu



st.set_page_config(page_title="Customer Habit Dashbord",
                   page_icon=":bar_chart:",
                   layout="wide",
                   initial_sidebar_state="collapsed")

logo_path = r"Final_Project\images\IMAGE2.png"

# Display the logo on the left side
st.image(logo_path, width=200)

def show_dashboard():

    df = pd.read_excel(
        io=r"C:\Users\islem\OneDrive\Desktop\final project\E-commerceCustomerBehavior.xlsx",
        engine='openpyxl',
        usecols='A:K',
        nrows=1000,
    )

    with st.expander("View Data"):
        st.write(df)

    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button('Download Data', data=csv, file_name="Data.csv", mime="text/csv")

    #---sidebar---
    st.sidebar.header('please filter here:')
    City = st.sidebar.multiselect(
        'Select the City',
        options=df['City'].unique(),
        default=df['City'].unique()
    )

    Gender = st.sidebar.multiselect(
        'Select the Gender',
        options=df['Gender'].unique(),
        default=df['Gender'].unique()
    )

    Age = st.sidebar.multiselect(
        'Select the Age',
        options=df['Age'].unique(),
        default=df['Age'].unique()
    )

    df_selection = df.query(
        "City == @City & Age == @Age & Gender == @Gender"
    )

    #st.dataframe(df_selection)

    st.title(":bar_chart: Customer Habit Dashboard")
    st.markdown("##")

    total_purchased = int(df_selection["Items Purchased"].sum())
    average_rating = round(df_selection["Average Rating"].mean(), 1)
    star_rating = ":star:" * int(round(average_rating, 0))
    average_spending_amount = round(df_selection["Total Spend"].mean(), 2)

    left_column, middle_column, right_column = st.columns(3)
    with left_column:
        st.subheader("total_purchased:")
        st.subheader(f"$ {total_purchased:,}")
    with middle_column:
        st.subheader("Average Rating")
        st.subheader(f"{average_rating} {star_rating}")
    with right_column:
        st.subheader("Average Spending Amount")
        st.subheader(f"$ {average_spending_amount}")

    st.markdown('---')

    # Rest of the code remains unchanged



    satisfaction_distribution = df_selection['Satisfaction Level'].value_counts().reset_index()
    satisfaction_distribution.columns = ['Satisfaction Level', 'Count']
    bar_chart_satisfaction = px.bar(satisfaction_distribution, x='Count', y='Satisfaction Level', 
                                    title='Distribution of Satisfaction Levels', 
                                    labels={'Satisfaction Level': 'Satisfaction Level', 'Count': 'Frequency'}, orientation="h")


    customer_counts = df_selection.groupby('City').size().reset_index(name='Customer Count')

    # Merge customer counts back to the original DataFrame
    df_selection = pd.merge(df_selection, customer_counts, on='City')

    city_counts = df_selection.groupby('City').size().reset_index(name='Customer Count')

    # Use a geocoding service to get the latitude and longitude coordinates for each city
    # Note: You may need to adjust this part depending on the geocoding service you use
    # Here, we'll use some sample coordinates
    city_locations = {  'City': ['Los Angeles', 'New York', 'Houston', 'Chicago', 'Miami', 'San Francisco'],
        'lat': [34.0522, 40.7128, 29.7604, 41.8781, 25.7617, 37.7749],
        'lon': [-118.2437, -74.0060, -95.3698, -87.6298, -80.1918, -122.4194]
    }
    city_locations_df = pd.DataFrame(city_locations)

    # Merge city counts with city locations
    city_data = pd.merge(city_locations_df, city_counts, on='City', how='inner')

    # Create a Plotly Mapbox figure
    mapbox = px.scatter_mapbox(city_data, 
                            lat="lat", lon="lon", 
                            hover_name="City", 
                            size="Customer Count", 
                            zoom=5, height=600,
                            color_continuous_scale=px.colors.cyclical.IceFire,
                            color='Customer Count',
                            labels={'Customer Count':'Number of Customers'}
                            )
    mapbox.update_layout(mapbox_style="carto-positron")
    mapbox.update_layout(margin={"r":0, "t":0, "l":0, "b":0})

    # Display the map

    left_column, right_column = st.columns(2)
    right_column.plotly_chart(bar_chart_satisfaction, use_container_width=True)
    left_column.plotly_chart(mapbox, use_container_width=True)

    #---hide streamlit style ---
    hide_st_style = """  
                <style>   
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                header {visibility: hidden;} 
                </style> 
                """

    st.markdown(hide_st_style, unsafe_allow_html=True)

        

    gender_spend = df_selection.groupby('Gender')['Total Spend'].mean().reset_index()

    # Plot average spending for each gender
    bar_chart_gender_spend = px.bar(gender_spend, x='Gender', y='Total Spend',
                                    title="Average Spending for each Gender",
                                    labels={'Gender': 'Gender', 'Total Spend': 'Total Spend'})

    # Calculate membership by gender
    gender_membership = df_selection.groupby(['Gender', 'Membership Type']).size().reset_index(name='Count')

    # Plot membership by gender
    bar_chart_gender_membership = px.bar(gender_membership, x='Gender', y='Count', color='Membership Type',
                                        title="Membership by Gender",
                                        labels={'Gender': 'Gender', 'Count': 'Membership Type', 'Membership Type': 'Membership Type'},
                                        barmode='group')

    pie_chart = px.pie(df_selection, title='Distribution of Customers based on gender', names='Gender', values='Customer ID')
    pie_chart.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=(dict(showgrid=False))
    )                  

    left_column, middle_column,right_column = st.columns(3)
    right_column.plotly_chart(bar_chart_gender_membership, use_container_width=True)
    middle_column.plotly_chart(bar_chart_gender_spend, use_container_width=True)
    left_column.plotly_chart(pie_chart,use_container_width=True)


    # average number of items purchased by age group

    bar_char_itemPurchased= px.bar(df_selection, x='Age', y='Items Purchased',
                                        title="Average NO. of Items Purchased by Age",
                                        labels={'Age': 'Age', 'Items Purchased': 'Items Purchased'},
                                        )
    bar_char_itemPurchased.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=(dict(showgrid=False))
    )
    pie_chart_discount = px.pie(df_selection, title="Frequency of Discounts Applied", names='Discount Applied')
    pie_chart_discount .update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=(dict(showgrid=False))
    )



    bar_chart_membership = px.bar(df_selection, x='Membership Type', y='Total Spend', 
                                        title="Membership & average spend",
                                        labels={'Membership Type': 'Membership Type', 'Total Spend': 'Total Spend'}
                                        )
    bar_chart_membership.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=(dict(showgrid=False)))




    left_column,middle_column, right_column = st.columns(3)
    right_column.plotly_chart(pie_chart_discount, use_container_width=True)
    middle_column.plotly_chart(bar_char_itemPurchased, use_container_width=True)
    left_column.plotly_chart(bar_chart_membership, use_container_width=True)




    #pie_chart = px.pie(melted_df, title='Custumers', values='Customer ID')

    st.image("Final_Project\images\survey.jpg", use_column_width=True)


if __name__ == "__main__":
     show_dashboard()



