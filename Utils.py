import re

# <------------0-----------------Verificaciones---------------------0---------------->

# Función para validar si una cadena cumple con la sintaxis de un nombre de variable válido en Python
def validar_variable(x):
    patron = r'^[a-zA-Z_][a-zA-Z0-9_]*$'
    return bool(re.match(patron, x))

# Función para verificar la estructura de bucles for, while e if en una línea de código
def verifyStructs(line, count, type):
    # Validar estructura de bucles for
    if type == "for":
        if re.match(r'^for\s+[a-zA-Z_][a-zA-Z0-9_]*\s+in\s+.+:$', line):
            print("Estructura for válida".format(count))
        else:
            print("Error, la linea {} es una estructura for inválida".format(count))

    # Validar estructura de bucles while
    if type == "while":   
        if re.match(r'^while\s+.+:$', line):
            print("Estructura while válida".format(count))
        else:
            print("Error, la linea {} es una estructura while inválida".format(count))

    # Validar estructura de condiciones if
    if type == "if": 
        if re.match(r'^if\s+\(.+?\)\s*:$', line):
            print("Estructura if válida".format(count))
        else:
            print("Error, la linea {} es una estructura if inválida".format(count))

# Función para verificar si una línea de código contiene "leer" o "imprimir"
def verifyImpRead(x):
    onOut = "ninguna"
    if(x.find("leer.") != -1):
        onOut = "leer"
    elif(x.find("imprimir(") != -1 or x.find("imprimir (") != -1):
        onOut = "imprimir"
    return onOut

# Función para verificar si una línea de código contiene "for", "while" o "if"
def verifyCicles(are):
    onOut = "ninguna"
    if(are.find("for(") != -1 or are.find("for (") != -1 or are.find("for") != -1):
        onOut = "for"
    elif(are.find("while(") != -1 or are.find("while (") != -1 or are.find("while") != -1):
        onOut = "while"
    elif(are.find("if(") != -1 or are.find("if (") != -1 or are.find("if") != -1):
        onOut = "if"
    return onOut

# Función para verificar el nombre de una variable en una línea de código
def verifyNomb(lexema, line, nasign, res_asignation, bool_values):
    if not validar_variable(lexema):
        print(f"Error, el nombre de la variable de la linea: {line} es invalido")
        return False
    if lexema in res_asignation or lexema in bool_values:
        print(f"Error, el nombre de la variable de la linea:  {line} es palabra reservada")
        return False
    if lexema in nasign:
        print(f"Error, el nombre de la variable de la linea:  {line} ya esta asignada")
        return False
    return True

# Función para verificar si una cadena puede convertirse en un número de punto flotante
def es_float(cadena):
    try:
        float(cadena)
        return True
    except ValueError:
        return False

# Función para dar formato a una línea de código eliminando comentarios y espacios innecesarios
def format_ln(line):
    line = re.sub(r';.*$','', line).strip()
    line = re.sub(r'(\".*?\")', lambda m: m.group(0).replace(" ", "<SPACE>"), line)
    line = re.sub(r'\s+',' ', line).strip()
    line = re.sub(r'\<SPACE\>', ' ', line)
    return line

# <------------0-----------------Asignaciones y declaraciones---------------------0---------------->

# Funciones para manejar distintos tipos de asignaciones
def manejar_asignacion_galaxy(asistente, count, line, nasign, typeAsignation, idAsignation, valueAsignation):
    match = re.search(r'"([^"]+)"', line)
    if match:
        texto_entre_comillas = match.group(1)
        nasign.append(asistente[1])
        typeAsignation.append(asistente[0])
        idAsignation.append(len(nasign))
        valueAsignation.append(texto_entre_comillas)
    else:
        print(f"Error, la linea {count} no se ha encontrado ninguna cadena")

# Función para manejar la asignación de valores numéricos
def manejar_asignacion_atom(asistente, lexema, count, line, nasign, typeAsignation, idAsignation, valueAsignation):
    if lexema.isnumeric():
        nasign.append(asistente[1])
        typeAsignation.append(asistente[0])
        idAsignation.append(len(nasign))
        valueAsignation.append(int(lexema))
    else:
        print(f"Error, la linea {count} ERROR el valor que se intenta guardar no es digito")

# Función para manejar la asignación de valores booleanos
def manejar_asignacion_exist(asistente, lexema, count, line, nasign, typeAsignation, idAsignation, valueAsignation, bool_values):
    if lexema in bool_values:
        nasign.append(asistente[1])
        typeAsignation.append(asistente[0])
        idAsignation.append(len(nasign))
        valueAsignation.append(lexema)
    else:
        print(f"Error, la linea {count}, el tipo de dato no es exist")

# Funciones para manejar distintos tipos de asignaciones generales
def handle_galaxy(asistente, nasign, typeAsignation, valueAsignation, count, line):
    match = re.search(r'"([^"]+)"', line)
    if match:
        texto_entre_comillas = match.group(1)
        nasign.append(asistente[1])
        typeAsignation.append(asistente[0])
        valueAsignation.append(texto_entre_comillas)
    else:
        print(f"Error, la linea {count}, no se encontró ninguna galaxy")

def handle_atom(asistente, nasign, typeAsignation, valueAsignation, count):
    if asistente[2].isdigit():
        nasign.append(asistente[1])
        typeAsignation.append(asistente[0])
        valueAsignation.append(int(asistente[2]))
    else:
        print(f"Error, la linea {count}, el tipo de dato no es atom")

def handle_exist(asistente, nasign, typeAsignation, valueAsignation, bool_values, count):
    if asistente[2] in bool_values:
        nasign.append(asistente[1])
        typeAsignation.append(asistente[0])
        valueAsignation.append(asistente[2])
    else:
        print(f"Error, la linea {count}, el tipo de dato no es booleano")

# Función para manejar asignaciones generales
def handle_general(asistente, nasign, typeAsignation, valueAsignation, bool_values, count, line):
    if asistente[0] == "galaxy":
        handle_galaxy(asistente, nasign, typeAsignation, valueAsignation, count, line)
    elif asistente[0] == "atom":
        handle_atom(asistente, nasign, typeAsignation, valueAsignation, count)
    elif asistente[0] == "exist":
        handle_exist(asistente, nasign, typeAsignation, valueAsignation, bool_values, count)
    else:
        print(f"ERROR en la línea: {count} tipo de asignación no reconocido")

# <------------0-----------------TablaDeResultados---------------------0---------------->

# Función para imprimir una tabla de resultados
def tableResults(id_list, name_list, type_list, value_list, imp_list, read_list):
    header = "| {:^114} |".format("AstroNova")
    separator = "-" * 118
    print(header)
    print(separator)

    header = "| {:<5} | {:<20} | {:<6} | {:<50} | {:<9} | {:<9} |"
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
