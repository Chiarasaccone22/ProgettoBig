import psycopg2


conn = psycopg2.connect(
    host="localhost",
    port="5432",
    user="postgres",
    password="password",
    database="postgres"
)

cursor = conn.cursor()
cursor.execute("SELECT * FROM conti")
results = cursor.fetchall()

for row in results:
    print(row)

cursor.close()
conn.close()
