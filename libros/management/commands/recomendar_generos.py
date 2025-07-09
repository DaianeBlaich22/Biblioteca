from django.core.management.base import BaseCommand
from django.db.models import Count, Avg
from libros.models import Genero, Libro

class Command(BaseCommand):
    help = "Recomienda géneros por cantidad de puntuaciones, o libros de un género si se indica su id"

    def add_arguments(self, parser):
        parser.add_argument(
            '--top', type=int, default=5,
            help='Cantidad de géneros a recomendar (default: 5)'
        )
        parser.add_argument(
            '--genero', type=int,
            help='ID del género para recomendar libros en ese género'
        )

    def handle(self, *args, **options):
        genero_id = options.get('genero')
        top_n = options.get('top')

        if genero_id:
            # Recomendar libros de un género específico
            try:
                genero = Genero.objects.get(pk=genero_id)
            except Genero.DoesNotExist:
                self.stdout.write(self.style.ERROR(f"No existe el género con id {genero_id}"))
                return

            self.stdout.write(f"\nLibros recomendados para el género '{genero.nombre}':\n")
            libros = (
                Libro.objects.filter(genero=genero)
                .annotate(total_puntuaciones=Count('calificaciones'),
                          promedio=Avg('calificaciones__puntuacion'))
                .order_by('-total_puntuaciones', '-promedio', 'titulo')
            )

            if not libros:
                self.stdout.write("No hay libros en este género.")
                return

            for idx, libro in enumerate(libros[:10], 1):
                self.stdout.write(f"{idx}. {libro.titulo} "
                                f"(Puntuaciones: {libro.total_puntuaciones}, "
                                f"Promedio: {libro.promedio:.2f} "
                                f"Autor: {libro.autor.nombre})")

            self.stdout.write("\n¡Fin de la recomendación de libros!\n")

        else:
            # Recomendar géneros por cantidad de puntuaciones
            self.stdout.write("\nBuscando géneros con más puntuaciones...\n")
            generos = (
                Genero.objects
                .annotate(total_puntuaciones=Count('libros__calificaciones'))
                .order_by('-total_puntuaciones')
            )

            if not generos:
                self.stdout.write("No hay géneros registrados.")
                return

            self.stdout.write("Ranking de géneros recomendados por cantidad de puntuaciones:\n")
            for idx, genero in enumerate(generos[:top_n], 1):
                self.stdout.write(f"{idx}. {genero.nombre}: {genero.total_puntuaciones} puntuaciones")

            genero_top = generos.first()
            if genero_top:
                self.stdout.write(f"\n★ Género más popular recomendado: {genero_top.nombre.upper()} ★\n")
