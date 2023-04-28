#Codigo propuesto por ChatGPT para convertir el texto en un diccionario
#Prompt: Ahora tenemos el siguiente ecsenario:
	#datos_personales = ```
	#datos personales
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
	#```
	#Pregunta: Si ahora que remos convertir {datos_personales} en un diccionario, como lo hacemos?
	#Teniendo en cuenta tres peculiaridades:
	#1ra. En el caso de "cedula" esta seria la clave, y el valor seria "#402-2474966-9". Es decir, no hay salto de linea. Lo mismo aplica para: "fecha nacimiento" y  "lugar nacimiento"
	#2da. "telefonos" debe quedar de la siguiente manera: telefonos: {
	#casa:"",
	#trabajo:"809-541-4800",
	#celular:"829-355-6165"
	#}
	#3ra. direcciones debe quedar como una lista, asi: direcciones: [
	#* no disponible piso loscartonesosanpabloii los mina norte santo domingo este,
	#* carretera de manoguayabo 250 piso mejoramientosocial,
	#* calle 3 12 apto los minas sur los minas sur distrito nacional/santo domingo
	#]

def obtener_datos_personales(texto):
    # Separa el texto en líneas y elimina cualquier línea vacía
    lineas = [linea.strip() for linea in texto.split("\n") if linea.strip()]

    # Crea un diccionario vacío
    diccionario = {}

    # Itera sobre cada línea y agrega la clave y el valor al diccionario
    for i, linea in enumerate(lineas):
        if i == 0:
            clave = "datos personales"
            valor = ""
        elif "telefonos" in linea:
            clave = "telefonos"
            valor = {}
            while i < len(lineas) - 1 and ":" not in lineas[i+1]:
                i += 1
                tipo_telefono, numero = lineas[i].split(":")
                valor[tipo_telefono.strip()] = numero.strip()
        elif "direcciones" in linea:
            clave = "direcciones"
            valor = []
            while i < len(lineas) - 1 and ":" not in lineas[i+1]:
                i += 1
                valor.append(lineas[i])
        elif ":" in linea:
            clave, valor = linea.split(":", maxsplit=1)
            clave = clave.strip()
            valor = valor.strip()
            if clave in ["cedula", "fecha nacimiento", "lugar nacimiento"]:
                valor = valor.replace("\n", " ")
        else:
            valor = linea.strip()
        diccionario[clave] = valor

    return diccionario


datos_personales = """datos personales
cedula #402-2474966-9
nombres
fresa matilde
apellidos
molina sanchez
fecha nacimiento 29/07/1996
edad
26 anos
ocupacion
lugar nacimiento montecristi, r.d.
pasaporte
estado civil
soltero/a
telefonos
casa:
trabajo: 809-541-4800
celular: 829-355-6165
direcciones
* no disponible piso loscartonesosanpabloii los mina norte santo domingo este
* carretera de manoguayabo 250 piso mejoramientosocial
* calle 3 12 apto los minas sur los minas sur distrito nacional/santo domingo
"""

diccionario = obtener_datos_personales(datos_personales)
print(diccionario)
# Salida:
# {'datos personales': '', 'cedula': '#402-2474966-9', 'nombres': 'fresa matilde', 'apellidos': 'molina sanchez',
#  'fecha nacimiento': '29/07/1996', 'edad': '26 anos', 'ocupacion': '', 'lugar nacimiento': 'montecristi, r.d.',
#  'pasaporte': '', 'estado civil': 'soltero/a', 'telefonos': {'casa': '', 'trabajo': '809-541-4800',
#  'celular': '829-355-6165'}, 'direcciones': ['* no disponible piso loscartonesosanpabloii los mina norte santo domingo este',
#  '* carretera de manoguayabo 250 piso mejoramientosocial', '* calle 
