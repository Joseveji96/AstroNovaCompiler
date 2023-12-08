import  re  
from Utils import tableResults
from SintAnalizer import AnSiA as ansia
from Utils import validar_variable, validar_ciclos_condiciones, validarCiclosCondiciones, ValidarImpLeer
from ASNtoASM import head_asn, body_asn, makeASN































def compAN():
    nameAsignation = []
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

                    line = re.sub(r';.*$','', line).strip()#Borra comentarios
                    line = re.sub(r'(\".*?\")', lambda m: m.group(0).replace(" ", "<SPACE>"), line)
                    line = re.sub(r'\s+',' ', line).strip()#Borra espacios
                    line = re.sub(r'\<SPACE\>', ' ', line)

                    aux = line
                    aux = aux.split()
                    #atom numero = 1
                    if (len(aux) > 0): #Saber si no es una linea vacia
                                        
                            for indice, lexema in enumerate(aux):
                                if(lexema.isnumeric() and lexema not in nameAsignation):
                                    nameAsignation.append(lexema)
                                    typeAsignation.append("int")
                                    idAsignation.append(len(nameAsignation))
                                    valueAsignation.append(int(lexema))
                                    
                            if (aux[0] in res_asignation):
                                for indice, lexema in enumerate(aux):
                                    if(indice == 1):
                                        #Validamos que el nombre de la variable sea uno valido
                                        if (validar_variable(lexema) != True):
                                            print("LINEA "+ str(count)+ " Error el nombre de la variable de la linea: " + line + " ES INVALIDO") 
                                            break
                                        #Validamos que el nombre de la variable no sea una palabra reservada
                                        if (lexema in res_asignation or lexema in bool_values):
                                            print("LINEA "+ str(count)+ " Error el nombre de la variable de la linea: " + line + "NO SE PERMITEN PALABRAS RESERVADAS")
                                            break
                                        #Validar que no este en la tabla de declaraciones 
                                        if (lexema in nameAsignation):
                                            print("LINEA "+ str(count)+ " Error el nombre de la variable de la linea: " + line + " YA HA SIDO ASIGNADO")
                                            break
                                    


                                    elif(indice == 2):
                                        if(lexema != "="):
                                            print("LINEA "+ str(count)+ " Error de sintaxis en la linea: " + line + " SIN SIGNO DE ASIGNACION =") 
                                            break
                                    


                                    elif(indice == 3):
                                        if(aux[0] == "galaxy"):
                                            match = re.search(r'"([^"]+)"', line)
                                            if match:
                                                texto_entre_comillas = match.group(1)
                                                nameAsignation.append(aux[1]) 
                                                typeAsignation.append(aux[0])
                                                idAsignation.append(len(nameAsignation))
                                                valueAsignation.append(texto_entre_comillas)
                                            else:
                                                print("LINEA "+ str(count)+ " ERROR no se encontro ninguna cadena")
                                                break
                                        elif(aux[0] == "atom"):
                                            if(lexema.isnumeric()):
                                                nameAsignation.append(aux[1])
                                                typeAsignation.append(aux[0])
                                                idAsignation.append(len(nameAsignation))
                                                valueAsignation.append(int(lexema))
                                            else:
                                                print("LINEA "+ str(count)+ " ERROR el valor que se intenta guardar no es digito")
                                                break
                                        elif(aux[0] == "exist"):
                                            if(lexema in bool_values):
                                                nameAsignation.append(aux[1])
                                                typeAsignation.append(aux[0])
                                                idAsignation.append(len(nameAsignation))
                                                valueAsignation.append(lexema)
                                            else:
                                                print("LINEA "+ str(count)+ " ERROR el valor que se intenta guardar no es booleano")
                                                break
                                        #Solo necesitamos ver los lexemas del 0 al 3
                                        break
                                    
                            #Analiza ciclos y condiciones
                                if(validarCiclosCondiciones(line) != "ninguna"):
                                    validar_ciclos_condiciones(line, count, validarCiclosCondiciones(line))
                                else:
                                    #Analiza expresiones matematicas las evalua y guarda el resultado en su respectiva variable
                                    if ('=' in aux):
                                        indiceIgual = aux.index('=')
                                        indexVariable = -1
                                        tipoVariable = None
                                        if (indiceIgual == 1):
                                            indexVariable = nameAsignation.index(aux[0])
                                            if (indexVariable != -1):
                                                tipoVariable = typeAsignation[indexVariable]
                                            else:
                                                print("LINEA "+ str(count)+ " ERROR no podemos asignar una variable no declarada")
                                        else:
                                            tipoVariable = aux[0]
                                            indexVariable = nameAsignation.index(aux[1])

                                        if (tipoVariable == "atom") :
                                            cadenaMatematica = ''.join(aux[indiceIgual + 1:])
                                            if (not(exploradorJW.analizarExpresionMatematica(cadenaMatematica))):
                                                print("LINEA "+ str(count)+ " ERROR expresion matematica incorrecta")
                                            else:
                                                #print("Cadena Valida")
                                                resultado = eval(cadenaMatematica)
                                                valueAsignation[indexVariable] = resultado

                        
                            #Si encuentra la instruccion de imprimir o leer validara la estructura de las sentencias
                            #A partir de expresiones regulares
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

                        
                            


                            #si no es una linea vacia y no se encuentra las palabras reservadas de asignacion
                            else:
                                if (validar_variable(aux[0])):
                                    for i in range(1, len(aux)):
                                        if(i == 1):    
                                            if (aux[i] == "="):
                                                if (aux[0] in nameAsignation):
                                                    celda = nameAsignation.index(aux[0])
                                                else:
                                                    print("LINEA "+ str(count)+ " Error no se puede asignar a una variable que no ah sido declarada")
                                                    break
                                        if (i == 2): 
                                            if (validar_variable(aux[i]) and aux[i] not in bool_values and aux[i] not in res_asignation):#Si lo que hay en el 3er lexema es el nombre de una variable verificar que exista 
                                                if (aux[i] in nameAsignation):
                                                    celda2 = nameAsignation.index(aux[i])
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
                                                    if(aux[i].isdigit()):
                                                        valueAsignation[celda] = aux[i]
                                                    else:
                                                        print("LINEA "+ str(count)+ " ERROR el valor que se intenta guardar no es digito")
                                                        break
                                                elif(typeAsignation[celda] == "exist"):
                                                    if(aux[i] in bool_values):
                                                        valueAsignation[celda] = aux[i]
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
    for i in range(len(nameAsignation)):
        impEnable.append(False)
    for i in range(len(nameAsignation)):
        readEnable.append(False)
    try:
        with open(name + ".dep", "r") as leer_file, open(name + ".ASM", "w") as write_file:
            head_asn(write_file)
            content_count = 1
            makeASN(write_file, leer_file, name, nameAsignation, valueAsignation, impEnable, readEnable, operacionesOrden, content_count)
            body_asn(write_file, operacionesOrden)
    except EnvironmentError:
        print("No se encontró el archivo")
    
    #---------------------------FINALMENTE PRESENTAMOS LA TABLA DE RESULTADOS------------------------------------
    tableResults(idAsignation, nameAsignation, typeAsignation, valueAsignation, impEnable, readEnable)











































