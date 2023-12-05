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
user_table_name = 'User'
emergency_fund_table_name = 'Emergency Fund'
user_columns = ['user_id', 'Name', 'email', 'University', 'City', 'Age', 'Gender']
emergency_fund_columns = ['user_id', 'ef_amount', 'ef_knowledge']

# Connect to the PostgreSQL database
conn = psycopg2.connect(**db_params)
cursor = conn.cursor()

# Open the CSV file and insert values into the table
with open(csv_file_path, 'r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        # Fetch user_id from the User table
        user_query = sql.SQL("SELECT user_id FROM {} WHERE email = {}").format(
            sql.Identifier(user_table_name),
            sql.Placeholder()
        )
        cursor.execute(user_query, (row['email'],))
        user_result = cursor.fetchone()

        if user_result:
            user_id = user_result[0]

            # Prepare the SQL query for Emergency Fund table
            insert_query = sql.SQL("INSERT INTO {} ({}, {}, {}) VALUES ({}, {}, {})").format(
                sql.Identifier(emergency_fund_table_name),
                sql.Identifier('user_id'),
                sql.Identifier('ef_amount'),
                sql.Identifier('ef_knowledge'),
                sql.Placeholder(),
                sql.Placeholder(),
                sql.Placeholder()
            )

            # Execute the query
            cursor.execute(insert_query, (user_id, None, row['ef_knowledge']))

# Commit the changes and close the connection
conn.commit()
conn.close()
