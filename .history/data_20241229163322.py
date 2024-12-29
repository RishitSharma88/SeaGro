import sqlite3
import pandas as pd

# Load CSV into a DataFrame
csv_file_path = "unique_course_records.csv"  # Replace with the path to your CSV file
df = pd.read_csv(csv_file_path)

# Connect to SQLite database (or create it if it doesn't exist)
db_file_path = r"C:\Users\Mudit\Desktop\GitHub\SeaGro\instance\SeaGro.db"
  # Replace with the desired SQLite DB file name
connection = sqlite3.connect(db_file_path)
cursor = connection.cursor()

# Insert data into the table
df.to_sql("Course", connection, if_exists="append", index=False)

# Commit and close the connection
connection.commit()
connection.close()

print(f"Data from {csv_file_path} has been loaded into {db_file_path}.")

