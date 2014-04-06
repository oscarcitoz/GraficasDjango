from django.shortcuts import render_to_response
from django.db.models import Max,Avg,Sum
from django.template import RequestContext
from Graficas.apps.grafica.models import archivos,datos,datosGrafica
from Graficas.apps.grafica.forms import Upload
from django.http import HttpResponseRedirect
import csv



def index_view(request):
    return render_to_response('index.html',context_instance=RequestContext(request))

def carga_view(request):
    lista={}
    infor=""
    tipo="CSV"
    if request.method=="POST":
        form=Upload(request.POST)
        if form.is_valid():
                nombre=form.cleaned_data['nombre']
                try:
                    f = open('Graficas/media/archivos/'+nombre+'.csv')
                except:
                    return HttpResponseRedirect("../error")
                lns = csv.reader(f)  
                a=archivos()
                a.nombre=nombre
                a.save()
                numero=archivos.objects.aggregate(Max('archivo_id'))
                #numero=archivos.objects.raw('select max(archivo_id')
                j=0
                i=-1
                promX=0
                promP=0
                for line in lns:
                    if len(line)>7:
                        return HttpResponseRedirect("../../error")
                    i=i+1
                    j=j+1
                    if i==0:
                        lista={i:line}
                    if i!=0:
                        #hacer operaciones
                        lista[i]={'fecha':line[0],'open':line[1],'high':line[2],'low':line[3],'close':line[4],'volume':line[5],'valor':line[6]}
                        d=datos()
                        d.archivo_id=numero['archivo_id__max']
                        d.fecha=lista[i]['fecha']
                        d.adjClose=lista[i]['valor']
                        promP=promP+(float(lista[i]['valor']))
                        d.open=lista[i]['open']
                        d.high=lista[i]['high']
                        d.low=lista[i]['low']
                        d.close=lista[i]['close']
                        d.volume=lista[i]['volume']
                        d.save()
         
                f.close()
                maxX=j-1
                f = open('Graficas/media/archivos/'+nombre+'.csv')    
                lns=csv.reader(f)
                i=-1
                sumX2=0
                sumXY=0    
                for line in lns:
                    if len(line)>7:
                        return HttpResponseRedirect("../../error")
                    i=i+1
                    if i==0:
                        lista={i:line}
                    if i!=0:
                        j=j-1
                        #hacer operaciones
                        lista[i]={'fecha':line[0],'valor':line[6]}
                        d=datosGrafica()
                        d.fecha=lista[i]['fecha']
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
                s=datosGrafica.objects.filter(archivo_id=numero['archivo_id__max']).aggregate(Avg('periodo'))
                promX=s['periodo__avg']
                promP=promP/maxX
                b1=sumXY-(maxX*promX*promP)
                b2=sumX2-(maxX*promX*promX)
                b=b1/b2
                a=promP-b*promX 
                diaP=maxX+1
                diaSig=(diaP*b)+a
                d=datosGrafica()
                d.archivo_id=numero['archivo_id__max']
                d.periodo=diaP
                d.precioAjt=diaSig
                d.xCuadrado=diaP*diaP
                d.xy=diaP*diaSig
                d.fecha="xxx"
                d.save()
                infor=" Se cargo correctamente el archivo a la base de datos "
                ctx={'informacion':infor}
                return render_to_response('csv/respuesta.html',ctx,context_instance=RequestContext(request)) 
        else:
            form=Upload()
            infor="No se cargo correctamente el archivo en la base de datos"
            ctx={'form':form,'informacion':infor,'tipo':tipo}
            return render_to_response('csv/carga.html',ctx,context_instance=RequestContext(request))  
    else:
        form=Upload()
        ctx={'form':form,'tipo':tipo}
        return render_to_response('csv/carga.html',ctx,context_instance=RequestContext(request))

def grafica1d_view(request,id_archivo):
    w=id_archivo
    registro2=datosGrafica.objects.filter(archivo_id=w).count()
    limite=registro2-5
    registro=datosGrafica.objects.filter(archivo_id=w).order_by('periodo')
    s=datosGrafica.objects.filter(archivo_id=w,periodo__gt=limite).aggregate(Avg('periodo'))
    promX=s['periodo__avg']
    p=datosGrafica.objects.filter(archivo_id=w,periodo__gt=limite).aggregate(Avg('precioAjt'))
    promP=p['precioAjt__avg']
    xy=datosGrafica.objects.filter(archivo_id=w,periodo__gt=limite).aggregate(Sum('xy'))
    sumXY=xy['xy__sum']
    x2=datosGrafica.objects.filter(archivo_id=w,periodo__gt=limite).aggregate(Sum('xCuadrado'))
    sumX2=x2['xCuadrado__sum']
    maxX=datosGrafica.objects.filter(archivo_id=w)[limite:registro2].count()
    b1=sumXY-(maxX*promX*promP)
    b2=sumX2-(maxX*promX*promX)
    b=b1/b2
    a=promP-b*promX 
    ctx={'registro':registro,'registro2':registro2,'limite':limite,'a':a,'b':b}
    return render_to_response('csv/tablas.html',ctx,context_instance=RequestContext(request))

