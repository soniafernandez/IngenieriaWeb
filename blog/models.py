# -*- coding: utf-8 -*-
from django.db import models
from django.utils import timezone
from django.dispatch import receiver
import os

# Create your models here.


unidad_choices = (
	('',''),
	('g','gramos'),
	('ml','mililitros'),
	('tsp','cucharadita'),
	('tbsp','cucharada'),
	)

class Receta(models.Model):
	nombre = models.CharField (max_length = 200 )
	foto = models.ImageField (upload_to = 'photos/', blank = True, null = True)
	sabias_que = models.TextField (verbose_name = '¿Sabías que...?')
	pasos = models.TextField (verbose_name = 'Pasos a seguir')
	fecha_publicacion = models.DateTimeField ( blank = True, null = True)
	autor = models.ForeignKey('auth.User', related_name='recetas')

	def publicar(self):
		self.fecha_publicacion = timezone.now()
		self.save()

	def __str__(self):
		return "%s" % self.nombre

class Ingredientes(models.Model):
	receta = models.ForeignKey(Receta, on_delete=models.CASCADE, related_name='ingredientes')
	cantidad = models.PositiveIntegerField()
	unidad = models.CharField(max_length= 4, choices= unidad_choices)
	alimento = models.ForeignKey('Alimento', blank=True, null=True)

	def __str__(self):
		return "%i%s %s" % (self.cantidad, self.unidad, self.alimento)
	

class Alimento(models.Model):
	nombre = models.TextField()
	codigo = models.CharField(max_length=10,primary_key=True)

	def __str__(self):
		return"%s" % self.nombre

#Funcion para borrar el archivo de la fotografia

@receiver(models.signals.post_delete, sender=Receta)
def auto_delete_file_on_delete(sender, instance, **kwargs):
	if instance.foto:
		if os.path.isfile(instance.foto.path):
			os.remove(instance.foto.path)

@receiver(models.signals.pre_save, sender=Receta)
def auto_delete_file_on_change(sender, instance, **kwargs):
	if not instance.pk:
		return False

	try:
		old_foto = Receta.objects.get(pk=instance.pk).foto
	except Receta.DoesNotExist:
		return False
	new_foto = instance.foto
	if not old_foto == new_foto:
		if os.path.isfile(old_foto.path):
			os.remove(old_foto.path)

