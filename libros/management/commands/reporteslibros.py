import os
from django.core.management.base import BaseCommand
from django.db.models import Count, Avg
from libros.models import Libro, Autor, Genero, Calificacion
from django.contrib.auth.models import User
import matplotlib.pyplot as plt
from collections import defaultdict
import numpy as np

class Command(BaseCommand):
    help = "Genera reportes gráficos de libros, autores y calificaciones"

    def handle(self, *args, **kwargs):
        # Crear carpeta si no existe
        os.makedirs('reportes', exist_ok=True)

        # 1. Libros por género
        qs1 = Genero.objects.annotate(num_libros=Count('libros')).order_by('-num_libros')
        plt.figure(figsize=(8,5))
        plt.bar([g.nombre for g in qs1], [g.num_libros for g in qs1])
        for i, v in enumerate([g.num_libros for g in qs1]):
            plt.text(i, v + 0.5, str(v), ha='center', va='bottom')
        plt.title('Cantidad de libros por género')
        plt.xlabel('Género')
        plt.ylabel('Cantidad de libros')
        plt.tight_layout()
        plt.savefig('reportes/1-libros_por_genero.png')


        # 2. Libros por autor (top 10)
        qs2 = Autor.objects.annotate(num_libros=Count('libros')).order_by('-num_libros')[:10]
        plt.figure()
        plt.bar([a.nombre for a in qs2], [a.num_libros for a in qs2])
        plt.title('Top 10 autores con más libros')
        plt.xlabel('Autor')
        plt.ylabel('Cantidad de libros')
        plt.xticks(rotation=30, ha='right')
        plt.tight_layout()
        plt.savefig('reportes/2-libros_por_autor.png')

        # 3. Calificaciones promedio por libro (top 10)
        qs3 = Libro.objects.annotate(prom=Avg('calificaciones__puntuacion')).order_by('-prom')[:10]
        plt.figure()
        plt.bar([l.titulo for l in qs3], [l.prom or 0 for l in qs3])
        plt.title('Top 10 libros mejor calificados')
        plt.xlabel('Libro')
        plt.ylabel('Promedio de calificación')
        plt.xticks(rotation=30, ha='right')
        plt.tight_layout()
        plt.savefig('reportes/3-top10_libros_calificacion.png')

        # 4. Calificaciones promedio por autor (top 10)
        qs4 = Autor.objects.annotate(prom=Avg('libros__calificaciones__puntuacion')).order_by('-prom')[:10]
        plt.figure()
        plt.bar([a.nombre for a in qs4], [a.prom or 0 for a in qs4])
        plt.title('Top 10 autores mejor calificados')
        plt.xlabel('Autor')
        plt.ylabel('Promedio de calificación')
        plt.xticks(rotation=30, ha='right')
        plt.tight_layout()
        plt.savefig('reportes/4-top10_autores_calificacion.png')

        # 5. Número de libros por año de lanzamiento
        qs5 = Libro.objects.values('fechalanzamiento').annotate(cant=Count('id')).order_by('fechalanzamiento')

        decadas = defaultdict(int)
        for row in qs5:
            year = int(str(row['fechalanzamiento'])[:4])
            decada = f"{year//10*10}s"
            decadas[decada] += row['cant']

        plt.figure(figsize=(12,6))
        bars = plt.bar(list(decadas.keys()), list(decadas.values()), color='skyblue')
        plt.title('Libros publicados por década', fontsize=16)
        plt.xlabel('Década', fontsize=12)
        plt.ylabel('Cantidad de libros', fontsize=12)
        plt.xticks(rotation=45, ha='right', fontsize=10)
        plt.yticks(fontsize=10)

        # Mostrar cantidad sobre cada barra
        for bar in bars:
            height = bar.get_height()
            plt.annotate('{}'.format(height),
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0,3),
                        textcoords="offset points",
                        ha='center', va='bottom')

        plt.tight_layout()
        plt.savefig('reportes/5-libros_por_decada.png')


        # 6. Usuarios con más calificaciones realizadas (top 10)
        qs6 = User.objects.annotate(num_cal=Count('calificaciones')).order_by('-num_cal')[:10]
        plt.figure()
        plt.bar([u.username for u in qs6], [u.num_cal for u in qs6])
        plt.title('Usuarios más activos (calificaciones)')
        plt.xlabel('Usuario')
        plt.ylabel('Cantidad de calificaciones')
        plt.xticks(rotation=30, ha='right')
        plt.tight_layout()
        plt.savefig('reportes/6-top10_usuarios_califican.png')

        # 7. Distribución de las calificaciones (histograma)
        qs7 = Calificacion.objects.values_list('puntuacion', flat=True)
        plt.figure()
        plt.hist(list(qs7), bins=10, edgecolor='black')
        plt.title('Distribución de calificaciones')
        plt.xlabel('Puntuación')
        plt.ylabel('Frecuencia')
        plt.tight_layout()
        plt.savefig('reportes/7-histograma_calificaciones.png')

        # 8. Libros sin calificaciones
        num_libros_sin_calif = Libro.objects.filter(calificaciones__isnull=True).count()
        num_libros_con_calif = Libro.objects.filter(calificaciones__isnull=False).distinct().count()
        plt.figure()
        plt.bar(['Con calificaciones', 'Sin calificaciones'], [num_libros_con_calif, num_libros_sin_calif])
        plt.title('Libros con/sin calificaciones')
        plt.ylabel('Cantidad')
        plt.tight_layout()
        plt.savefig('reportes/8-libros_con_sin_calificacion.png')

        # 9. Calificación promedio global por género
        qs9 = Genero.objects.annotate(prom=Avg('libros__calificaciones__puntuacion')).order_by('-prom')
        plt.figure()
        values = [g.prom or 0 for g in qs9]
        names = [g.nombre for g in qs9]
        colors = ['#1f77b4'] * len(values)
        
        if values:
            idx_max = np.argmax(values)
            idx_min = np.argmin(values)
            colors[idx_max] = '#2ca02c'
            colors[idx_min] = '#d62728'
        plt.figure(figsize=(8, 4))
        bars = plt.barh(names, values, color=colors)
        plt.xlim(2.5, 3.1)
        plt.xlabel('Promedio')
        plt.ylabel('Género')
        plt.title('Calificación promedio por género')

        for i, bar in enumerate(bars):
            width = bar.get_width()
            plt.annotate(f"{width:.2f}", (width, bar.get_y() + bar.get_height()/2),
                        ha='left', va='center')

        plt.tight_layout()
        plt.savefig('reportes/9-promedio_genero_h.png')



        # 10. Libros mejor calificados por género (top 1 por género)
        plt.figure(figsize=(9,5))
        nombres_generos = []
        mejores_libros = []
        for genero in Genero.objects.all():
            libro = (
                Libro.objects.filter(genero=genero)
                .annotate(prom=Avg('calificaciones__puntuacion'))
                .order_by('-prom')
                .first()
            )
            if libro and libro.prom is not None:
                nombres_generos.append(genero.nombre)
                mejores_libros.append(libro.prom)

        bars = plt.bar(nombres_generos, mejores_libros, color='skyblue')
        plt.title('Mejor libro por género (promedio calificación)')
        plt.xlabel('Género')
        plt.ylabel('Promedio calificación')
        plt.xticks(rotation=35, ha='right')
        for i, v in enumerate(mejores_libros):
            plt.text(i, float(v) + 0.05, f"{float(v):.2f}", ha='center', va='bottom')

        plt.tight_layout()
        plt.savefig('reportes/10-mejor_libro_por_genero.png')


        # 11. Cantidad de libros por nacionalidad de autor
        qs11 = Autor.objects.values('nacionalidad').annotate(cant=Count('libros')).order_by('-cant')
        plt.figure()
        plt.bar([x['nacionalidad'] for x in qs11], [x['cant'] for x in qs11])
        plt.title('Cantidad de libros por nacionalidad de autor')
        plt.xlabel('Nacionalidad')
        plt.ylabel('Cantidad de libros')
        plt.tight_layout()
        plt.savefig('reportes/11-libros_por_nacionalidad.png')

        self.stdout.write(self.style.SUCCESS('¡Reportes generados en la carpeta "reportes"!'))
