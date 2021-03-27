from django.db import models

# Create your models here.

class User(models.Model):
    nombre = models.CharField(max_length=40)
    apellidos = models.CharField(max_length=80, null=True, blank=True)
    email = models.EmailField()
    fechaNacimiento = models.DateField(null=True, blank=True)
    GENERO = [
        ("F", "Femenino"),
        ("M", "Masculino")
    ]
    genero = models.CharField(max_length=1, choices=GENERO)
    clave = models.CharField(max_length=40, null=True, blank=True)
    tipo = models.CharField(max_length=44, null=True, blank=True)

    def __str__(self):
      """ Se define la representación en str para User """
      return f"{self.nombre} {self.apellidos}" 

class Zona(models.Model):
    """ Define la tabla Zona """
    nombre = models.CharField(max_length=45)
    descripcion = models.CharField(max_length=256, null=True, blank=True)
    latitud = models.DecimalField(max_digits=8, decimal_places=6, null=True, blank=True)
    longitud = models.DecimalField(max_digits=8, decimal_places=6, null=True, blank=True)

    def __str__(self):
      """ Se define la representación en str para User """
      return f"{self.nombre}"

class Tour(models.Model):
    """ Define la tabla Tour """
    nombre = models.CharField(max_length=145)
    slug = models.CharField(max_length=45, null=True, blank=True)
    operador = models.CharField(max_length=45, null=True, blank=True)
    tipoDeTour = models.CharField(max_length=45, null=True, blank=True)
    descripcion = models.CharField(max_length=256)
    img = models.CharField(max_length=256, null=True, blank=True)
    pais = models.CharField(max_length=45, null=True, blank=True)
    zonaSalida = models.ForeignKey(Zona, on_delete=models.SET_NULL, null=True,
        blank=True, related_name="tours_salida")
    zonaLlegada = models.ForeignKey(Zona, on_delete=models.SET_NULL, null=True,
        blank=True, related_name="tours_llegada")

    def __str__(self):
        return f"{self.nombre}"

class Salida(models.Model):
    """ Define la tabla Salida """
    fechaInicio = models.DateField()
    fechaFin = models.DateField()
    asientos = models.PositiveSmallIntegerField(null=True, blank=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    tour = models.ForeignKey(Tour, related_name="salidas", on_delete=models.CASCADE)#CASCADE ON DELETE TOUR

    def __str__(self):
        return f"{self.tour} {self.fechaInicio} {self.fechaFin}"

class Boleto(models.Model):
    """ Define la tabla Salida """
    metodo_pago = models.CharField(max_length=100)
    usuario = models.ForeignKey(User, related_name="usuarios",null=True,on_delete=models.SET_NULL)
    salida = models.ForeignKey(Salida, related_name="salidas",null=True, on_delete=models.SET_NULL)
    numero_asiento = models.CharField(max_length=4)
    puerta_de_salida = models.PositiveSmallIntegerField(null=True, blank=True)
    STATUS = [
        ("approved", "approved"),
        ("pending", "pending")
    ]
    status = models.CharField(max_length=15, choices=STATUS)

    def __str__(self):
        return f"{self.usuario} {self.salida} "

