# libros/serializers.py
from rest_framework import serializers
from .models import Autor, Libro, Calificacion, Genero
from django.contrib.auth.models import User

# Serializador para Autor
class AutorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Autor
        fields = '__all__'

# Serializador para Libro
class LibroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Libro
        fields = '__all__'

# Serializador para Calificación
class CalificacionSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Calificacion
        fields = ['id', 'libro', 'puntaje', 'username']  # 'user' no es necesario si usas 'username'

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class GeneroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genero
        fields = '__all__'