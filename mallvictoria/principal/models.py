#encoding:utf-8
from django.db import models
import datetime
from django.utils.timezone import utc

# Create your models here.
class Estado(models.Model):
	estado=models.CharField(max_length=30)
	def __unicode__(self):
		return self.estado

class Ciudad(models.Model):
	estado=models.ForeignKey(Estado)
	ciudad=models.CharField(max_length=50)
	def __unicode__(self):
		return self.ciudad

class Categoria(models.Model):
	categoria=models.CharField(max_length=20)
	def __unicode__(self):
		return self.categoria

class Tipo(models.Model):
	tipo=models.CharField(max_length=10)
	def __unicode__(self):
		return self.tipo

class Usuario(models.Model):
	nombre=models.CharField(max_length=40)
	direccion=models.CharField(max_length=150)
	telefono=models.CharField(max_length=20)
	sitioweb=models.URLField(max_length=100)
	correo=models.EmailField(max_length=75)
	password=models.CharField(max_length=20)
	estado=models.ForeignKey(Estado)
	ciudad=models.ForeignKey(Ciudad)
	def __unicode__(self):
		return self.nombre

class Articulo(models.Model):
	#fecha=datetime.timedelta(days=15)+datetime.datetime.now()
	#fecha=datetime.timedelta(days=15)+datetime.datetime.utcnow().replace(tzinfo=utc)
	titulo=models.CharField(max_length=30)
	descripcion=models.CharField(max_length=140)
	fecha_publicacion=models.DateTimeField(auto_now=True)
	fecha_vencimiento=models.DateTimeField(editable=False,null=True)
	costo=models.DecimalField(max_digits=7,decimal_places=2)
	imagen=models.ImageField(upload_to='articulos')
	usuario=models.ForeignKey(Usuario)
	tipo=models.ForeignKey(Tipo)
	categoria=models.ForeignKey(Categoria)
	status=models.SmallIntegerField(default=1,blank=True,null=True)	
	def __unicode__(self):
		return self.titulo
	def save(self, *args, **kwargs):
		fecha=datetime.timedelta(days=15)+datetime.datetime.utcnow().replace(tzinfo=utc)
		self.fecha_vencimiento = fecha
		super(Articulo, self).save(*args, **kwargs)	

class ArticuloUsuario(models.Model):
	usuario=models.ForeignKey(Usuario)
	articulo=models.ForeignKey(Articulo)
	orden=models.SmallIntegerField()
	def __unicode__(self):
		return self.articulo.titulo

class Visita(models.Model):
	articulo=models.ForeignKey(Articulo)
	ip=models.CharField(max_length=15)
	fecha_publicacion=models.DateTimeField(auto_now=True)
	def __unicode__(self):
		return articulo.titulo
	#def create(self, *args, **kwargs):
	#	now=datetime.datetime.utcnow().replace(tzinfo=utc)
	#	ahora=datetime.datetime.today()
	#	super(Visita, self).create(*args, **kwargs)
	#	self.fecha_publicacion = ahora
    