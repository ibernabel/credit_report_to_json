#import pandas as pd

#with open("./output_text/idequel.txt", "r") as file:
#    content = file.read()

file = open("./output_text/idequel.txt", "r")
text = file.read()

rnc_index = text.find("rnc")

#inquirer data indexes
subscriber_index = text.find("suscriptor:")
user_index = text.find("usuario:")
consultation_date_index = text.find("fecha:")
consultation_time_index = text.find("hora:")

#inquirer variables
inquirer = {}
subscriber = text[subscriber_index + 12 : user_index -1]
user = text[user_index + 9 : consultation_date_index - 1]
consultation_date = text[consultation_date_index + 7 : consultation_time_index -1]
consultation_time = text[consultation_time_index + 6 : consultation_time_index +14]
inquirer.update({"suscriptor": subscriber, "usuario": user, "fecha consulta": consultation_date, "hora consulta":consultation_time })

#Define type of Credit Report
is_individual_credit_history_type = text.find("historia de credito de individuo") != -1
is_transunion_credit_vision_score_type = text.find("transunion credit vision score") != -1

if is_transunion_credit_vision_score_type:
  reporting_type = "Transunion Credit Vision Score"
else:
  reporting_type = "Historia De Crédito De Individuo"

#Define which Headings contains it

#transunion_creditvision_score_table
has_transunion_creditvision_score_table = False
if is_transunion_credit_vision_score_type:
  has_transunion_creditvision_score_table = True
  transunion_creditvision_score_table_index = text.find("transunion creditvision score")

#resumen_de_cuentas_abiertas_table
has_resumen_de_cuentas_abiertas_table = text.find("resumen de cuentas abiertas") != -1
resumen_de_cuentas_abiertas_table_index = text.find("resumen de cuentas abiertas")

#detalle_de_cuentas_abiertas_table
has_detalle_de_cuentas_abiertas_table = text.find("detalle de cuentas abiertas") != -1
detalle_de_cuentas_abiertas_table_index = text.find("detalle de cuentas abiertas")

#leyenda_comportamiento_historico
has_leyenda_comportamiento_historico_title = text.find("leyenda comportamiento historico") != -1
leyenda_comportamiento_historico_index = text.find("leyenda comportamiento historico")

#resumen_de_cuentas_abiertas_table
has_detalle_de_cuentas_cerradas_inactivas_table = text.find("detalle de cuentas cerradas / inactivas") != -1
detalle_de_cuentas_cerradas_inactivas_table_index = text.find("detalle de cuentas cerradas / inactivas")

#indagaciones_ultimos_6_meses_table
has_indagaciones_ultimos_6_meses_table = text.find("indagaciones ultimos 6 meses") != -1
indagaciones_ultimos_6_meses_table_index = text.find("indagaciones ultimos 6 meses")

#datos_personales_table and index
has_datos_personales_table = text.find("datos personales") != -1
datos_personales_table_index = text.find("datos personales")
identification_index = text.find("cedula")
names_index = text.find("nombres")
lastnames_index = text.find("apellidos")
birthday_index = text.find("fecha nacimiento")
age_index = text.find("edad")
ocupation_index = text.find("ocupacion")
place_of_birth_index = text.find("lugar nacimiento")
passport_index = text.find("pasaporte")
marital_status_index = text.find("estado civil")
phones_index = text.find("telefonos")
home_phone_index = text.find("casa:")
work_phone_index = text.find("trabajo:")
personal_phone_index = text.find("celular:")
addresses_index_start = text.find("direcciones")

#Define the end of the addresses line
if has_transunion_creditvision_score_table:
  addresses_index_end = transunion_creditvision_score_table_index - 1
elif has_resumen_de_cuentas_abiertas_table:
  addresses_index_end = resumen_de_cuentas_abiertas_table_index - 1
elif has_detalle_de_cuentas_cerradas_inactivas_table:
  addresses_index_end = detalle_de_cuentas_cerradas_inactivas_table_index - 1
else:
  addresses_index_end = indagaciones_ultimos_6_meses_table_index - 1
  
#personal data variables:
personal_data = {}
identification = text[identification_index + 8 : identification_index + 21]
names = text[names_index + 8 : lastnames_index - 1]
lastnames = text[lastnames_index + 10 : birthday_index - 1]
birthday = text[birthday_index + 17 : age_index - 1]
age = text[age_index + 5 : age_index + 7]
ocupation = text[ocupation_index + 10 : place_of_birth_index - 1]
place_of_birth = text[place_of_birth_index + 17 : passport_index - 1]
passport = text[passport_index + 10 : marital_status_index - 1]
marital_status = text[marital_status_index + 13 : phones_index - 1]
phones = {}
home_phone = text[home_phone_index + 6 : work_phone_index - 1]
work_phone = text[work_phone_index + 9 : personal_phone_index - 1]
personal_phone = text[personal_phone_index + 9 : addresses_index_start - 1]
phones.update({"casa": home_phone, "trabajo": work_phone, "celular": personal_phone})
addresses_raw = text[addresses_index_start + 12 : addresses_index_end]
addresses_raw = addresses_raw.split('* ')
addresses_raw.pop(0)
addresses =[]

for address in addresses_raw:
    address = address.rstrip('\n').replace('\n', ' ')
    addresses.append(address)
    
personal_data.update({"cedula": identification, "nombres": names, "apellidos": lastnames, "fecha nacimiento": birthday, "edad": age, "ocupacion": ocupation, "lugar nacimiento": place_of_birth, "pasaporte": passport, "estado civil": marital_status, "telefonos": phones, "direcciones": addresses})

#credit vision table
has_transunion_creditvision_score_table = True
transunion_creditvision_score_table_index = text.find("transunion creditvision score")


#Defautl variables
#score = "No score"
#scoring = "No score"
#summary_of_open_accounts_text = "No summary"
#summary_of_open_accounts_end = "No summary"

if has_transunion_creditvision_score_table:
  puntuacion_index = text.rfind("puntuacion")
  score = text[puntuacion_index +10 : puntuacion_index + 14] 
  factors_index = text.find("factores")  
  factors = text[factors_index + 36 : rnc_index - 1]
  factors = factors.replace('* ', '').replace(') ', ')').split('\n')



#BUILDING INDEXES AND VARIABLES
#INDEXES