#diccionario = {"a": 1, "b": 2, "c": 3}

#for clave, valor in diccionario.items():
#    print(f"Clave: {clave}, Valor: {valor}")

  #for i in details_open_accounts:
  #  for clave, valor in details_open_accounts[1].items():
  #    print(f"{clave}: {valor}")

list = ['tarjeta cr >> cancelada >> scotiabank', '11/2019', '01/2023', 'rd$', '1', '000  000  000  000', 'tarjeta cr >> cancelada >> scotiabank', '06/2016', '01/2023', 'rd$', '100', '000  000  000  000', 'tarjeta cr >> cancelada >> banco bhd leon', '07/2021', '08/2022', 'rd$', '9,000', '000  000  000  00-', 'tarjeta cr >> cancelada >> scotiabank', '05/2020', '08/2020', 'rd$', '0', '---  ---  ---  --0']

list2 = ['tarjeta cr >>', 'cancelada >>', 'bancamerica', '12/2011', '11/2020', 'rd$', '20,000', '---  ---  ---  --0', '12/2011', '11/2020', 'us$', '1', '---  ---  ---  --0', 'tarjeta cr >>', 'cancelada >>', 'asociacion popular', '07/2014', '01/2019', 'rd$', '0', '001  012  345  670', '07/2014', '01/2019', 'us$', '0', '000  000  000  000', 'tarjeta cr >>', 'cancelada >>', 'bancamerica', '12/2011', '12/2018', 'us$', '0', '000  000  000  000']

for i, elemento in enumerate(list2):
  if ">>" in elemento:
    print(i)