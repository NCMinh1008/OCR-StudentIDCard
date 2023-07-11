import gradio as gr
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

iface = gr.Interface(
    fn=fetch_data,
    inputs=None,
    outputs="table"
)

# # Define a database query function
# def query_database(name):
#     cursor = conn.cursor()
#     cursor.execute("SELECT * FROM extracted_data WHERE name = %s", (name,))
#     result = cursor.fetchone()
#     cursor.close()
#     return result

# # Define the Gradio app
# iface = gr.Interface(
#     fn=query_database,
#     inputs="text",
#     outputs="text",
#     title="Database Query",
#     description="Enter a name to query the database.",
#     examples=[["John"], ["Jane"]],
# )

# Run the Gradio app
iface.launch()