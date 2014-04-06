from django.conf.urls.defaults import patterns,url

urlpatterns = patterns('Graficas.apps.grafica.views',
                       url(r'^$','index_view',name='vista_principal'),
                       url(r'^tablasCsv/1d/(?P<id_archivo>.*)/$','grafica1d_view',name='vista_tablasCsv'),
                       url(r'^tablasCsv/1m/(?P<id_archivo>.*)/$','grafica1m_view',name='vista_tablasCsv'), 
                       url(r'^tablasCsv/1a/(?P<id_archivo>.*)/$','grafica1a_view',name='vista_tablasCsv'),  
                       url(r'^tablasCsv/6m/(?P<id_archivo>.*)/$','grafica6m_view',name='vista_tablasCsv'), 
                       url(r'^cargaCsv/$','carga_view',name='vista_cargaCsv'), 
                       url(r'^archivosCsv/$','archivos_view',name='vista_archivosCsv'), 
                       url(r'^error/$','error_view',name='vista_error'),
                       url(r'^vistaCsv/(?P<id_archivo>.*)/$','mostrar_view',name='vista_archivoCsv'),
                       url(r'^eliminarCsv/(?P<id_archivo>.*)/$','eliminar_view',name='vista_eliminarCsv'),
                       )