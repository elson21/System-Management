import psycopg2

connection = psycopg2.connect(
    host='localhost',
    port=5432,
    user='postgres',
    password='postgres'
)

print("Hey, I am you Porstgres DB!")

cursor = connection.cursor()
cursor.execute("SELECT version();")
result = cursor.fetchone()
print(f"ProsgreSQL version: {result[0]}")

cursor.close()
connection.close()