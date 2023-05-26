import pandas as pd
import streamlit as st
import plotly.express as px
import json
import mysql.connector
from PIL import Image
import webbrowser
from streamlit_option_menu import option_menu
import requests

#Set Page Configuration
def page_configuration():
    st.set_page_config(page_title='PhonePe Pulse Data',page_icon = ":bar_chart:", layout='wide')
    #Load and display image
    image = Image.open("C:/Users/GIRI RAGHAV/Phonepe Pulse Project/logo.jpg")
    st.title("&emsp;:blue[PhonePe Pulse Data Visualization and Exploration]  :bar_chart:")
    st.image(image)

def home():
    st.subheader(":blue[INTRODUCTION]")
    st.write("""
    Welcome to PhonePe Pulse, a powerful data analytics tool designed to help businesses track and analyze their transaction data in real-time. 
    With PhonePe Pulse, you can gain valuable insights into transaction count, transaction amount, transaction type and more. 
    This tool provides a user-friendly interface that empowers businesses to make data-driven decisions and optimize their operations.""")

    st.subheader(":blue[KEY FEATURES]")
    st.write("""
    - Transaction Count Analysis: Gain a comprehensive understanding of the number of transactions processed over a specific time period, enabling you to identify trends and patterns.
    - Transaction Amount Analysis: Analyze the total transaction amount generated during a particular period, helping you measure revenue and identify growth opportunities.
    - Data Visualization: Visualize your transaction data through interactive charts, graphs, and maps, enabling you to easily interpret and communicate insights.
    - Filters and Options: Customize your data exploration by applying filters, selecting specific timeframes, and drilling down into specific regions or categories.
    - Data Export: Download your analyzed plots as PNG images for further analysis or integration with other tools.""")

    st.subheader(":blue[GITHUB REPOSITORY]")
    st.write("""Explore the GitHub repository for PhonePe Pulse, where you can access the source code, contribute to the project, and stay updated with the latest enhancements and releases.""")
    if st.button('Open'):
        webbrowser.open_new_tab("https://github.com/PhonePe/pulse#readme")
    
