import mysql.connector
import pandas as pd 
import json
import os

conn = mysql.connector.connect(
    host='127.0.0.1',
    port='3306',
    user='root',
    password='N@mtr4n123',
    database='ocr'
)

cursor = conn.cursor()

# Directory containing the JSON files
json_files_dir = '/kaggle/working/OCR-StudentIDcard/craft/Results/Output'

# Iterate over the JSON files
for filename in os.listdir(json_files_dir):
    if filename.endswith('.json'):
        json_file_path = os.path.join(json_files_dir, filename)
        
        # Read the JSON file
        with open(json_file_path, 'r') as file:
            json_data = json.load(file)
            
        # Extract the data from JSON
        data_points = json_data['data']
        headers = json_data['headers']
        
        student_name = data_points[0][0]
        date_of_birth = data_points[1][0]
        major = data_points[2][0]
        student_id = data_points[3][0]
                    
        # Insert the data into the database table
        insert_query = '''
        INSERT INTO extracted_data (student_name, date_of_birth, major, student_id)
        VALUES (%s, %s, %s, %s)
        '''
        insert_values = (student_name, date_of_birth, major, student_id)
        cursor.execute(insert_query, insert_values)
        conn.commit()

# Close the cursor and connection
cursor.close()
conn.close()
