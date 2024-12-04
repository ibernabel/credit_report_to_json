## Objetivo: Conseguir un analizador de reportes de historial de credito de Transunion.

### Problemas: Se debe analizar el reporte que viene en formato pdf, pasarlo a un formato que pueda ser leido por un programa.

### Luego hay que convertir el texto en un formato de objeto: diccionario de python.

### Con los datos en formato de diccionario, se puede usar de diferentes formas: Se puede usar para crear un API, para actualizar datos en la base de datos. O se puede usar en una funcionalidad que analize e interprete el reporte de credito. Posiblemente usando una herramienta como GPT-4

Pasos:

[x] Crear funcionalidad para leer el archivo pdf y convertirlo a texto plano. 

[x] A partir del texto plano, convertirlo en un diccionario despues de analizar sus estructura.

[x] Este diccionario, exportarlo en formato JSON para usarlo en otras herramientas.

[ ] Crear herramienta que analize e interprete el Reporte de Credito usando un LLM como GPT-4.
