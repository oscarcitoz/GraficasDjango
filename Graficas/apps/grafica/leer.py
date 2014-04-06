import csv
lista={}
f = open('../../media/archivos/table.csv')
lns = csv.reader(f)
i=-1
for line in lns:
    i=i+1
    if i==0:
        lista={i:line}
    if i!=0:
        #hacer operaciones
        lista[i]={'n':i,'fecha':line[0],'valor':line[6]}
for (line, valor) in lista.items():
    print line," :" , valor

print lista[1]['n']
i=1
nombre="hola "+i+ " como estas " 
print nombre