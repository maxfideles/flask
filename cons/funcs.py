import math
import sys
import re

#Calculo do consumo anual
def consumoAnual(data):
	totp=0
	tot=0
	for a in data:
		totp=totp+float(a[0].replace(',','.'))
	totp=totp/0.64
	for a in data:
		tot=tot+float(a[1].replace(',','.'))+float(a[2].replace(',','.'))
	tot=tot+totp
	return(tot)

#Tabela de demanda e consumo
def getConDem(pdftext):
	info = pdftext[pdftext.find("PERÍODOC")+len("PERÍODOC"):pdftext.rfind("PERÍODOUFER")]
	consumo = [['.' for x in range(3)] for y in range(12)]
	demanda = [['.' for x in range(3)] for y in range(12)]
	datas = ['.' for y in range(12)]
	info = info[info.rfind('.'):len(info)]
	info = info.split(' / ')
	info=info[0:13]
	for line in range(len(info)):
		if(line<12):
			datas[line]=info[line][len(info[line])-3:len(info[line])]+"/"+info[line+1][0:2]
			indexes = [x.start() for x in re.finditer(',', info[line+1])]
			consumo[line][0]=info[line+1][2:indexes[0]+3]
			consumo[line][1]=info[line+1][indexes[0]+3:indexes[1]+3]
			consumo[line][2]=info[line+1][indexes[1]+3:indexes[2]+3]
			demanda[line][0]=info[line+1][indexes[2]+3:indexes[3]+5]
			demanda[line][1]=info[line+1][indexes[3]+5:indexes[4]+5]
			demanda[line][2]=info[line+1][indexes[4]+5:indexes[5]+5]
	return(consumo, demanda, datas)

#Demanda contratada e valor da tarifa
def getInfo(pdftext, mD):
	demandaCon = pdftext[pdftext.rfind("DEMANDA")+len("DEMANDA"):pdftext.rfind("CÓDIGO")]
	demandaCon = float(demandaCon.replace(',','.'))
	indices = [x.start() for x in re.finditer('DEMANDA', pdftext)]
	pr=['' for x in range(len(indices))]
	for val in range(len(indices)):
		if((pdftext[indices[val]:indices[val]+30]).find('*')!=-1):
			temp=pdftext[indices[val]:indices[val]+30]
			temp=temp[temp.find('*')-9:temp.find('*')]
			valTarifa=temp

	valTarifa = float(valTarifa.replace(',','.'))
	return(demandaCon, valTarifa)

def melhorDemanda(dl, dc, tarif):
	dn=dc
	dna=0
	valAnoa=float('inf')
	while(True):
		valAno=0
		for mes in dl:
			if(max(mes)>1.05*dn):
				valAno=valAno+(max(mes)-dn)*2*tarif
			valAno=valAno+max([dn, max(mes)])*tarif
		if(dn==dc):
			valAnob=valAno
		dna=dn
		
		if(valAno<valAnoa):
			dn=dn-1
			valAnoa=valAno
		else:
			dn=dna
			break;
	return(dn, valAnoa, valAnob)
