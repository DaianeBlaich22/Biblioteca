import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import psycopg2

# Configura el estilo de los gráficos
sns.set(style="whitegrid")

# Conexión a PostgreSQL
conn = psycopg2.connect(
    dbname="biblioteca",
    user="postgres",
    password="123",
    host="localhost",
    port="5432"
)

# -------- Reporte 1: Puntaje promedio por libro --------
def promedio_por_libro():
    df = pd.read_sql("""
        SELECT l.nombre AS libro, AVG(c.puntaje) AS promedio
        FROM libros_calificacion c
        JOIN libros_libro l ON c.libro_id = l.id
        GROUP BY l.nombre
        ORDER BY promedio DESC;
    """, conn)
    df.plot(kind='bar', x='libro', y='promedio', legend=False, color='skyblue')
    plt.title("Puntaje promedio por libro")
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()


# -------- Reporte 2: Libros por autor --------
def libros_por_autor():
    df = pd.read_sql("""
        SELECT a.nombre AS autor, COUNT(l.id) AS cantidad
        FROM libros_autor a
        JOIN libros_libro l ON l.autor_id = a.id
        GROUP BY a.nombre
        ORDER BY cantidad DESC;
    """, conn)
    sns.barplot(data=df, x="cantidad", y="autor", palette="viridis")
    plt.title("Cantidad de libros por autor")
    plt.show()


# -------- Reporte 3: Distribución de puntajes --------
def distribucion_puntajes():
    df = pd.read_sql("SELECT puntaje FROM libros_calificacion;", conn)
    sns.histplot(df['puntaje'], bins=10, kde=True, color='salmon')
    plt.title("Distribución de calificaciones")
    plt.xlabel("Puntaje")
    plt.show()


# -------- Reporte 4: Libros por género --------
def libros_por_genero():
    df = pd.read_sql("""
        SELECT g.nombre AS genero, COUNT(l.id) AS cantidad
        FROM libros_genero g
        JOIN libros_libro l ON l.genero_id = g.id
        GROUP BY g.nombre
        ORDER BY cantidad DESC;
    """, conn)
    df.plot(kind='pie', y='cantidad', labels=df['genero'], autopct='%1.1f%%')
    plt.title("Distribución de libros por género")
    plt.ylabel("")
    plt.show()


# -------- Reporte 5: Calificaciones por usuario --------
def calificaciones_por_usuario():
    df = pd.read_sql("""
        SELECT u.username, COUNT(c.id) AS calificaciones
        FROM auth_user u
        JOIN libros_calificacion c ON c.user_id = u.id
        GROUP BY u.username
        ORDER BY calificaciones DESC;
    """, conn)
    sns.barplot(data=df, x="calificaciones", y="username", palette="coolwarm")
    plt.title("Número de calificaciones por usuario")
    plt.show()


# -------- Reporte 6: Publicaciones por año --------
def publicaciones_por_anio():
    df = pd.read_sql("""
        SELECT DATE_PART('year', fecha_lanzamiento) AS anio, COUNT(*) AS cantidad
        FROM libros_libro
        GROUP BY anio
        ORDER BY anio;
    """, conn)
    sns.lineplot(data=df, x="anio", y="cantidad", marker="o")
    plt.title("Libros publicados por año")
    plt.xlabel("Año")
    plt.ylabel("Cantidad de libros")
    plt.show()


# -------- Reporte 7: Top 5 libros mejor calificados --------
def top_libros_mejor_calificados():
    df = pd.read_sql("""
        SELECT l.nombre, ROUND(AVG(c.puntaje), 2) AS promedio
        FROM libros_calificacion c
        JOIN libros_libro l ON c.libro_id = l.id
        GROUP BY l.nombre
        ORDER BY promedio DESC
        LIMIT 5;
    """, conn)
    sns.barplot(data=df, x="promedio", y="nombre", palette="mako")
    plt.title("Top 5 libros mejor calificados")
    plt.show()


# -------- Reporte 8: Autores con mejor promedio --------
def autores_con_mejor_promedio():
    df = pd.read_sql("""
        SELECT a.nombre AS autor, ROUND(AVG(c.puntaje), 2) AS promedio
        FROM libros_calificacion c
        JOIN libros_libro l ON c.libro_id = l.id
        JOIN libros_autor a ON l.autor_id = a.id
        GROUP BY a.nombre
        ORDER BY promedio DESC
        LIMIT 10;
    """, conn)
    sns.barplot(data=df, x="promedio", y="autor", palette="rocket")
    plt.title("Autores con mejor promedio de calificaciones")
    plt.show()


# -------- Reporte 9: Cantidad de calificaciones por libro --------
def calificaciones_por_libro():
    df = pd.read_sql("""
        SELECT l.nombre AS libro, COUNT(c.id) AS total
        FROM libros_libro l
        LEFT JOIN libros_calificacion c ON l.id = c.libro_id
        GROUP BY l.nombre
        ORDER BY total DESC;
    """, conn)
    df.plot(kind='bar', x='libro', y='total', color='orchid')
    plt.title("Número de calificaciones por libro")
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()


# -------- Reporte 10: Promedio por género --------
def promedio_por_genero():
    df = pd.read_sql("""
        SELECT g.nombre AS genero, ROUND(AVG(c.puntaje), 2) AS promedio
        FROM libros_calificacion c
        JOIN libros_libro l ON c.libro_id = l.id
        JOIN libros_genero g ON l.genero_id = g.id
        GROUP BY g.nombre
        ORDER BY promedio DESC;
    """, conn)
    sns.barplot(data=df, x="promedio", y="genero", palette="cubehelix")
    plt.title("Promedio de calificación por género")
    plt.show()


# ---------- Ejecutar todos los reportes ----------
if __name__ == "__main__":
    promedio_por_libro()
    libros_por_autor()
    distribucion_puntajes()
    libros_por_genero()
    calificaciones_por_usuario()
    publicaciones_por_anio()
    top_libros_mejor_calificados()
    autores_con_mejor_promedio()
    calificaciones_por_libro()
    promedio_por_genero()

    # Cierra la conexión
    conn.close()
