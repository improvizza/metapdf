# -*- encoding: utf-8 -*-
#
#Notas:
#La función "walk" es útil para recorrer todos los ficheros y directorios que se encuentran incluidos en un directorio concreto.
#

from PyPDF2 import PdfFileReader, PdfFileWriter #importamos modulo y librerias
import os
from stat import *
import os,sys,argparse,time,re

def banner():
	print '''
  __  __ ______ _______       _____  _____  ______ 
 |  \/  |  ____|__   __|/\   |  __ \|  __ \|  ____|
 | \  / | |__     | |  /  \  | |__) | |  | | |__   
 | |\/| |  __|    | | / /\ \ |  ___/| |  | |  __|  
 | |  | | |____   | |/ ____ \| |    | |__| | |     _
 |_|  |_|______|  |_/_/    \_\_|    |_____/|_|    |_|
                                                  
					-by mike-
'''

def isgroupreadable(filepath):
  st = os.stat(filepath)
  return bool(st.st_mode & stat.S_IRGRP)

def printMeta():
	for dirpath, dirnames, files in os.walk("/home/mike/Escriptori/test"): 
		#calculo para el marco de asteriscos..
		tabpath=''

		namelength=0
		for name in files:
			if len(dirpath+os.path.sep+name)<41:
				tabpath="\t\t\t"
			else: tabpath="\t\t"
			if namelength < len(name): namelength=len(name)
		print "*"*(66)
		print "** Actual directory: "+dirpath+tabpath+"**"
		print "** Permissions\t\tFileName\t\tFileSize\t**"
		for name in files:
			name2print=''
			tabs=''
			if len(name) > 15: 
				name2print=name[:15]+"~.pdf"
				tabs="\t"
			elif len(name) <8:
				name2print=name
				tabs="\t\t\t"
			else: 
				name2print=name
				tabs="\t\t"
			print "** "+oct(os.stat(dirpath+os.path.sep+name)[ST_MODE])[-3:]+"\t\t\t"+name2print+tabs+str(os.stat(dirpath+os.path.sep+name).st_size/1024)+" KB\t\t**"
		print "*"*(66)+"\n"
		#print dirnames
		
		#print files
		for name in files:
			ext = name.lower().rsplit('.', 1)[-1]
			if ext in ['pdf']:
				print " "*20+"*"*(6+len(name))
				print " "*20+"** "+name+" **"
				print " "*20+"*"*(6+len(name))
				pdfFile = PdfFileReader(file(dirpath+os.path.sep+name, 'rb'))
				docInfo = pdfFile.getDocumentInfo()
				pages = pdfFile.getNumPages()#Calculates the number of pages in this PDF file.
				isenc=pdfFile.isEncrypted #Read-only boolean property showing whether this PDF file is encrypted.'''
				
				#abrimos el archivo para leer cabecera
				fo = open(dirpath+os.path.sep+name, "rb")
				# read the file header to get the PDF version information.
				head = fo.read(8)
				fo.close()
				#recolectamos información xmp si existe
				xmpinfo = docInfo.getXmpMetadata()
				xmparray=[]
				if hasattr(xmpinfo,'dc_contributor'): xmparray.append('dc_contributor:\t\t'+xmpinfo.dc_contributor)
				elif hasattr(xmpinfo,'dc_identifier'): xmparray.append('dc_identifier:\t\t'+xmpinfo.dc_identifier)
				elif hasattr(xmpinfo,'dc_date'): xmparray.append('dc_date:\t\t'+xmpinfo.dc_date)
				elif hasattr(xmpinfo,'dc_source'): xmparray.append('dc_source:\t\t'+xmpinfo.dc_source)
				elif hasattr(xmpinfo,'dc_subject'): xmparray.append('dc_subject:\t\t'+xmpinfo.dc_subject)
				elif hasattr(xmpinfo,'xmp_modifyDate'): xmparray.append('xmp_modifyDate:\t\t'+xmpinfo.xmp_modifyDate)
				elif hasattr(xmpinfo,'xmp_metadataDate'): xmparray.append('xmp_metadataDate:\t\t'+xmpinfo.xmp_metadataDate)
				elif hasattr(xmpinfo,'xmpmm_documentId'): xmparray.append('xmpmm_documentId:\t\t'+xmpinfo.xmpmm_documentId)
				elif hasattr(xmpinfo,'xmpmm_instanceId'): xmparray.append('xmpmm_instanceId:\t\t'+xmpinfo.xmpmm_instanceId)
				elif hasattr(xmpinfo,'pdf_keywords'): xmparray.append('pdf_keywords:\t\t'+xmpinfo.pdf_keywords)
				elif hasattr(xmpinfo,'pdf_pdfversion'): xmparray.append('pdf_pdfversion:\t\t'+xmpinfo.pdf_pdfversion)
				elif hasattr(xmpinfo,'dc_publisher'):
					for y in xmpinfo.dc_publisher:
						if y:
							 xmparray.append("Publisher:\t" + y)
				
				#horas del archivo
				print "\nInformación del archivo en disco"

				(mode, ino, dev, nlink, uid, gid, size, atime, mtime, ctime) = os.stat(dirpath+os.path.sep+name)

				# time.strftime("%d/%m/%Y %H:%M:%S",time.localtime(st.ST_CTIME))
				print "** File path:\t\t%s" %(dirpath+os.path.sep+name)
				print "** Creción:\t\t%s" % time.ctime(ctime)
				print "** Última modificación:\t%s" % time.ctime(mtime)
				print "** Último acceso:\t%s" % time.ctime(atime)
				#print "Size:\t" % os.path.getsize(args.file)
				
				
				print "\nInformación del archivo en metadatos"
				# print pdf header
				print "** Cabecera PDF:\t%s"%head
				
				#imprimimos los metadatos extraídos con PyPDF2
				for metaItem in docInfo:
					if len(metaItem) > 10: tabs=":\t"
					else: tabs=":\t\t"
					print '** ' + metaItem[1:] + tabs + docInfo[metaItem]
				
				#impimimos el número de páginas en el pdf
				print '** Páginas:\t\t'+str(pages)
				
				#imprimimos información xmp
				if xmparray:
					print "** XMP info:\t\t"+xmparray
				else: print "** XMP info:\t\tNo hay información XMP"
				xmparray=[]				
				
				#Imprimimos si el archivo esta cifrado o no
				if isenc: print '** Cifrado:\t\tEl archivo está cifrado!'
				else: print '** Cifrado:\t\tEl archivo no está cifrado'
				print "\n"


banner()
printMeta()

#https://pythonhosted.org/PyPDF2/PdfFileReader.html
