import pandas as pd
import psycopg2

# Replace these with your actual database parameters
db_params = {
    'dbname': 'studybucks',
    'user': 'vaidehipatel',
    'password': 'root',
    'host': 'localhost',
    'port': '5432'
}

# Connect to the PostgreSQL database
conn = psycopg2.connect(**db_params)
cursor = conn.cursor()

# Load data from worldcities_filtered.csv
world_cities_df = pd.read_csv('worldcities_filtered.csv')

# Insert data into the geo table
for index, row in world_cities_df.iterrows():
    insert_query = """
    INSERT INTO geo (city, state, lat, lng)
    VALUES (%s, %s, %s, %s);
    """
    cursor.execute(insert_query, (row['city'], row['state'], row['lat'], row['lng']))

conn.commit()

# Close the database connection
cursor.close()
conn.close()
