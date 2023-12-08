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

def ValidarImpLeer(variable):
    inout = "ninguna"
    if(variable.find("leer.") != -1):
        inout = "leer"
    elif(variable.find("imprimir(") != -1 or variable.find("imprimir (") != -1):
        inout = "imprimir"
    return inout

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