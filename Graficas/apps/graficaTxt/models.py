from django.db import models

class archivosTxt(models.Model):
    archivo_id=models.AutoField(primary_key=True)  
    nombre=models.CharField(max_length=30)
    def __unicode__(self):
        return self.nombre
    
class datosTxt(models.Model):
    periodo=models.IntegerField()
    precioAjt=models.CharField(max_length=30)
    archivo=models.ForeignKey(archivosTxt)
    
    def __unicode__(self):
        return self.periodo
    
class datosTxtGrafica(models.Model):
    archivo=models.ForeignKey(archivosTxt)
    periodo=models.FloatField()
    precioAjt=models.CharField(max_length=30)
    xCuadrado=models.CharField(max_length=30)
    xy=models.CharField(max_length=30)
        
    def __unicode__(self):
        return self.periodo
    