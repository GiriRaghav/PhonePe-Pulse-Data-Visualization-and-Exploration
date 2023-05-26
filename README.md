
# PhonePe Pulse Data Visualization and Exploration: A User-Friendly Tool Using Streamlit and Plotly

Introducing the PhonePe Pulse Dashboard: A powerful data visualization and analytics tool. This interactive dashboard brings the PhonePe Pulse Github repository to life, providing real-time insights and trends. With intuitive dropdown options, users can explore transaction count, transaction amount analysis, and customized data exploration. The dashboard, powered by a robust MySQL database, offers efficient data retrieval and seamless navigation. Export your analyzed data effortlessly and utilize pan, zoom, and reset options. Experience the transformative journey of data extraction, processing, and visualization with the PhonePe Pulse Dashboard, making informed decisions and elevating your data analysis.

## REQUIREMENTS

Libraries and Packages Used:

#### os: Operating system-related functionalities.

#### Pandas: Data manipulation and analysis.

#### streamlit: Framework for creating the interactive dashboard.

#### plotly.express: Creating visually appealing and interactive data visualizations.

#### json: Handling JSON data.

#### mysql.connector: Connecting to the MySQL database and executing SQL commands.

#### PIL (Python Imaging Library): Image processing tasks.

#### webbrowser: Opening the GitHub repository link.

#### streamlit_option_menu: Creating dropdown menus with icons in Streamlit.

#### requests: Making HTTP requests.

These libraries and packages play a crucial role in different aspects of the project, enabling operations such as data manipulation, visualization, database connectivity, image processing, web page opening, and HTTP communication.

## WORK FLOW

### Data Extraction: 
The PhonePe Pulse Github repository was cloned using scripting techniques to retrieve the required data. The data was then stored in a suitable format, such as CSV or JSON.

### Data Transformation: 
Python programming language, along with the Pandas library, was employed to manipulate and preprocess the extracted data. This involved performing tasks like data cleaning, handling missing values, and transforming the data into a format suitable for further analysis and visualization.

### Database Insertion: 
The "mysql-connector-python" library was utilized to establish a connection with a MySQL database. SQL commands were employed to insert the transformed data into the database for efficient storage and retrieval.

### Dashboard Creation: 
To develop an interactive and visually appealing dashboard, the Streamlit and Plotly libraries in Python were utilized. The Plotly library provided convenient functions for creating geo maps, enabling the display of data on a map. Streamlit facilitated the creation of a user-friendly interface, incorporating multiple dropdown options that allowed users to select and visualize different facts and figures.

### Data Retrieval: 
The "mysql-connector-python" library was employed once again to connect to the MySQL database. The data stored in the database was retrieved and loaded into a Pandas dataframe, which served as the basis for dynamically updating the dashboard.

### Deployment: 
Considerable emphasis was placed on ensuring the security, efficiency, and user-friendliness of the solution. Thorough testing was conducted to verify the functionality and accuracy of the dashboard. Once deemed ready, the dashboard was deployed publicly, enabling easy access for users.


By following this workflow, the project successfully accomplished the extraction, transformation, and visualization of data from the PhonePe Pulse Github repository.
