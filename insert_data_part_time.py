import csv
import psycopg2
from psycopg2 import sql

# PostgreSQL database connection parameters
db_params = {
    'dbname': 'studybucks',
    'user': 'vaidehipatel',
    'password': 'root',
    'host': 'localhost',
    'port': '5432'
}

# CSV file path
csv_file_path = 'cleaned_new_dataset.csv'

# Table and column names
part_time_table_name = 'Part Time'
part_time_columns = ['user_id', 'wage_per_hour', 'total']

# Constants
hours_per_week = 15
weeks_per_month = 4

# Connect to the PostgreSQL database
conn = psycopg2.connect(**db_params)
cursor = conn.cursor()

# Open the CSV file and insert values into the table
with open(csv_file_path, 'r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        # Fetch user_id from the User table
        user_query = sql.SQL("SELECT user_id FROM {} WHERE email = {}").format(
            sql.Identifier('User'),
            sql.Placeholder()
        )
        cursor.execute(user_query, (row['email'],))
        user_result = cursor.fetchone()

        if user_result:
            user_id = user_result[0]

            # Calculate total wage for the user
            wage_per_hour = float(row['wage_per_hour'])
            total_wage = wage_per_hour * hours_per_week * weeks_per_month

            # Prepare the SQL query for Part Time table
            insert_query = sql.SQL("INSERT INTO {} ({}, {}, {}) VALUES ({}, {}, {})").format(
                sql.Identifier(part_time_table_name),
                sql.Identifier('user_id'),
                sql.Identifier('wage_per_hour'),
                sql.Identifier('total'),
                sql.Placeholder(),
                sql.Placeholder(),
                sql.Placeholder()
            )

            # Execute the query
            cursor.execute(insert_query, (user_id, wage_per_hour, total_wage))

# Commit the changes and close the connection
conn.commit()
conn.close()