def grafica1m_view(request,id_archivo):
    w=id_archivo
    registro2=datosGrafica.objects.filter(archivo_id=w).count()
    limite=registro2-21
    registro=datosGrafica.objects.filter(archivo_id=w).order_by('periodo')
    s=datosGrafica.objects.filter(archivo_id=w,periodo__gt=limite).aggregate(Avg('periodo'))
    promX=s['periodo__avg']
    p=datosGrafica.objects.filter(archivo_id=w,periodo__gt=limite).aggregate(Avg('precioAjt'))
    promP=p['precioAjt__avg']
    xy=datosGrafica.objects.filter(archivo_id=w,periodo__gt=limite).aggregate(Sum('xy'))
    sumXY=xy['xy__sum']
    x2=datosGrafica.objects.filter(archivo_id=w,periodo__gt=limite).aggregate(Sum('xCuadrado'))
    sumX2=x2['xCuadrado__sum']
    maxX=datosGrafica.objects.filter(archivo_id=w)[limite:registro2].count()
    b1=sumXY-(maxX*promX*promP)
    b2=sumX2-(maxX*promX*promX)
    b=b1/b2
    a=promP-b*promX 
    ctx={'registro':registro,'registro2':registro2,'limite':limite,'a':a,'b':b}
    return render_to_response('csv/tablas.html',ctx,context_instance=RequestContext(request))

def grafica1a_view(request,id_archivo):
    w=id_archivo
    registro2=datosGrafica.objects.filter(archivo_id=w).count()
    registro=datosGrafica.objects.filter(archivo_id=w).order_by('periodo')
    limite=registro2-252
    s=datosGrafica.objects.filter(archivo_id=w,periodo__gt=limite).aggregate(Avg('periodo'))
    promX=s['periodo__avg']
    p=datosGrafica.objects.filter(archivo_id=w,periodo__gt=limite).aggregate(Avg('precioAjt'))
    promP=p['precioAjt__avg']
    xy=datosGrafica.objects.filter(archivo_id=w,periodo__gt=limite).aggregate(Sum('xy'))
    sumXY=xy['xy__sum']
    x2=datosGrafica.objects.filter(archivo_id=w,periodo__gt=limite).aggregate(Sum('xCuadrado'))
    sumX2=x2['xCuadrado__sum']
    maxX=datosGrafica.objects.filter(archivo_id=w)[limite:registro2].count()
    b1=sumXY-(maxX*promX*promP)
    b2=sumX2-(maxX*promX*promX)
    b=b1/b2
    a=promP-b*promX 
    ctx={'registro':registro,'registro2':registro2,'limite':limite,'a':a,'b':b}
    return render_to_response('csv/tablas.html',ctx,context_instance=RequestContext(request))

def grafica6m_view(request,id_archivo):
    w=id_archivo
    registro2=datosGrafica.objects.filter(archivo_id=w).count()
    limite=registro2-126
    registro=datosGrafica.objects.filter(archivo_id=w).order_by('periodo')
    s=datosGrafica.objects.filter(archivo_id=w,periodo__gt=limite).aggregate(Avg('periodo'))
    promX=s['periodo__avg']
    p=datosGrafica.objects.filter(archivo_id=w,periodo__gt=limite).aggregate(Avg('precioAjt'))
    promP=p['precioAjt__avg']
    xy=datosGrafica.objects.filter(archivo_id=w,periodo__gt=limite).aggregate(Sum('xy'))
    sumXY=xy['xy__sum']
    x2=datosGrafica.objects.filter(archivo_id=w,periodo__gt=limite).aggregate(Sum('xCuadrado'))
    sumX2=x2['xCuadrado__sum']
    maxX=datosGrafica.objects.filter(archivo_id=w)[limite:registro2].count()
    b1=sumXY-(maxX*promX*promP)
    b2=sumX2-(maxX*promX*promX)
    b=b1/b2
    a=promP-b*promX 
    ctx={'registro':registro,'registro2':registro2,'limite':limite,'a':a,'b':b}
    return render_to_response('csv/tablas.html',ctx,context_instance=RequestContext(request))

def archivos_view(request):
    registro=archivos.objects.all()
    ctx={'registro':registro}
    return render_to_response('csv/archivos.html',ctx,context_instance=RequestContext(request))

def error_view(request):
    return render_to_response('csv/error.html',context_instance=RequestContext(request))

def mostrar_view(request,id_archivo):
    w=id_archivo
    registro=datos.objects.filter(archivo_id=w)
    ctx={'registro':registro}
    return render_to_response('csv/vista.html',ctx,context_instance=RequestContext(request))

def eliminar_view(request,id_archivo):
    w=id_archivo
    datos.objects.filter(archivo_id=w)
    archivos.objects.filter(archivo_id=w).delete()
    informacion="Archivo eliminado exitosamente"
    registro=archivos.objects.all()
    ctx={'informacion':informacion,'registro':registro}
    return render_to_response('csv/archivos.html',ctx,context_instance=RequestContext(request))
