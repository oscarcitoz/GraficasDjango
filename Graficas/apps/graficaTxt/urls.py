from django.conf.urls.defaults import patterns,url

urlpatterns = patterns('Graficas.apps.graficaTxt.views',
                     
                       url(r'^cargaTxt/$','cargaTxt_view',name='vista_cargaTxt'), 
                       url(r'^archivosTxt/$','archivosTxt_view',name='vista_archivosTxt'),  
                       url(r'^tablasTxt/(?P<id_archivo>.*)/$','graficaTxt_view',name='vista_tablasTxt'),
                       url(r'^vistaTxt/(?P<id_archivo>.*)/$','mostrarTxt_view',name='vista_archivoTxt'), 
                       url(r'^eliminarTxt/(?P<id_archivo>.*)/$','eliminarTxt_view',name='vista_eliminarTxt'), 
                       )