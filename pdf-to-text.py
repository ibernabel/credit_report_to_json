#Import libraries
import fitz #PyMuPDF (PDF extractor)
import unidecode #format accents
import sys #Module for interacting with the system and the Python interpreter

#Read, process and export file to txt
print('Enter the file name (without: ".pdf"):')
input_name = input()
file_name = f'{input_name}'

fname = f'./credit_reports/{file_name}.pdf'

#Raise error if PDF file has not found with provided name
try:
	doc = fitz.open(fname)  
except fitz.fitz.FileNotFoundError:
    print(f'No such file called:  {file_name}')
    sys.exit()

data = ''
for page in doc:  
    data += page.get_text() 

text = data.lower() 
text = unidecode.unidecode(text)

#print(text)

##Save the file
with open(f'{file_name}.txt', 'w') as f:
    f.write(text)

#building variables and table
#nombres_index = text.find("nombres")
#apellidos_index = text.find("apellidos")

##print(nombres_index)
##print(apellidos_index)

#print(f'Nombres: {text[nombres_index + 8 : apellidos_index - 1]}')
#print(f'Apellidos: {text[apellidos_index + 10 :]}')

##Analize text

#has_legal = text.find("legal") != -1
#has_castigado = text.find("castigado") != -1
#has_mora = text.find("mora") != -1

#print("mora" in text)
##print(text.count("mora"))



#puntuacion_index = text.rfind("puntuacion") + 11
#puntuacion = text[puntuacion_index:puntuacion_index +  3]
#print(f'Puntuacion Data: {puntuacion}')

#fecha_nacimiento_index = text.find("fecha nacimiento") + 17
#fecha_nacimiento = text[fecha_nacimiento_index:fecha_nacimiento_index + 10 ]
#print(f'Fecha de nacimiento: {fecha_nacimiento}')


#This code is base on the code share for:
#Autor: Jeanna Schoonmaker
#AuthorURL: https://medium.com/@jeanna-schoonmaker
#ArticleURL: https://medium.com/social-impact-analytics/comparing-4-methods-for-pdf-text-extraction-in-python-fd34531034f