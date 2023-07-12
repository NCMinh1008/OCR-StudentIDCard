import gradio as gr
import pandas as pd
import mysql.connector

# Connect to the database
conn = mysql.connector.connect(
    host="localhost",
    port="3306",
    user="root",
    password="N@mtr4n123",
    database="ocr"
)
cursor = conn.cursor()

def fetch_data():
    cursor.execute("SELECT * FROM extracted_data")
    data = cursor.fetchall()
    return data

gr.Interface(
    fetch_data,
    inputs=None,
    outputs=gr.outputs.Dataframe(type='array', headers=['No.', 'Name', 'Date of Birth', 'Major', 'Student ID']),
    title="EXTRACTED INFORMATION",
    description='<div style="text-align: center;"><h3>Press Generate button to display all the extracted information</h3></div>'
    ).launch(debug=True)