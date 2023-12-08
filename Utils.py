import re

def tableResults(id_list, name_list, type_list, value_list, imp_list, read_list):
    
    header = "| {:<5} | {:<20} | {:<6} | {:<50} | {:<9} | {:<9} |"
    separator = "-" * 98
    print(header.format("ID_", "NAME", "DTYPE", "VALUE", "WAS IMP", "WAS READ"))
    print(separator)

    # Imprimir filas de la tabla
    for i in range(len(id_list)):
        # Obtener valores de las listas
        name = str(name_list[i])
        typeV = str(type_list[i])
        value = str(value_list[i])
        id_val = str(id_list[i])
        imp = str(imp_list[i])
        read = str(read_list[i])

        # Imprimir fila de la tabla
        print("| {:<5} | {:<20} | {:<6} | {:<50} | {:<9} | {:<9} |".format(id_val, name, typeV, value, imp, read))

    print(separator)


def validar_ciclos_condiciones(line, count, type):
# Validar estructura de bucles for
    if type == "for":
        if re.match(r'^for\s+[a-zA-Z_][a-zA-Z0-9_]*\s+in\s+.+:$', line):
            print("LINEA {} OK - Estructura de bucle for válida".format(count))
        else:
            print("LINEA {} ERROR - Estructura de bucle for inválida".format(count))

    # Validar estructura de bucles while
    if type == "while":   
        if re.match(r'^while\s+.+:$', line):
            print("LINEA {} OK - Estructura de bucle while válida".format(count))
        else:
            print("LINEA {} ERROR - Estructura de bucle while inválida".format(count))

    # Validar estructura de condiciones if
    if type == "if": 
        if re.match(r'^if\s+\(.+?\)\s*:$', line):
            print("LINEA {} OK - Estructura de condición if válida".format(count))
        else:
            print("LINEA {} ERROR - Estructura de condición if inválida".format(count))


def validar_variable(variable):
    patron = r'^[a-zA-Z_][a-zA-Z0-9_]*$'
    return bool(re.match(patron, variable))

def verifyImpRead(x):
    onOut = "ninguna"
    if(x.find("leer.") != -1):
        onOut = "leer"
    elif(x.find("imprimir(") != -1 or x.find("imprimir (") != -1):
        onOut = "imprimir"
    return onOut

def validarCiclosCondiciones(ciclo):
    inout = "ninguna"
    if(ciclo.find("for(") != -1 or ciclo.find("for (") != -1 or ciclo.find("for") != -1):
        inout = "for"
    elif(ciclo.find("while(") != -1 or ciclo.find("while (") != -1 or ciclo.find("while") != -1):
        inout = "while"
    elif(ciclo.find("if(") != -1 or ciclo.find("if (") != -1 or ciclo.find("if") != -1):
        inout = "if"
    return inout

def es_float(cadena):
    try:
        float(cadena)
        return True
    except ValueError:
        return False
    
def format_ln(line):
    line = re.sub(r';.*$','', line).strip()
    line = re.sub(r'(\".*?\")', lambda m: m.group(0).replace(" ", "<SPACE>"), line)
    line = re.sub(r'\s+',' ', line).strip()
    line = re.sub(r'\<SPACE\>', ' ', line)
    return line



def validar_nombre_variable(lexema, count, line, nasign, res_asignation, bool_values):
        if not validar_variable(lexema):
            print(f"LINEA {count} Error el nombre de la variable de la linea: {line} ES INVALIDO")
            return False
        if lexema in res_asignation or lexema in bool_values:
            print(f"LINEA {count} Error el nombre de la variable de la linea: {line} NO SE PERMITEN PALABRAS RESERVADAS")
            return False
        if lexema in nasign:
            print(f"LINEA {count} Error el nombre de la variable de la linea: {line} YA HA SIDO ASIGNADO")
            return False
        return True

def manejar_asignacion_galaxy(asistente, count, line, nasign, typeAsignation, idAsignation, valueAsignation):
    match = re.search(r'"([^"]+)"', line)
    if match:
        texto_entre_comillas = match.group(1)
        nasign.append(asistente[1])
        typeAsignation.append(asistente[0])
        idAsignation.append(len(nasign))
        valueAsignation.append(texto_entre_comillas)
    else:
        print(f"LINEA {count} ERROR no se encontro ninguna cadena")

def manejar_asignacion_atom(asistente, lexema, count, line, nasign, typeAsignation, idAsignation, valueAsignation):
    if lexema.isnumeric():
        nasign.append(asistente[1])
        typeAsignation.append(asistente[0])
        idAsignation.append(len(nasign))
        valueAsignation.append(int(lexema))
    else:
        print(f"LINEA {count} ERROR el valor que se intenta guardar no es digito")

def manejar_asignacion_exist(asistente, lexema, count, line, nasign, typeAsignation, idAsignation, valueAsignation, bool_values):
    if lexema in bool_values:
        nasign.append(asistente[1])
        typeAsignation.append(asistente[0])
        idAsignation.append(len(nasign))
        valueAsignation.append(lexema)
    else:
        print(f"LINEA {count} ERROR el valor que se intenta guardar no es booleano")