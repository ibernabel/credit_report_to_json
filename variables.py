from reporting import aury, fresa, perla, enrique, estarlin, irisaudy, mildred, yeliset, joseph

text = aury
#text = fresa
#text = perla
#text = enrique
#text = estarlin
#text = irisaudy
#text = mildred
#text = yeliset
#text = joseph


#BUILDING INDEXES AND VARIABLES
#INDEXES
# :
#inquirer data indexes
subscriber_index = text.find("suscriptor:")
user_index = text.find("usuario:")
consultation_date_index = text.find("fecha:")
consultation_time_index = text.find("hora:")

#personal data indexes
personal_data_section_title_index = text.find("datos personales")
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

#general data indexes
legend_historical_behavior_index = text.find("leyenda comportamiento historico")
inquiries_last_6_months_index = text.find("indagaciones ultimos 6 meses") 
rnc_index = text.find("rnc")

#Defautl variables
score = "No score"
scoring = "No score"
summary_of_open_accounts_text = "No summary"
summary_of_open_accounts_end = "No summary"

#Checking the type of reporting
is_credit_score_report_type = text.find("transunion credit vision score") != -1

#Checking if titles of tables exits
is_summary_of_open_accounts = text.find("resumen de cuentas abiertas") != -1
is_legend_historical_behavior = text.find("leyenda comportamiento historico") != -1

if is_summary_of_open_accounts:
	summary_of_open_accounts_table_title_index = text.find("resumen de cuentas abiertas")
	details_of_open_accounts_table_title_index = text.find("detalle de cuentas abiertas")


if is_credit_score_report_type:
	credit_score_report_type_index = text.find("transunion credit vision score") 
	credit_vision_table_title_index = text.find("transunion creditvision score")
	puntuacion_index = text.rfind("puntuacion")
	addresses_index_end = credit_vision_table_title_index -2
	factors_index = text.find("factores")
	factors = text[factors_index + 36 : rnc_index - 1]
	factors = factors.replace('* ', '').replace(') ', ')').split('\n')
else: 
	credit_score_report_type_index = text.find("historia de credito de individuo")


if not is_credit_score_report_type and is_summary_of_open_accounts:
	addresses_index_end = summary_of_open_accounts_table_title_index -2
	summary_of_open_accounts_text = text[summary_of_open_accounts_table_title_index + 28 : legend_historical_behavior_index - 1]
	summary_of_open_accounts_end = text[legend_historical_behavior_index : legend_historical_behavior_index + 32]


elif not is_credit_score_report_type and not is_summary_of_open_accounts:
	addresses_index_end = inquiries_last_6_months_index -2


if is_credit_score_report_type and is_summary_of_open_accounts:
	scoring = text[puntuacion_index + 11 : summary_of_open_accounts_table_title_index -1]
	summary_of_open_accounts_text = text[summary_of_open_accounts_table_title_index + 28 : details_of_open_accounts_table_title_index - 1]
	summary_of_open_accounts_end = text[details_of_open_accounts_table_title_index : details_of_open_accounts_table_title_index + 27]
	
elif is_credit_score_report_type and not is_summary_of_open_accounts: 
	scoring = text[puntuacion_index + 11 : inquiries_last_6_months_index -1]


#VARIABLES:
#General variables

#inquirer variables
inquirer = {}
credit_score_report_type = text[credit_score_report_type_index : personal_data_section_title_index - 1]
subscriber = text[subscriber_index + 12 : user_index -1]
user = text[user_index + 9 : consultation_date_index - 1]
consultation_date = text[consultation_date_index + 7 : consultation_time_index -1]
consultation_time = text[consultation_time_index + 6 : credit_score_report_type_index -1]
inquirer.update({"tipo de consulta": credit_score_report_type, "suscriptor": subscriber, "usuario": user, "fecha consulta": consultation_date, "hora consulta":consultation_time })

#personal data variables:
personal_data = {}
identification = text[identification_index + 8 : identification_index + 21]
names = text[names_index + 8 : lastnames_index - 1]
lastnames = text[lastnames_index + 10 : birthday_index - 1]
birthday = text[birthday_index + 17 : age_index -1]
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

if is_credit_score_report_type:
	score = {}
	score.update({"scoring": scoring, "factors": factors})
	#print(score)

#building summary open accounts table
summary_open_accounts = [] # Table. A list of dicctionaries that represent a each row of data in the original table
summary_of_open_accounts_list = summary_of_open_accounts_text.split('\n')
first_subscriber_row_start_index = 17 #Index where the headers of de table ends
last_subscriber_row_end_index = summary_of_open_accounts_list.index("total general >>")
suscriber_rows_count = ( last_subscriber_row_end_index - first_subscriber_row_start_index ) / 11 # Eache group of data in a row has 11 '\n'

summary_open_accounts_headers =  ["subscriber", "accounts_amount", "account_type", "credit_amount_dop", "credit_amount_usd", "current_balance_dop", "current_balance_usd","current_overdue_dop", "current_overdue_usd","utilization_percent_dop", "utilization_percent_usd"]

def create_summary_open_accounts_table():

	for i in range(first_subscriber_row_start_index, last_subscriber_row_end_index, 11 ):
		summary_open_accounts_rows = {}	

		for j in range(i, i + 11, 1):
			summary_open_accounts_rows.update({summary_open_accounts_headers[j - i] : summary_of_open_accounts_list[j]})
		
		summary_open_accounts.append(summary_open_accounts_rows)

create_summary_open_accounts_table()

print(len(summary_open_accounts))
print(f'summary_open_accounts = {summary_open_accounts}')

#print(summary_open_accounts[0]["subscriber"])
#print(summary_open_accounts[1]["subscriber"])
#print(summary_open_accounts[2]["subscriber"])
#print(summary_open_accounts[3]["subscriber"])

#{"subscriber": "", "accounts_amount": "", "account_type": "", "credit_amount_dop": "", "credit_amount_usd": "", "current_balance_dop": "", "current_balance_usd": "","current_overdue_dop": "", "current_overdue_usd": "","utilization_percent_dop": "", "utilization_percent_usd": ""}

#subscriber
#accounts_amount
#account_type
#credit_amount_dop
#credit_amount_usd
#current_balance_dop
#current_balance_usd
#current_overdue_dop
#current_overdue_usd
#utilization_percent_dop
#utilization_percent_usd

#deploy:
#print(names)
#print(summary_of_open_accounts_end)
#print(inquirer)
#print(personal_data)

#print(personal_data["direcciones"][0].title())
#print(summary_of_open_accounts_list[60])
#print(summary_of_open_accounts_list.index("banreservas"))

#print(first_subscriber_row_start_index)
#print(last_subscriber_row_end_index)
#print(suscriber_rows_count)

#print(len(summary_of_open_accounts_list))

#print(text.count("puntuacion"))

#for index, address in enumerate(addresses):
    #print(f'{index + 1}: {address.title()}')

#table = [
#    {"name": "John", "age": 30, "city": "New York"},
#    {"name": "Jane", "age": 25, "city": "Los Angeles"},
#    {"name": "Bob", "age": 40, "city": "San Francisco"}
#]