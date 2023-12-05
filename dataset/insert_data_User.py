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
table_name = 'User'
columns = ['name_stud', 'email', 'university', 'city', 'age', 'gender']

# Connect to the PostgreSQL database
conn = psycopg2.connect(**db_params)
cursor = conn.cursor()

# Open the CSV file and insert values into the table
with open(csv_file_path, 'r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        # Prepare the SQL query
        insert_query = sql.SQL("INSERT INTO {} ({}) VALUES ({})").format(
            sql.Identifier(table_name),
            sql.SQL(', ').join(map(sql.Identifier, columns)),
            sql.SQL(', ').join(sql.Placeholder() * len(columns))
        )

        # Execute the query
        cursor.execute(insert_query, [row[col] for col in columns])

# Commit the changes and close the connection
conn.commit()
conn.close()
