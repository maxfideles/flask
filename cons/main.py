import PyPDF2
import pandas
import numpy
import re
import math
from cons import funcs
import ocrmypdf
import os
import werkzeug
from tkinter import filedialog
from shutil import copy

def principal():
	ocrmypdf.ocr(os.getcwd()+'\\TEMP\\temp.pdf','output.pdf',redo_ocr=True,output_type='pdf')
	res=['','','','','','','','','','','','']
	pdfFileObj = open('output.pdf','rb')
	pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
	pageObj0 = pdfReader.getPage(0)
	pageObj2 = pdfReader.getPage(2)
	pdftext2=pageObj2.extractText()
	pdftext0=pageObj0.extractText()
	pdfFileObj.close()
	os.remove(r'output.pdf')
	os.remove(os.getcwd()+'\\TEMP\\temp.pdf')
	consumo, demanda, datas = funcs.getConDem(pdftext2)
	conAn=funcs.consumoAnual(consumo)
	projecao=conAn/12/125
	# print("Consumo Anual = "+str(conAn))
	res[0]=conAn
	# print("Potência estimada do sistema = "+str(projecao))
	res[1]=projecao
	# print("Numero aproximado de modulos = "+str(projecao*1000/400))
	res[2]=projecao*1000/400
	for a in demanda:
		a[0]=float(a[0].replace(',','.'))
		a[1]=float(a[1].replace(',','.'))
		a[2]=float(a[2].replace(',','.'))
	for a in consumo:
		a[0]=float(a[0].replace(',','.'))
		a[1]=float(a[1].replace(',','.'))
		a[2]=float(a[2].replace(',','.'))

	mdLida = max(map(max,demanda))	
	demandaC, Tarifa= funcs.getInfo(pdftext0, mdLida)
	# print("Maior demanda lida anual = "+str(mdLida))
	res[3]=mdLida
	nd=math.ceil(mdLida*0.95238)
	# print("Nova demanda = "+str(nd)+" com um limite de "+str(nd*1.05))
	# print("Economia de  R$"+str((demandaC-nd)*Tarifa))
	res[4]=nd
	res[5], res[7], valAnob=funcs.melhorDemanda(demanda, demandaC, Tarifa)
	res[7]=valAnob-res[7]
	res[6]=valAnob-nd*12*Tarifa
	res[8]=datas
	res[9]=consumo
	res[10]=demanda
	res[11]=demandaC
	return(res)