import  re  
from Utils import tableResults
from SintAnalizer import AnSiA as ansia
from Utils import validar_variable, validar_ciclos_condiciones, validarCiclosCondiciones, ValidarImpLeer, format_ln
from ASNtoASM import head_asn, body_asn, makeASN


def compAN():
    nasign = []
    typeAsignation = []
    valueAsignation = []
    idAsignation = []
    impEnable = []
    readEnable = []

    res_asignation = ["atom", "galaxy", "exist"]
    bool_values = ["true","false"]

    exploradorJW = ansia()
    count = 0

    #Sintaxis del archivo
    name = "AstroNova"
    name_txt = name + ".asn"
    try:
        with open(name_txt, "r") as leer_file:
            with open(name+".dep", "w") as write_file:
                for line in leer_file:
                    count += 1
                    line = format_ln(line)
                    asistente = line.split()

                    if (len(asistente) > 0):          
                            for indice, lexema in enumerate(asistente):
                                if(lexema.isnumeric() and lexema not in nasign):
                                    nasign.append(lexema)
                                    typeAsignation.append("int")
                                    idAsignation.append(len(nasign))
                                    valueAsignation.append(int(lexema))
                                    
                            if (asistente[0] in res_asignation):
                                for indice, lexema in enumerate(asistente):
                                    if(indice == 1):
                                        if (validar_variable(lexema) != True):
                                            print("LINEA "+ str(count)+ " Error el nombre de la variable de la linea: " + line + " ES INVALIDO") 
                                            break
                                        if (lexema in res_asignation or lexema in bool_values):
                                            print("LINEA "+ str(count)+ " Error el nombre de la variable de la linea: " + line + "NO SE PERMITEN PALABRAS RESERVADAS")
                                            break
                                        if (lexema in nasign):
                                            print("LINEA "+ str(count)+ " Error el nombre de la variable de la linea: " + line + " YA HA SIDO ASIGNADO")
                                            break
                                    elif(indice == 2):
                                        if(lexema != "="):
                                            print("LINEA "+ str(count)+ " Error de sintaxis en la linea: " + line + " SIN SIGNO DE ASIGNACION =") 
                                            break
                                    elif(indice == 3):
                                        if(asistente[0] == "galaxy"):
                                            match = re.search(r'"([^"]+)"', line)
                                            if match:
                                                texto_entre_comillas = match.group(1)
                                                nasign.append(asistente[1]) 
                                                typeAsignation.append(asistente[0])
                                                idAsignation.append(len(nasign))
                                                valueAsignation.append(texto_entre_comillas)
                                            else:
                                                print("LINEA "+ str(count)+ " ERROR no se encontro ninguna cadena")
                                                break
                                        elif(asistente[0] == "atom"):
                                            if(lexema.isnumeric()):
                                                nasign.append(asistente[1])
                                                typeAsignation.append(asistente[0])
                                                idAsignation.append(len(nasign))
                                                valueAsignation.append(int(lexema))
                                            else:
                                                print("LINEA "+ str(count)+ " ERROR el valor que se intenta guardar no es digito")
                                                break
                                        elif(asistente[0] == "exist"):
                                            if(lexema in bool_values):
                                                nasign.append(asistente[1])
                                                typeAsignation.append(asistente[0])
                                                idAsignation.append(len(nasign))
                                                valueAsignation.append(lexema)
                                            else:
                                                print("LINEA "+ str(count)+ " ERROR el valor que se intenta guardar no es booleano")
                                                break
                                        break
                                if(validarCiclosCondiciones(line) != "ninguna"):
                                    validar_ciclos_condiciones(line, count, validarCiclosCondiciones(line))
                                else:
                                    if ('=' in asistente):
                                        indiceIgual = asistente.index('=')
                                        indexVariable = -1
                                        tipoVariable = None
                                        if (indiceIgual == 1):
                                            indexVariable = nasign.index(asistente[0])
                                            if (indexVariable != -1):
                                                tipoVariable = typeAsignation[indexVariable]
                                            else:
                                                print("LINEA "+ str(count)+ " ERROR no podemos asignar una variable no declarada")
                                        else:
                                            tipoVariable = asistente[0]
                                            indexVariable = nasign.index(asistente[1])

                                        if (tipoVariable == "atom") :
                                            cadenaMatematica = ''.join(asistente[indiceIgual + 1:])
                                            if (not(exploradorJW.analizarExpresionMatematica(cadenaMatematica))):
                                                print("LINEA "+ str(count)+ " ERROR expresion matematica incorrecta")
                                            else:
                                                resultado = eval(cadenaMatematica)
                                                valueAsignation[indexVariable] = resultado
                            elif(ValidarImpLeer(line) != "ninguna"):
                                if (ValidarImpLeer(line) == "imprimir"):
                                    if(line.find("imprimir") == 0):
                                        
                                        patron = r'^imprimir\((?:[a-zA-Z_][a-zA-Z0-9_]*|\"[^\"]*\"|(?:\"[^\"]*\"|[a-zA-Z_][a-zA-Z0-9_]*)\s*\+\s*(?:\"[^\"]*\"|[a-zA-Z_][a-zA-Z0-9_]*))(?:\s*\+\s*(?:\"[^\"]*\"|[a-zA-Z_][a-zA-Z0-9_]*))*\)$'
                                        if re.match(patron, line) == None:
                                            print("LINEA "+ str(count)+ " ERROR La instrucción de impresión es inválida.")
                                    else:
                                        print("LINEA "+ str(count)+ " ERROR de sintaxis imprimir siempre debe ir al inicio de la linea")
                                elif ValidarImpLeer(line) == "leer":
                                    indexLeer = line.find("leer.")
                                    auxLeer = line[indexLeer:]

                                    patron = r'^leer\.(Num|Cad|Bool)\([a-zA-Z_][a-zA-Z0-9_]*\)$'
                                    if re.match(patron, auxLeer) is None:
                                        print("LINEA " + str(count) + " ERROR La instrucción de lectura es inválida.")

                            else:
                                if (validar_variable(asistente[0])):
                                    for i in range(1, len(asistente)):
                                        if(i == 1):    
                                            if (asistente[i] == "="):
                                                if (asistente[0] in nasign):
                                                    celda = nasign.index(asistente[0])
                                                else:
                                                    print("LINEA "+ str(count)+ " Error no se puede asignar a una variable que no ah sido declarada")
                                                    break
                                        if (i == 2): 
                                            if (validar_variable(asistente[i]) and asistente[i] not in bool_values and asistente[i] not in res_asignation):#Si lo que hay en el 3er lexema es el nombre de una variable verificar que exista 
                                                if (asistente[i] in nasign):
                                                    celda2 = nasign.index(asistente[i])
                                                    if (typeAsignation[celda] == typeAsignation[celda2]): 
                                                        valueAsignation[celda] = valueAsignation[celda2]
                                                        break 
                                                    else:
                                                        print("LINEA "+ str(count)+ " Error no se puede asignar una variable de diferente tipo")
                                                        break
                                                else:
                                                    print("LINEA "+ str(count)+ " Error no se puede asignar a una variable otra variable que no ah sido declarada")
                                                    break
                                            else: 
                                                if(typeAsignation[celda] == "galaxy"):
                                                    match = re.search(r'"([^"]+)"', line)
                                                    if match:
                                                        texto_entre_comillas = match.group(1)
                                                        valueAsignation[celda] = texto_entre_comillas
                                                    else:
                                                        print("LINEA "+ str(count)+ " ERROR no se encontro ninguna cadena")
                                                        break
                                                elif(typeAsignation[celda] == "atom"):
                                                    if(asistente[i].isdigit()):
                                                        valueAsignation[celda] = asistente[i]
                                                    else:
                                                        print("LINEA "+ str(count)+ " ERROR el valor que se intenta guardar no es digito")
                                                        break
                                                elif(typeAsignation[celda] == "exist"):
                                                    if(asistente[i] in bool_values):
                                                        valueAsignation[celda] = asistente[i]
                                                    else:
                                                        print("ERROR en la linea: "+ str(count)+ " el tipo de dato no es Exist")
                                                        break
                                                break 
                                else:
                                    print("ERROR en la linea: "+ str(count)+ " variable invalida para operaciones")
                    if line != '':
                        line = line + '\n'
                    write_file.write(line)
    except EnvironmentError:
        print("No se encontro el archivo")
    count = 0






# Se traduce el codigo a ensamblador.
    operacionesOrden = []
    for i in range(len(nasign)):
        impEnable.append(False)
    for i in range(len(nasign)):
        readEnable.append(False)
    try:
        with open(name + ".dep", "r") as leer_file, open(name + ".ASM", "w") as write_file:
            head_asn(write_file)
            content_count = 1
            makeASN(write_file, leer_file, name, nasign, valueAsignation, impEnable, readEnable, operacionesOrden, content_count)
            body_asn(write_file, operacionesOrden)
    except EnvironmentError:
        print("No se encontró el archivo")
    
    #---------------------------FINALMENTE PRESENTAMOS LA TABLA DE RESULTADOS------------------------------------
    tableResults(idAsignation, nasign, typeAsignation, valueAsignation, impEnable, readEnable)