from django.shortcuts import render_to_response
from django.template import RequestContext
from django.db.models import Max,Avg,Sum
from Graficas.apps.graficaTxt.models import archivosTxt,datosTxt,datosTxtGrafica
from django.http import HttpResponseRedirect
from Graficas.apps.grafica.forms import Upload



def cargaTxt_view(request):
    lista={}
    infor=""
    tipo="TXT"
    if request.method=="POST":
        form=Upload(request.POST)
        if form.is_valid():
                nombre=form.cleaned_data['nombre']
                try: 
                    f= open('Graficas/media/archivos/'+nombre+'.txt','r')
                except:
                    return HttpResponseRedirect("../../error")
                lns = f.readlines()
                i=0  
                a=archivosTxt()
                a.nombre=nombre
                a.save()
                numero=archivosTxt.objects.aggregate(Max('archivo_id'))
                promX=0
                maxX=0
                promP=0
                sumXY=0
                sumX2=0
                for line in lns:
                    
                    line=line.split('|')
                    if len(line)>2:
                        return HttpResponseRedirect("../../error")
                    i=i+1
                        #hacer operaciones     
                    lista[i]={'n':line[0],'valor':line[1]}
                    d=datosTxt()
                    d.periodo=lista[i]['n']
                    j=d.periodo
                    j=float(j)
                    promX=promX+j
                    if j>maxX:
                        maxX=j
                    d.archivo_id=numero['archivo_id__max']
                    d.periodo=j
                    d.precioAjt=lista[i]['valor']
                    promP=promP+(float(lista[i]['valor']))
                    d.save()
                    d=datosTxtGrafica()
                    d.archivo_id=numero['archivo_id__max']
                    d.periodo=j
                    d.precioAjt=lista[i]['valor']
                    d.xCuadrado=j*j
                    sumX2=sumX2+d.xCuadrado
                    k=float(lista[i]['valor'])
                    d.xy=j*k
                    sumXY=sumXY+d.xy
                    d.save()
                f.close()
                maxX=datosTxtGrafica.objects.filter(archivo_id=numero['archivo_id__max']).count()
                promX=promX/maxX
                promP=promP/maxX
                infor=" Se cargo correctamente el archivo a la base de datos "
                b1=sumXY-(maxX*promX*promP)
                b2=sumX2-(maxX*promX*promX)
                b=b1/b2
                a=promP-b*promX 
                diaP=maxX+1
                diaSig=(diaP*b)+a
                d=datosTxtGrafica()
                d.archivo_id=numero['archivo_id__max']
                d.periodo=diaP
                d.precioAjt=diaSig
                d.xCuadrado=diaP*diaP
                d.xy=diaP*diaSig
                d.save()
                ctx={'informacion':infor}
                return render_to_response('csv/respuesta.html',ctx,context_instance=RequestContext(request)) 
        else:
            form=Upload()
            infor="No se guardo correctamente el archivo en la base de datos"
            ctx={'form':form,'informacion':infor,'tipo':tipo}
            return render_to_response('csv/carga.html',ctx,context_instance=RequestContext(request))  
    else:
        form=Upload()
        ctx={'form':form,'tipo':tipo}
        return render_to_response('csv/carga.html',ctx,context_instance=RequestContext(request))
 
def archivosTxt_view(request):
    registro=archivosTxt.objects.all()
    ctx={'registro':registro}
    return render_to_response('txt/archivos.html',ctx,context_instance=RequestContext(request))

def graficaTxt_view(request,id_archivo):
    w=id_archivo
    registro=datosTxtGrafica.objects.filter(archivo_id=w).order_by('periodo')
    registro2=datosTxtGrafica.objects.filter(archivo_id=w).count()
    limite=0
    s=datosTxtGrafica.objects.filter(archivo_id=w,periodo__gt=limite).aggregate(Avg('periodo'))
    promX=s['periodo__avg']
    p=datosTxtGrafica.objects.filter(archivo_id=w,periodo__gt=limite).aggregate(Avg('precioAjt'))
    promP=p['precioAjt__avg']
    xy=datosTxtGrafica.objects.filter(archivo_id=w,periodo__gt=limite).aggregate(Sum('xy'))
    sumXY=xy['xy__sum']
    x2=datosTxtGrafica.objects.filter(archivo_id=w,periodo__gt=limite).aggregate(Sum('xCuadrado'))
    sumX2=x2['xCuadrado__sum']
    maxX=datosTxtGrafica.objects.filter(archivo_id=w)[limite:registro2].count()
    b1=sumXY-(maxX*promX*promP)
    b2=sumX2-(maxX*promX*promX)
    b=b1/b2
    a=promP-b*promX 
    ctx={'registro':registro,'registro2':registro2,'a':a,'b':b}
    return render_to_response('csv/tablas.html',ctx,context_instance=RequestContext(request))

def mostrarTxt_view(request,id_archivo):
    w=id_archivo
    registro=datosTxt.objects.filter(archivo_id=w).order_by('periodo')
    ctx={'registro':registro}
    return render_to_response('txt/vista.html',ctx,context_instance=RequestContext(request))

def eliminarTxt_view(request,id_archivo):
    w=id_archivo
    datosTxt.objects.filter(archivo_id=w).delete()
    archivosTxt.objects.filter(archivo_id=w).delete()
    informacion="Archivo eliminado exitosamente"
    registro=archivosTxt.objects.all()
    ctx={'informacion':informacion,'registro':registro}
    return render_to_response('txt/archivos.html',ctx,context_instance=RequestContext(request))


