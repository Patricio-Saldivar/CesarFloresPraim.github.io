from django.db import models


# Create your models here.

class Familia(models.Model):
    usuario = models.CharField(max_length=25, db_column='usuario', primary_key=True)
    contrasenia1 = models.CharField(max_length=100)
    email = models.CharField(max_length=50)
    celular = models.CharField(max_length=15)
    escuela = models.BooleanField(default=False)
    colonia = models.CharField(default='Nada', max_length=30)
    calle = models.CharField(default='Nada', max_length=30)
    numero = models.CharField(default='Nada', max_length=30)
    cp = models.CharField(default='Nada', max_length=30)
    pasajeros = models.IntegerField(default=3)
    ocupantes = models.IntegerField(default=3)

    def __str__(self):
        return self.usuario


class Solicitud(models.Model):
    usuario_recibe = models.ForeignKey(Familia, on_delete=models.PROTECT, related_name='usuario_recibe')
    usuario_sol = models.ForeignKey(Familia, on_delete=models.PROTECT, related_name='usuario_sol')


class Match(models.Model):
    usuario_auto = models.ForeignKey(Familia, on_delete=models.PROTECT, related_name='usuario_auto')
    usuario_acomodado = models.ForeignKey(Familia, on_delete=models.PROTECT, related_name='usuario_acomodado')
    lunes = models.CharField(max_length=20, default="")
    martes = models.CharField(max_length=20, default="")
    miercoles = models.CharField(max_length=20, default="")
    jueves = models.CharField(max_length=20, default="")
    viernes = models.CharField(max_length=20, default="")


class NoMatch(models.Model):
    usuario_denego = models.ForeignKey(Familia, on_delete=models.PROTECT, related_name='usuario_denego')
    usuario_denegado = models.ForeignKey(Familia, on_delete=models.PROTECT, related_name='usuario_denegado')

class Horario(models.Model):
    usuario_1 = models.ForeignKey(Familia, on_delete=models.PROTECT, related_name='usuario_1')
    usuario_2 = models.ForeignKey(Familia, on_delete=models.PROTECT, related_name='usuario_2')
    lunes = models.CharField(max_length=20)
    martes = models.CharField(max_length=20)
    miercoles = models.CharField(max_length=20)
    jueves = models.CharField(max_length=20)
    viernes = models.CharField(max_length=20)

