# Biblioteca Digital - Daiane Blaich

## Tecnologías y dependencias utilizadas

```text
Package                       Version
----------------------------- -----------
asgiref                       3.9.1
contourpy                     1.3.2
cycler                        0.12.1
Django                        5.2.4
djangorestframework           3.16.0
djangorestframework_simplejwt 5.5.0
fonttools                     4.58.5
kiwisolver                    1.4.8
matplotlib                    3.10.3
numpy                         2.3.1
packaging                     25.0
pandas                        2.3.1
pillow                        11.3.0
pip                           24.3.1
psycopg2-binary               2.9.10
PyJWT                         2.9.0
pyparsing                     3.2.3
python-dateutil               2.9.0.post0
pytz                          2025.2
six                           1.17.0
sqlparse                      0.5.3
tzdata                        2025.2
```

---

## Instrucciones de instalación y configuración

### Requisitos previos

Asegúrate de tener **Python 3.8 o superior** instalado.\
Verifica tu versión ejecutando:

```bash
python --version
```

### Crear entorno virtual

Se recomienda crear un entorno virtual.\
Por ejemplo, para crear uno llamado `venv`:

```bash
python -m venv venv
```

Para activar el entorno virtual:

- **En Windows:**
  ```bash
  venv\Scripts\activate
  ```
- **En Linux/Mac:**
  ```bash
  source venv/bin/activate
  ```

### Instalación de requerimientos

Con el entorno virtual activo, instala Django y el driver de PostgreSQL:

```bash
pip install django psycopg2-binary
```

### Crear el proyecto Django

Con el siguente comando creamos el projecto de django:
```bash
django-admin startproject biblioteca
cd biblioteca
```

### Crear la aplicación principal

Vamos a crear la aplicacion  `libros`:

```bash
python manage.py startapp libros
```

### Configuración de PostgreSQL en Django

Edita `biblioteca/settings.py` y modifica la sección `DATABASES`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'biblioteca',
        'USER': 'postgres',
        'PASSWORD': 'contraseñaSegura', 
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### Aplicar Migraciones

Ejecuta las migraciones para crear las tablas en la base de datos:

```bash
python manage.py makemigrations
python manage.py migrate
```

---

## Descripción general del sistema

El sistema **Biblioteca Digital** permite gestionar información de libros, autores, géneros y usuarios, además de analizar calificaciones, generar reportes visuales y recomendar lecturas.\
Está basado en **Django**, utiliza PostgreSQL como motor de base de datos y soporta autenticación JWT.

### Estructura de modelos

- **Autor:** Guarda el nombre y nacionalidad del escritor/a.
- **Género:** Categoriza los libros en distintos géneros literarios.
- **Libro:** Incluye detalles como título, autor, género, fecha de publicación, ISBN y un enlace externo.
- **Calificación:** Relaciona a los usuarios con los libros mediante una puntuación.

### Usuarios y seguridad

El sistema aprovecha el módulo de usuarios de Django, permitiendo registro y login.\
La autenticación para la API se maneja mediante **JWT tokens** para mayor seguridad.

### Panel administrativo y análisis de datos

El panel de Django permite administrar todos los registros fácilmente.\
Además, se incluyen **comandos personalizados** que producen gráficos estadísticos y sugerencias de libros de acuerdo a las preferencias y tendencias de la base de datos.

### Comandos especiales disponibles

- **Generar reportes:**\
  Comando para crear gráficos en la carpeta `/reportes` sobre géneros, autores, libros mejor calificados, tendencias por año, etc.
- **Recomendar libros:**\
  Comando para sugerir libros destacados de un género específico usando la consola.

---

## Ejemplo de uso y pruebas

### **Registro de usuario**


**Endpoint:**

```
POST http://127.0.0.1:8000/api/register/
```

**Ejemplo de payload:**

```json
{
  "username": "daiane",
  "email": "daiane@gmail.com",
  "password": "Abc1234!#"
}
```

**Respuesta esperada (Postman):**

