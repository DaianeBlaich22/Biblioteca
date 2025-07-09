from rest_framework import serializers
from .models import Autor, Genero, Libro, Calificacion
from django.contrib.auth.models import User

class AutorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Autor
        fields = '__all__'

class GeneroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genero
        fields = '__all__'

class LibroSerializer(serializers.ModelSerializer):
    autor = AutorSerializer(read_only=True)
    genero = GeneroSerializer(read_only=True)
    autor_id = serializers.PrimaryKeyRelatedField(queryset=Autor.objects.all(), source='autor', write_only=True)
    genero_id = serializers.PrimaryKeyRelatedField(queryset=Genero.objects.all(), source='genero', write_only=True)

    class Meta:
        model = Libro
        fields = ['id', 'titulo', 'autor', 'autor_id', 'genero', 'genero_id', 'fechalanzamiento', 'isbn', 'enlace']

class CalificacionSerializer(serializers.ModelSerializer):
    usuario = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Calificacion
        fields = ['id', 'libro', 'usuario', 'puntuacion']
