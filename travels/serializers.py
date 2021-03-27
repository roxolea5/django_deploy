from rest_framework import serializers
from .models import User, Zona, Tour, Salida


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'nombre', 'apellidos', 'fechaNacimiento', 'email', 'genero', 'clave', 'tipo')

class Zona2Serializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        # Se define sobre que modelo actua
        model = Zona
        # Se definen los campos a incluir
        fields = ('nombre',)

class TourSerializer(serializers.HyperlinkedModelSerializer):
    zonaSalida = Zona2Serializer(read_only=True)
    """ Serializador para atender las conversiones para Zona """
    class Meta:
        # Se define sobre que modelo actua
        model = Tour
        # Se definen los campos a incluir
        fields = ('id', 'nombre', 'slug', 'operador', 'tipoDeTour', 'descripcion', 'pais', 'zonaSalida', 'zonaLlegada', 'salidas' )

class ZonaSerializer(serializers.HyperlinkedModelSerializer):
    #Una zona puede tener muchos tours
    tours_salida = TourSerializer(many=True, read_only=True)
    tours_llegada = TourSerializer(many=True, read_only=True)
    """ Serializador para atender las conversiones para Zona """
    class Meta:
        # Se define sobre que modelo actua
        model = Zona
        # Se definen los campos a incluir
        fields = ('id', 'nombre', 'descripcion', 'longitud', 'latitud', 'tours_salida', 'tours_llegada')

class SalidaSerializer(serializers.HyperlinkedModelSerializer):
    """ Serializador para atender las conversiones para Salida """
    class Meta:
        # Se define sobre que modelo actúa
        model = Salida
        # Se definen los campos a incluir
        fields = ('id', 'fechaInicio', 'fechaFin', 'asientos', 'precio', 'tour')



