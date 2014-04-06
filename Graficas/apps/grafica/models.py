from django.db import models

class archivos(models.Model):
    archivo_id=models.AutoField(primary_key=True)  
    nombre=models.CharField(max_length=30)
    
    def __unicode__(self):
        return self.nombre
    
class datos(models.Model):
    fecha=models.CharField(max_length=30)
    adjClose=models.CharField(max_length=30)
    archivo=models.ForeignKey(archivos)
    open=models.CharField(max_length=30)
    close=models.CharField(max_length=30)
    volume=models.CharField(max_length=30)
    high=models.CharField(max_length=30)
    low=models.CharField(max_length=30)
    archivo=models.ForeignKey(archivos)
    
    def __unicode__(self):
        return self.periodo
    
class datosGrafica(models.Model):
    archivo=models.ForeignKey(archivos)
    fecha=models.CharField(max_length=30)
    periodo=models.IntegerField()
    precioAjt=models.CharField(max_length=30)
    xCuadrado=models.CharField(max_length=30)
    xy=models.CharField(max_length=30)
        
    def __unicode__(self):
        return self.periodo
    