![registrarse](https://github.com/user-attachments/assets/02107df3-cf2f-4b4a-a548-be5b485509c2)


---

### **Inicio de sesión**


**Endpoint:**

```
POST http://127.0.0.1:8000/api/login/
```

**Ejemplo de datos:**

```json
{
  "username": "daiane",
  "password": "Abc1234!#"
}
```

**Respuesta esperada (Postman):**

![login](https://github.com/user-attachments/assets/0b79848c-0dfe-4c37-8ce1-f9e84db31924)


El token generado se usa para autenticarse en los demás endpoints protegidos.

---

## **Gestión de libros vía API**
A continuación se muestra cómo interactuar con la API de libros utilizando métodos HTTP estándar.
Recuerda: Para las operaciones de actualización y eliminación, es obligatorio pasar el ID del libro en la URL.

**Listar todos los libros**

**Endpoint:**
```http
GET http://127.0.0.1:8000/api/libros/
```
**Respuesta esperada (Postman):**

Se listan todos los libros registrados en la base de datos.

![todos_los_libros](https://github.com/user-attachments/assets/19e388ef-2e38-41ef-8f5e-55234f89e54a)

**Consultar un libro por ID**

**Endpoint:**
```http
GET http://127.0.0.1:8000/api/libros/1/
```
Donde 1 es el ID del libro que quieres consultar.

**Respuesta esperada (Postman):**

Se muestra el detalle del libro con ID 1.

![pro_id](https://github.com/user-attachments/assets/593268e2-9d4b-4775-a672-37a73d3a3c32)


**Agregar un nuevo libro**

**Endpoint:**

```http
POST http://127.0.0.1:8000/api/libros/
```
Ejemplo de datos a enviar:

```json
{
    "titulo": "Unterm Rad",
    "autor_id": 3,
    "genero_id": 1,
    "fechalanzamiento": "1906-01-01",
    "isbn": "9783150000281",
    "enlace": "https://de.wikipedia.org/wiki/Unterm_Rad"
}
```

**Respuesta esperada (Postman):**

Se retorna el objeto del libro recién creado, incluyendo su ID asignado por la base de datos.

![insertar](https://github.com/user-attachments/assets/e03cea6f-0fce-4d5f-a97b-f04290293f6c)


**Actualizar un libro existente**

Para actualizar un libro, debes pasar el ID del libro en la URL.

**Ejemplo:**
Supón que deseas actualizar el libro con ID 47.

**Endpoint:**
```http
PUT http://127.0.0.1:8000/api/libros/47/
```
**Ejemplo de datos a enviar:**

```json
{
    "titulo": "Demian",
    "autor_id": 3,
    "genero_id": 1,
    "fechalanzamiento": "1919-01-01",
    "isbn": "9783150000298",
    "enlace": "https://de.wikipedia.org/wiki/Demian"
}
```

**Nota:**
Asegúrate de poner el ID correcto en la URL.

**Respuesta esperada (Postman):**

Se retorna el libro actualizado con los nuevos datos.

![actualizar](https://github.com/user-attachments/assets/e4c918cd-7226-43cd-bb1b-b9a00d83964e)


**Eliminar un libro**
Para eliminar un libro, debes pasar el ID del libro en la URL.

**Ejemplo:**
Si quieres eliminar el libro con ID 47:

**Endpoint:**
```http
DELETE http://127.0.0.1:8000/api/libros/47/
```

**Respuesta esperada (Postman):**

Se confirma la eliminación exitosa del libro (puede mostrar un mensaje o un status 204 sin contenido).

![eliminar](https://github.com/user-attachments/assets/2db8ed16-26c5-4c33-912f-f8ec8d69f278)


**Resumen**

Para consultar, actualizar o eliminar un libro, el ID del libro debe ir en la URL.

Para agregar, simplemente realiza el POST al endpoint sin necesidad de especificar un ID.
---
## Uso de ModelViewSet para las vistas de la API
Para las operaciones sobre libros, se utiliza la clase ModelViewSet de Django REST Framework, que permite implementar de manera sencilla todas las operaciones CRUD (crear, leer, actualizar y eliminar) para el modelo.
Esto elimina la necesidad de escribir manualmente cada vista para cada operación, haciendo el desarrollo mucho más ágil y limpio.

**Ejemplo:**

```python
from rest_framework import viewsets
from .models import Libro
from .serializers import LibroSerializer
from rest_framework.permissions import IsAuthenticated

class LibroViewSet(viewsets.ModelViewSet):
    queryset = Libro.objects.all()
    serializer_class = LibroSerializer
    permission_classes = [IsAuthenticated]

```
**Ventajas de este enfoque:**

- Crea automáticamente todos los endpoints REST necesarios (GET, POST, PUT, DELETE, etc.) para el modelo.
- Centraliza la lógica repetitiva, manteniendo el código simple y fácil de mantener.
- Permite agregar fácilmente permisos y validaciones para proteger la API (por ejemplo, sólo usuarios autenticados pueden acceder).
- Sigue las buenas prácticas recomendadas por Django REST Framework.


## Reportes gráficos automáticos del sistema
Al ejecutar el comando:

```bash
python manage.py reporteslibros
```

se generan automáticamente los siguientes gráficos estadísticos en la carpeta /reportes:

**1. Cantidad de libros por género**
Archivo: 1-libros_por_genero.png
Muestra cuántos libros hay en cada género literario dentro de la base de datos. Cada barra representa un género y el número arriba de cada barra indica la cantidad exacta.

![1-libros_por_genero](https://github.com/user-attachments/assets/11646e88-ba75-4bf3-8aee-fc3503f87f20)


**2. Top 10 autores con más libros**
Archivo: 2-libros_por_autor.png
Presenta los diez autores que tienen más libros registrados en el sistema, ordenados de mayor a menor. Ideal para identificar los autores más productivos en la biblioteca.

![2-libros_por_autor](https://github.com/user-attachments/assets/330c027c-74f6-4364-8cc5-dc11c737552e)


**3. Top 10 libros mejor calificados**
Archivo: 3-top10_libros_calificacion.png
Exhibe los diez libros con el promedio de calificación más alto, considerando únicamente aquellos que han recibido al menos una puntuación. Útil para recomendar lecturas destacadas.

![3-top10_libros_calificacion](https://github.com/user-attachments/assets/b7ae8d65-c888-4f51-9bed-5c85c7648016)


**4. Top 10 autores mejor calificados**
Archivo: 4-top10_autores_calificacion.png
Muestra los diez autores cuyos libros tienen, en promedio, las mejores calificaciones otorgadas por los usuarios. Es útil para descubrir los autores más valorados por la comunidad.

![4-top10_autores_calificacion](https://github.com/user-attachments/assets/06249682-26d5-4e47-9c5f-a6648717f88b)


**5. Libros publicados por década**
Archivo: 5-libros_por_decada.png
Agrupa los libros según la década en la que fueron lanzados, permitiendo visualizar tendencias de publicación y la evolución histórica del catálogo.

![5-libros_por_decada](https://github.com/user-attachments/assets/a7c801ad-d66f-42e0-8ed6-4ed8cee251c2)


**6. Usuarios más activos (top 10 por calificaciones)**
Archivo: 6-top10_usuarios_califican.png
Resalta los diez usuarios que han realizado más calificaciones, mostrando los miembros más participativos de la plataforma.

![6-top10_usuarios_califican](https://github.com/user-attachments/assets/d4108d12-c838-4a84-82b1-3a118613c46f)


**7. Distribución de calificaciones (histograma)**
Archivo: 7-histograma_calificaciones.png
Gráfico de histograma que muestra cómo se distribuyen todas las calificaciones otorgadas, permitiendo ver si la mayoría de libros reciben buenas, malas o variadas puntuaciones.

![7-histograma_calificaciones](https://github.com/user-attachments/assets/8c46e854-83e8-447b-b167-1a6db332e608)


**8. Libros con y sin calificaciones**
Archivo: 8-libros_con_sin_calificacion.png
Comparativo entre la cantidad de libros que tienen al menos una calificación y los que aún no han sido calificados por ningún usuario.

![8-libros_con_sin_calificacion](https://github.com/user-attachments/assets/9e5795c3-46b7-4e85-9f24-42d0b1104f45)


**9. Calificación promedio por género (horizontal)**
Archivo: 9-promedio_genero_h.png
Presenta el promedio de calificación global para cada género literario. El género mejor valorado se resalta en verde y el de menor promedio en rojo, facilitando la comparación.

![9-promedio_genero_h](https://github.com/user-attachments/assets/63993fdc-5e2d-4615-90c3-6131c416183b)


**10. Mejor libro por género (promedio calificación)**
Archivo: 10-mejor_libro_por_genero.png
Para cada género, muestra el libro que obtuvo el mayor promedio de calificación, permitiendo identificar las obras más destacadas de cada categoría.

![10-mejor_libro_por_genero](https://github.com/user-attachments/assets/052fb82f-354a-4a19-b036-d17ab60ad78a)


**11. Cantidad de libros por nacionalidad del autor**
Archivo: 11-libros_por_nacionalidad.png
Desglosa cuántos libros existen por cada nacionalidad de los autores registrados, visualizando la diversidad geográfica de la colección.

![11-libros_por_nacionalidad](https://github.com/user-attachments/assets/dc40bf13-44bc-4c1c-a34a-fd5f1459ed96)



## Comando de recomendación de géneros y libros
El proyecto incluye un comando especial para la recomendación de géneros y libros, que puede ejecutarse desde consola para obtener sugerencias personalizadas según la cantidad de calificaciones en la base de datos.

**¿Qué hace este comando?**
**Sin argumentos:**
Muestra un ranking de los géneros literarios más populares, ordenados por la cantidad total de puntuaciones recibidas por todos sus libros.
Por defecto, se muestran los 5 géneros más recomendados, pero puedes cambiar ese número con el argumento --top.

**Con argumento de género:**
Si se indica un ID de género mediante --genero, el comando recomienda los 10 libros más relevantes de ese género, ordenados por la cantidad de calificaciones y su promedio.
Se muestran el título, el número de puntuaciones, el promedio de calificación y el autor.

**Ejemplos de uso**
Para ver los géneros más recomendados:

```bash
python manage.py recomendar_generos
```
Para ver los 8 géneros más recomendados:

```bash
python manage.py recomendar_generos --top 8
```

Para ver recomendaciones de libros dentro de un género (por ID):

```bash
python manage.py recomendar_generos --genero 3
```

![recomendaciones](https://github.com/user-attachments/assets/69a15538-1761-49f7-8887-6d2d16ad0a0e)


**Explicación técnica**
Este comando utiliza consultas avanzadas del ORM de Django para:

- Contar cuántas puntuaciones ha recibido cada género sumando las de todos sus libros.
- Ordenar los libros dentro de un género por popularidad y promedio de calificación.
- Presentar los resultados de manera ordenada y legible en la consola.

Así, permite a los administradores o usuarios internos identificar tendencias y recomendar lecturas a partir de la participación real de la comunidad.


## Licencia
Este proyecto está licenciado bajo los términos de la Licencia MIT.

Esto significa que puedes utilizar, copiar, modificar y distribuir el código con libertad, siempre que incluyas una copia del aviso de licencia original en cualquier distribución significativa del software.

**Resumen:**
Puedes usar el sistema para fines personales, educativos o comerciales.
No hay garantías explícitas. El uso es bajo tu propio riesgo.

Para ver los detalles completos, consulta el archivo LICENSE incluido en este repositorio.

**Licencia de terceros:**
```text
 Name                           Version      License
 Django                         5.2.4        BSD License
 PyJWT                          2.9.0        MIT License
 asgiref                        3.9.1        BSD License
 contourpy                      1.3.2        BSD License
 cycler                         0.12.1       BSD License
 djangorestframework            3.16.0       BSD License
 djangorestframework_simplejwt  5.5.0        MIT License
 fonttools                      4.58.5       MIT
 kiwisolver                     1.4.8        BSD License
 matplotlib                     3.10.3       Python Software Foundation License
 numpy                          2.3.1        BSD License
 packaging                      25.0         Apache Software License; BSD License
 pandas                         2.3.1        BSD License
 pillow                         11.3.0       UNKNOWN
 psycopg2-binary                2.9.10       GNU Library or Lesser General Public License (LGPL)
 pyparsing                      3.2.3        MIT License
 python-dateutil                2.9.0.post0  Apache Software License; BSD License
 pytz                           2025.2       MIT License
 six                            1.17.0       MIT License
 sqlparse                       0.5.3        BSD License
 tzdata                         2025.2       Apache Software License
```
