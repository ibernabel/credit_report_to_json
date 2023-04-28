#datos_personales = """datos personales
#cedula #402-2474966-9
#nombres
#fresa matilde
#apellidos
#molina sanchez
#fecha nacimiento 29/07/1996
#edad
#26 anos
#ocupacion
#lugar nacimiento montecristi, r.d.
#pasaporte
#estado civil
#soltero/a
#telefonos
#casa:
#trabajo: 809-541-4800
#celular: 829-355-6165
#direcciones
#* no disponible piso loscartonesosanpabloii los mina norte santo domingo este
#* carretera de manoguayabo 250 piso mejoramientosocial
#* calle 3 12 apto los minas sur los minas sur distrito nacional/santo domingo
#"""
#print("legal" in datos_personales)

datos = """nombres
fresa matilde
apellidos
molina sanchez"""

#palabras = datos.split()  # dividir la cadena en una lista de palabras
#print(len(palabras))
#print(palabras)


nombres_index = datos.find("nombres")
apellidos_index = datos.find("apellidos")

#print(nombres_index)
#print(apellidos_index)

print(f'Nombres: {datos[nombres_index + 8 : apellidos_index - 1]}')
print(f'Apellidos: {datos[apellidos_index + 10 :]}')

#if "nombres" in palabras:
#    indice_nombres = palabras.index("nombres")
#    if "apellidos" in palabras[indice_nombres:]:
#        indice_apellidos = palabras[indice_nombres:].index("apellidos") + indice_nombres
#        nombres = " ".join(palabras[indice_nombres+1:indice_apellidos])
#        print(nombres)  # imprimir los nombres encontrados

#print(text.count("transunion credit vision score"))
