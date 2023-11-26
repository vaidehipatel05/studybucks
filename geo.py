import pandas as pd
import folium
from folium.plugins import HeatMap
from sqlalchemy import create_engine

# Replace these with your actual database parameters
db_params = {
    'database': 'studybucks',
    'user': 'vaidehipatel',
    'password': 'root',
    'host': 'localhost',
    'port': '5432'
}

# Create a SQLAlchemy engine
engine = create_engine(f'postgresql+psycopg2://{db_params["user"]}:{db_params["password"]}@{db_params["host"]}/{db_params["database"]}')

# Fetch student data including city, state, lat, and lng
query = """
    SELECT g.lat, g.lng
    FROM "User" u
    JOIN geo g ON u.city = g.city;
"""

# Load data into a DataFrame
student_geo_df = pd.read_sql_query(query, engine)

# Close the SQLAlchemy engine
engine.dispose()

# Create a base map centered at an average location
map_center = [student_geo_df['lat'].mean(), student_geo_df['lng'].mean()]
mymap = folium.Map(location=map_center, zoom_start=4)

# Create a heatmap layer using the coordinates of each student
heat_data = student_geo_df[['lat', 'lng']].values
HeatMap(heat_data, name='Heatmap', max_zoom=13).add_to(mymap)

# Add a layer control to switch between the heatmap and the base map
folium.LayerControl().add_to(mymap)

# Save the map as an HTML file or display it
mymap.save("student_concentration_heatmap.html")

