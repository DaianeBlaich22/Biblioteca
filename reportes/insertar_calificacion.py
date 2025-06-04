import psycopg2
import random

# Conexión a la base de datos
conn = psycopg2.connect(
    host="localhost",
    database="biblioteca",
    user="postgres",
    password="123"
)
cur = conn.cursor()

# Obtener libros y usuarios existentes
cur.execute("SELECT id FROM libros_libro;")
libros = [row[0] for row in cur.fetchall()]

cur.execute("SELECT id FROM auth_user;")
usuarios = [row[0] for row in cur.fetchall()]

if len(usuarios) < 10:
    raise Exception("Debe haber al menos 1 usuario en la base de datos.")

# Parámetros para cantidad de calificaciones aleatorias
min_calificaciones = 0
max_calificaciones = 15

for libro_id in libros:
    cantidad_calificaciones = random.randint(min_calificaciones, max_calificaciones)
    for _ in range(cantidad_calificaciones):
        user_id = random.choice(usuarios)
        puntaje = round(random.uniform(0.5, 5.0), 2)
        cur.execute("""
            INSERT INTO libros_calificacion (libro_id, user_id, puntaje)
            VALUES (%s, %s, %s)
            ON CONFLICT DO NOTHING;
        """, (libro_id, user_id, puntaje))

conn.commit()
cur.close()
conn.close()

print("✅ Se insertaron calificaciones aleatorias para cada libro con cantidad variable y usuarios repetidos.")