#Visualization and Exploration
def visualization_and_exploration():
    
    with st.container():
        SELECT = option_menu("MENU", ["HOME","TOP TRENDS","VISUALIZE DATA"],
                            icons=["house","graph-up-arrow","bar-chart-line"],
                            menu_icon= "menu-button-wide",
                            default_index=0,
                            orientation="horizontal",
                            )
        #HOME
        if SELECT == "HOME":
            st.subheader(":blue[HOME]")
            home()

        #Establish the MySQL connection
        conn = mysql.connector.connect(
                                        host='localhost',
                                        user='your_username',
                                        password='your_password',
                                        database='phonepe_pulse_database',
                                        auth_plugin='mysql_native_password'
                                    )
        #TOP TRENDS                                                             
        if SELECT == "TOP TRENDS":
            st.subheader(":blue[TOP TRENDS]")
            Type = st.selectbox("**:blue[SELECT THE TYPE OF DATA]**", ("Transaction Data", "User Data"))
            column1, column2 = st.columns([1, 1], gap="large")
            
            with column1:
                Year = st.selectbox('**:blue[SELECT THE YEAR]**',(2018,2019,2020,2021,2022))
                
            with column2:
                Quarter = st.selectbox('**:blue[SELECT THE QUARTER]**',(1,2,3,4))
               
            #Transaction Data
            if Type == "Transaction Data":
                Data = st.selectbox("**:blue[DATA]**", ("Top 10 States in per capita transactions", "Top 10 Districts in per capita transactions" , "Top 10 Pincodes in per capita transactions"))

                #Top 10 States
                if Data == "Top 10 States in per capita transactions":

                    cursor = conn.cursor()
                    cursor.execute(f"SELECT State, SUM(Transaction_amount/Transaction_count) AS Per_Capita_transaction FROM agg_trans_data WHERE Year = {Year} AND Quarter = {Quarter} GROUP BY State ORDER BY Per_Capita_transaction DESC LIMIT 10")

                    df = pd.DataFrame(cursor.fetchall(), columns=['State', 'Per_Capita_transaction'])

                    fig = px.pie(df, values='Per_Capita_transaction', 
                                 names='State', title=st.write("### :blue[TOP 10 STATES IN PER CAPITA TRANSACTIONS]"),
                                color_discrete_sequence=px.colors.sequential.haline, hover_data=['Per_Capita_transaction'],
                                labels={'Per_Capita_transaction': 'Per_Capita_transaction'})

                    fig.update_traces(textposition='inside', textinfo='percent+label')
                    st.plotly_chart(fig, use_container_width=True)
                    
                #Top 10 Districts
                elif Data == "Top 10 Districts in per capita transactions":
                    
                    cursor = conn.cursor()
                    cursor.execute(
                        f"select District, SUM(Transaction_amount/Transaction_count) AS Per_Capita_transaction FROM map_trans_data WHERE Year = {Year} AND Quarter = {Quarter} GROUP BY District ORDER BY Per_Capita_transaction DESC LIMIT 10")

                    df = pd.DataFrame(cursor.fetchall(), columns=['District', 'Per_Capita_transaction'])

                    fig = px.pie(df, values='Per_Capita_transaction',
                                names='District',
                                title=st.write("### :blue[TOP 10 DISTRICTS IN PER CAPITA TRANSACTIONS]"),
                                color_discrete_sequence=px.colors.sequential.matter,
                                hover_data=['Per_Capita_transaction'],
                                labels={'Per_Capita_transaction': 'Per_Capita_transaction'})

                    fig.update_traces(textposition='inside', textinfo='percent+label')
                    st.plotly_chart(fig, use_container_width=True)
                    
                #Top 10 Pincodes
                elif Data == "Top 10 Pincodes in per capita transactions":
                    
                    cursor = conn.cursor()                    
                    cursor.execute(
                        f"SELECT District, SUM(Transaction_amount/Transaction_count) AS Per_Capita_transaction FROM top_trans_data WHERE Year = {Year} and Quarter = {Quarter} GROUP BY District ORDER BY Per_Capita_transaction DESC LIMIT 10")

                    df = pd.DataFrame(cursor.fetchall(), columns=['Pincode', 'Per_Capita_transaction'])
                    fig = px.pie(df, values='Per_Capita_transaction',
                                names='Pincode',
                                title=st.write("### :blue[TOP 10 PINCODES IN PER CAPITA TRANSACTIONS]"),
                                color_discrete_sequence=px.colors.sequential.speed,
                                hover_data=['Per_Capita_transaction'],
                                labels={'Per_Capita_transaction': 'Per_Capita_transaction'})

                    fig.update_traces(textposition='inside', textinfo='percent+label')
                    st.plotly_chart(fig, use_container_width=True)

            #User Data
            elif Type == "User Data":
                Data = st.selectbox("**:blue[DATA]**", ("Top 10 Brands used" , "Top 10 Districts in Number of Users", "Top 10 States in Number of Registered Users"))
                
                #Top 10 Brands
                if Data == "Top 10 Brands used":

                    if Year == 2022 and Quarter in [2, 3, 4]:
                        st.write("#### Data for Quarters 2, 3 and 4 of the year 2022 are not available.")
                        
                    else:
                        cursor = conn.cursor()
                        cursor.execute(
                            f"SELECT Brands, SUM(User_count) AS Total_users, AVG(User_percentage)*100 AS Avg_Percentage FROM agg_user where Year = {Year} and Quarter = {Quarter} GROUP BY Brands ORDER BY Total_users DESC LIMIT 10")

                        df = pd.DataFrame(cursor.fetchall(), columns=['Brands', 'Total_Users', 'Avg_Percentage'])
                        fig = px.bar(df,
                                    title=st.write("### :blue[TOP 10 BRANDS]"),
                                    x="Total_Users",
                                    y="Brands",
                                    orientation='h',
                                    color='Avg_Percentage',
                                    color_continuous_scale=px.colors.sequential.Sunsetdark)
                        st.plotly_chart(fig, use_container_width=True)

                #Top 10 Districts   
                elif Data == "Top 10 Districts in Number of Users":
                        
                        cursor = conn.cursor()                     
                        cursor.execute(
                            f"SELECT District, SUM(Number_of_users) AS Total_Users FROM map_user_data WHERE Year = {Year} AND Quarter = {Quarter} GROUP BY District ORDER BY Total_Users DESC LIMIT 10")
                        
                        df = pd.DataFrame(cursor.fetchall(), columns=['District', 'Total_Users'])
                        df.Total_Users = df.Total_Users.astype(float)
                        
                        fig = px.bar(df,
                                    title=st.write("### :blue[TOP 10 DISTRICTS IN NUMBER OF USERS]"),
                                    x="Total_Users",
                                    y="District",
                                    orientation='h',
                                    color='Total_Users',
                                    color_continuous_scale=px.colors.sequential.Emrld)
                        st.plotly_chart(fig, use_container_width=True)
                
                #Top 10 States
                elif Data == "Top 10 States in Number of Registered Users":
                        
                        cursor = conn.cursor()                     
                        cursor.execute(
                            f"SELECT State, SUM(Registered_users) AS Registered_users FROM top_user_data WHERE Year = {Year} AND Quarter = {Quarter} GROUP BY State ORDER BY Registered_users DESC LIMIT 10")
                        
                        df = pd.DataFrame(cursor.fetchall(), columns=['State', 'Registered_users'])
             
                        fig = px.bar(df,
                                    title=st.write("### :blue[TOP 10 STATES IN NUMBER OF REGISTERED USERS]"),
                                    x="Registered_users",
                                    y="State",
                                    orientation='h',
                                    color='Registered_users',
                                    color_continuous_scale=px.colors.sequential.Purpor)
                        st.plotly_chart(fig, use_container_width=True)

        #VISUALIZE DATA
        elif SELECT == "VISUALIZE DATA":
            st.subheader(":blue[VISUALIZATION AND EXPLORATION]")

            Year = st.selectbox('**:blue[SELECT THE YEAR]**',(2018,2019,2020,2021,2022))
            Quarter = st.selectbox('**:blue[SELECT THE QUARTER]**',(1,2,3,4))
            Type = st.selectbox("**:blue[SELECT THE TYPE OF DATA]**", ("Transaction Data", "User Data"))

            #Transaction Data
            if Type == "Transaction Data":
                    Data = st.selectbox("**:blue[DATA]**", ("Overall Transaction Amount", "Overall Transaction Count"))

                    #Overall Transaction Amount
                    if Data == "Overall Transaction Amount":
                        st.write("## :blue[Overall State Data | Transaction Amount]")
                        
                        cursor = conn.cursor()
                        cursor.execute(
                            f"SELECT State, SUM(Transaction_count) AS Total_Transactions, SUM(Transaction_amount) AS Total_amount FROM map_trans_data WHERE Year = {Year} AND Quarter = {Quarter} GROUP BY State ORDER BY State")
                        
                        df1 = pd.DataFrame(cursor.fetchall(), columns=['State', 'Total_Transactions', 'Total_amount'])
                        df2 = pd.read_csv('C:/Users/GIRI RAGHAV/Phonepe Pulse Project/State_list.csv')
                    
                        #Get the geojson data from the provided link
                        response = requests.get("https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson")
                        geojson_data = response.json()

                        #Extract the state names from the geojson data
                        geojson_states = [feature['properties']['ST_NM'] for feature in geojson_data['features']]

                        #df2 state list
                        df2_states = ['andaman-&-nicobar-islands', 'andhra-pradesh', 'arunachal-pradesh', 'assam', 'bihar', 'chandigarh', 
                                      'chhattisgarh', 'dadra-&-nagar-haveli-&-daman-&-diu', 'delhi', 'goa', 'gujarat', 'haryana', 'himachal-pradesh', 
                                      'jammu-&-kashmir', 'jharkhand', 'karnataka', 'kerala', 'ladakh', 'lakshadweep', 'madhya-pradesh', 'maharashtra',
                                      'manipur', 'meghalaya', 'mizoram', 'nagaland', 'odisha', 'puducherry', 'punjab', 'rajasthan', 'sikkim', 
                                      'tamil-nadu', 'telangana', 'tripura', 'uttar-pradesh', 'uttarakhand', 'west-bengal']

                        #Create a mapping dictionary
                        state_mapping = dict(zip(df2_states, geojson_states))

                        #Replace state names in df2 using the mapping dictionary
                        df1['State'] = df2['State'].replace(state_mapping)

                        fig = px.choropleth(df1,
                                            geojson=geojson_data,
                                            featureidkey='properties.ST_NM',
                                            locations='State',
                                            color='Total_amount',
                                            color_continuous_scale='Sunsetdark')

                        fig.update_geos(fitbounds="locations", visible=False)
                        fig.update_layout(width=600,height=600)
                        st.plotly_chart(fig, use_container_width=True)
 
                    #Overall Transaction Count
                    elif Data == "Overall Transaction Count":
                        st.write("## :blue[Overall State Data | Transaction Count]")
                        
                        cursor = conn.cursor()
                        cursor.execute(
                            f"SELECT State, SUM(Transaction_count) AS Total_Transactions, SUM(Transaction_amount) AS Total_amount FROM map_trans_data WHERE Year = {Year} AND Quarter = {Quarter} GROUP BY State ORDER BY State")
                        df1 = pd.DataFrame(cursor.fetchall(), columns=['State', 'Total_Transactions', 'Total_amount'])
                        df2 = pd.read_csv('C:/Users/GIRI RAGHAV/Phonepe Pulse Project/State_list.csv')

                        #Get the geojson data from the provided link
                        response = requests.get("https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson")
                        geojson_data = response.json()

                        #Extract the state names from the geojson data
                        geojson_states = [feature['properties']['ST_NM'] for feature in geojson_data['features']]

                        #df2 state list
                        df2_states = ['andaman-&-nicobar-islands', 'andhra-pradesh', 'arunachal-pradesh', 'assam', 'bihar', 'chandigarh', 
                                      'chhattisgarh', 'dadra-&-nagar-haveli-&-daman-&-diu', 'delhi', 'goa', 'gujarat', 'haryana', 'himachal-pradesh', 
                                      'jammu-&-kashmir', 'jharkhand', 'karnataka', 'kerala', 'ladakh', 'lakshadweep', 'madhya-pradesh', 'maharashtra',
                                      'manipur', 'meghalaya', 'mizoram', 'nagaland', 'odisha', 'puducherry', 'punjab', 'rajasthan', 'sikkim', 
                                      'tamil-nadu', 'telangana', 'tripura', 'uttar-pradesh', 'uttarakhand', 'west-bengal'] 

                        #Create a mapping dictionary
                        state_mapping = dict(zip(df2_states, geojson_states))

                        #Replace state names in df2 using the mapping dictionary
                        df1['State'] = df2['State'].replace(state_mapping)

                        fig = px.choropleth(df1,
                                            geojson=geojson_data,
                                            featureidkey='properties.ST_NM',
                                            locations='State',
                                            color='Total_Transactions',
                                            color_continuous_scale='Bluered')

                        fig.update_geos(fitbounds="locations", visible=False)
                        fig.update_layout(width=600,height=600)
                        st.plotly_chart(fig, use_container_width=True)
            
            #User Data
            elif Type == "User Data":
                    Data = st.selectbox("**:blue[DATA]**", ("State Wise Users", "District Wise Users"))

                    #State wise Users
                    if Data == "State Wise Users":
                        st.write("## :blue[Overall State Data | Number Of Users]")

                        cursor = conn.cursor()
                        cursor.execute(
                            f"SELECT State, SUM(Number_of_users) AS Total_Users FROM map_user_data WHERE Year = {Year} AND Quarter = {Quarter} GROUP BY State ORDER BY State")
                        df1 = pd.DataFrame(cursor.fetchall(), columns=['State', 'Total_Users'])
                        df1.Total_Users = df1.Total_Users.astype(int)
                        df2 = pd.read_csv('C:/Users/GIRI RAGHAV/Phonepe Pulse Project/State_list.csv')
            
                        #Get the geojson data from the provided link
                        response = requests.get("https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson")
                        geojson_data = response.json()

                        #Extract the state names from the geojson data
                        geojson_states = [feature['properties']['ST_NM'] for feature in geojson_data['features']]

                        #df2 state list
                        df2_states = ['andaman-&-nicobar-islands', 'andhra-pradesh', 'arunachal-pradesh', 'assam', 'bihar', 'chandigarh', 
                                      'chhattisgarh', 'dadra-&-nagar-haveli-&-daman-&-diu', 'delhi', 'goa', 'gujarat', 'haryana', 'himachal-pradesh', 
                                      'jammu-&-kashmir', 'jharkhand', 'karnataka', 'kerala', 'ladakh', 'lakshadweep', 'madhya-pradesh', 'maharashtra',
                                      'manipur', 'meghalaya', 'mizoram', 'nagaland', 'odisha', 'puducherry', 'punjab', 'rajasthan', 'sikkim', 
                                      'tamil-nadu', 'telangana', 'tripura', 'uttar-pradesh', 'uttarakhand', 'west-bengal']
                        
                        #Create a mapping dictionary
                        state_mapping = dict(zip(df2_states, geojson_states))
                    
                        #Replace state names in df2 using the mapping dictionary
                        df1['State'] = df2['State'].replace(state_mapping)

                        fig = px.choropleth(df1,
                                                geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                                                featureidkey='properties.ST_NM',
                                                locations='State',
                                                color='Total_Users',
                                                color_continuous_scale='YlGnBu')

                        fig.update_geos(fitbounds="locations", visible=False)
                        fig.update_layout(width=600,height=600)
                        st.plotly_chart(fig, use_container_width=True)

                    #District-wise Users - Bar Chart
                    elif Data == "District Wise Users":
                        st.write("## :blue[Choose any State to Explore more about it.]")

                        selected_state = st.selectbox("",
                                                        ('andaman-&-nicobar-islands', 'andhra-pradesh', 'arunachal-pradesh', 'assam',
                                                        'bihar',
                                                        'chandigarh', 'chhattisgarh', 'dadra-&-nagar-haveli-&-daman-&-diu', 'delhi',
                                                        'goa', 'gujarat', 'haryana',
                                                        'himachal-pradesh', 'jammu-&-kashmir', 'jharkhand', 'karnataka', 'kerala',
                                                        'ladakh', 'lakshadweep',
                                                        'madhya-pradesh', 'maharashtra', 'manipur', 'meghalaya', 'mizoram',
                                                        'nagaland', 'odisha', 'puducherry', 'punjab', 'rajasthan', 'sikkim',
                                                        'tamil-nadu', 'telangana', 'tripura', 'uttar-pradesh', 'uttarakhand',
                                                        'west-bengal'), index=30)
                                                            
                        cursor = conn.cursor()
                        cursor.execute(
                            f"SELECT State,Year,Quarter,District,SUM(Number_of_users) AS Total_Users FROM map_user_data WHERE Year = {Year} AND Quarter = {Quarter} AND State = '{selected_state}' GROUP BY State, District,Year,Quarter ORDER BY State,District")

                        df = pd.DataFrame(cursor.fetchall(),columns=['State', 'Year', 'Quarter', 'District', 'Total_Users'])
                        df.Total_Users = df.Total_Users.astype(int)

                        fig = px.bar(df,
                                        title = selected_state,
                                        x="District",
                                        y="Total_Users",
                                        orientation='v',
                                        color='Total_Users',
                                        color_continuous_scale=px.colors.sequential.Plasma)
                        
                        fig.update_layout(xaxis_tickangle=-50)       
                        st.plotly_chart(fig, use_container_width=True)        
                    
        conn.close()

if __name__ == '__main__':
     page_configuration()
     visualization_and_exploration()