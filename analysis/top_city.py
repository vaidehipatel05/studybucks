import pandas as pd
import matplotlib.pyplot as plt
import psycopg2

# Replace these with your actual database parameters
db_params = {
    'database': 'studybucks',
    'user': 'vaidehipatel',
    'password': 'root',
    'host': 'localhost',
    'port': '5432'
}

# Connect to the PostgreSQL database
conn = psycopg2.connect(**db_params)

# Assuming 'cleaned_new_dataset' is the table in your database
query = """
    SELECT city
    FROM "User";
"""

# Load data into a DataFrame
df = pd.read_sql_query(query, conn)

# Close the database connection
conn.close()

# Explore the distribution of students across all cities
city_distribution = df['city'].value_counts()

# Display all cities and the number of students in each city
print("City-wise Distribution:")
print(city_distribution)

# Create a bar chart for all cities
plt.figure(figsize=(15, 8))
city_distribution.plot(kind='bar', color='skyblue')
plt.title('Distribution of Students Across Cities')
plt.xlabel('City')
plt.ylabel('Number of Students')
plt.xticks(rotation=45, ha='right')  # Rotate city names for better visibility
plt.show()