# #--------------------Intentamos leer y escribir AstroNova.asm-------------------------------
#     try:
#         with open(name + ".dep", "r") as leer_file:
#             with open(name + ".ASM", "w") as write_file:
#                 #Escribe las primeras lineas obligatorias
#                 write_file.write("include MACROS.INC\n"
#                                 "pila    segment para stack 'stack'\n"
#                                 "        dw 500 dup(?)\n"
#                                 "pila    ends\n"
#                                 "\n"
#                                 "datos   segment para public 'data'\n"
#                                 "    empty       db      13, 10, '$'\n")
#                 content_count = 1
# #   -       -   Ingresa a un arreglo la declaracion de datos (imp o leer)
#                 for line in leer_file:
#                     find = False
#                     aux = line.strip().split()
#                     validar = ValidarImpLeer(line)
#                     if validar != "ninguna":
#                         for index, i in enumerate(nameAsignation):
#                             if i in line and validar == "imprimir" and impEnable[index] == False:
#                                 write_file.write(f"    esc_{i} db '  {valueAsignation[index]}$'\n")
#                                 impEnable[index] = True
#                                 operacionesOrden.append(f"IMPRIMIR esc_{i}, empty")
#                                 find = True
#                             elif i in line and validar == "imprimir" and readEnable[index] == False:
#                                 operacionesOrden.append(f"IMPRIMIR esc_{i}, empty")
#                                 find = True
#                             elif i in line and validar == "leer" and readEnable[index] == False:
#                                 write_file.write(f"    leer_{i} db 254,?,254 dup('$')\n")
#                                 readEnable[index] = True
#                                 operacionesOrden.append(f"LEER leer_{i}, empty")
#                                 impEnable[index] = True
#                                 find = True 
#                             elif i in line and validar == "imprimir" and impEnable[index] == True and readEnable[index] == True:
#                                 operacionesOrden.append(f"IMPRIMIR leer_{i}, empty")
#                                 find = True
#                             elif i in line and validar == "leer" and readEnable[index] == True:
#                                 operacionesOrden.append(f"LEER leer_{i}, empty")
#                                 find = True

#                     if find == False and validar == "imprimir":
#                         match = re.search(r'"([^"]+)"', line)
#                         if match:
#                             texto_entre_comillas = match.group(1) #guarda el texto entre comillas para ingresar el valor al asm
#                             write_file.write(f"    text_{content_count} db '  {texto_entre_comillas}$'\n")
#                             operacionesOrden.append(f"IMPRIMIR text_{content_count}, empty")
#                             content_count+=1 
#                         else:
#                             print("ERROR no se encontro ninguna cadena para ASM")
#                 #Escribimos las lineas obligatorias del segmento de datos
#                 write_file.write(
#                     "datos   ends \n"
#                     "extra   segment para public 'data'\n"
#                     "extra   ends\n\n"
#                     "public  pp\n"
#                     "assume  cs:codigo,ds:datos,es:extra,ss:pila\n\n"
#                     "codigo  segment para public 'code'\n"
#                     "pp      proc    far\n"
#                     "    push    ds\n"
#                     "    mov     ax,0\n"
#                     "    push    ax\n"
#                     "    mov     ax,datos\n"
#                     "    mov     ds,ax\n"
#                     "    mov     ax,extra\n"
#                     "    mov     es,ax\n")
#                 #Escribimos las operaciones en el segmento de datos
#                 for i in range(len(operacionesOrden)):
#                     write_file.write("    "+operacionesOrden[i] + "\n")
#                 write_file.write(
#                     "   ret \n"
#                     "pp   endp \n"
#                     "codigo ends \n"
#                     "   end pp \n"
#                     )
#     except EnvironmentError:
#         print("No se encontró el archivo")
