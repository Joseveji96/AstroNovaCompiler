#Codigo desarrollado por Jose Eduardo Velazco Jimenez
#NC-20291027
import  re  
from Utils import tableResults
from SintAnalizer import AnSiA as ansia
from Utils import verifyStructs, verifyCicles,  verifyImpRead, format_ln, verifyNomb
from ASNtoASM import head_asn, body_asn, makeASN
from Utils import manejar_asignacion_atom, manejar_asignacion_exist, manejar_asignacion_galaxy
from Utils import handle_general

def compAN():
    nasign = []     # Lista para almacenar nombres de variables
    tasign = []     # Lista para almacenar tipos de variables
    vasign = []     # Lista para almacenar valores de variables
    idasign = []    # Lista para almacenar identificadores de variables
    okRead = []     # Lista para almacenar variables marcadas como leídas
    areImp = []     # Lista para almacenar variables marcadas como listas para impresión

    varResAN = ["atom", "galaxy", "exist"]
    onExist = ["true","false"]

    exploradorJW = ansia()
    count = 0

    name = "AstroNova"
    name_txt = name + ".asn"
    
    try:
        with open(name_txt, "r") as leer_file:
            with open(name+".dep", "w") as write_file:
                for line in leer_file:
                    count += 1
                    # Formatear la línea para eliminar comentarios y espacios innecesarios
                    line = format_ln(line)
                    asistente = line.split()

                    if (len(asistente) > 0):          
                            for indice, lexema in enumerate(asistente):
                                if(lexema.isnumeric() and lexema not in nasign):
                                    nasign.append(lexema)
                                    tasign.append("int")
                                    idasign.append(len(nasign))
                                    vasign.append(int(lexema))
                                    
                            if (asistente[0] in varResAN):
                                for indice, lexema in enumerate(asistente):
                                    if indice == 1:
                                        # Verificar validez del nombre de la variable
                                        if not verifyNomb(lexema, line, nasign, varResAN, onExist):
                                            break
                                    elif indice == 2:
                                        # Verificar si se encuentra el operador de asignación (=)
                                        if lexema != "=":
                                            print(f"Error de sintaxis en la linea: {line} se esperaba =")
                                            break
                                    elif indice == 3:
                                         # Manejar la asignación según el tipo de variable
                                        if asistente[0] == "galaxy":
                                            manejar_asignacion_galaxy(asistente, count, line, nasign, tasign, idasign, vasign)
                                        elif asistente[0] == "atom":
                                            manejar_asignacion_atom(asistente, lexema, count, line, nasign, tasign, idasign, vasign)
                                        elif asistente[0] == "exist":
                                            manejar_asignacion_exist(asistente, lexema, count, line, nasign, tasign, idasign, vasign, onExist)
                                        break
                                # Verificar y manejar estructuras de control y cíclos
                                if(verifyCicles(line) != "ninguna"):
                                    verifyStructs(line, count, verifyCicles(line))
                                else:
                                    if ('=' in asistente):
                                        eq = asistente.index('=')
                                        ivar = -1
                                        tipoVariable = None
                                        # Identificar el tipo de variable y su índice en las listas
                                        if (eq == 1):
                                            ivar = nasign.index(asistente[0])
                                            if (ivar != -1):
                                                tipoVariable = tasign[ivar]
                                            else:
                                                print("Error en la linea "+ str(count)+ " no es posible asignar a variables declaradas")
                                        else:
                                            tipoVariable = asistente[0]
                                            ivar = nasign.index(asistente[1])
                                        # Evaluar y asignar el resultado de expresiones matemáticas para variables 'atom'
                                        if (tipoVariable == "atom") :
                                            cadenaMatematica = ''.join(asistente[eq + 1:])
                                            if (not(exploradorJW.analizarExpresionMatematica(cadenaMatematica))):
                                                print("Error en la linea "+ str(count)+ " expresion matematica incorrecta")
                                            else:
                                                resultado = eval(cadenaMatematica)
                                                vasign[ivar] = resultado
                            elif(verifyImpRead(line) != "ninguna"):
                                if (verifyImpRead(line) == "imprimir"):
                                    if(line.find("imprimir") == 0):
                                        
                                        patron = r'^imprimir\((?:[a-zA-Z_][a-zA-Z0-9_]*|\"[^\"]*\"|(?:\"[^\"]*\"|[a-zA-Z_][a-zA-Z0-9_]*)\s*\+\s*(?:\"[^\"]*\"|[a-zA-Z_][a-zA-Z0-9_]*))(?:\s*\+\s*(?:\"[^\"]*\"|[a-zA-Z_][a-zA-Z0-9_]*))*\)$'
                                        if re.match(patron, line) == None:
                                            print("Error en la linea "+ str(count)+ " La impresión es inválida.")
                                    else:
                                        print("Error en la linea "+ str(count)+ " en instruccion imprimir")
                                elif verifyImpRead(line) == "leer":
                                    indexLeer = line.find("leer.")
                                    auxLeer = line[indexLeer:]

                                    patron = r'^leer\.(Num|Cad|Bool)\([a-zA-Z_][a-zA-Z0-9_]*\)$'
                                    if re.match(patron, auxLeer) is None:
                                        print("Error en la linea: " + str(count) + " La instrucción de lectura es inválida.")
                            else:
                                # Manejar asignaciones generales
                                handle_general(asistente, nasign, tasign, vasign, onExist, count, line)
                    # Escribir la línea formateada en el archivo de salida
                    if line != '':
                        line = line + '\n'
                    write_file.write(line)
    except EnvironmentError:
        print("No se encontro el archivo")
    count = 0




# Se traduce el codigo a ensamblador.
    operacionesOrden = []
    for i in range(len(nasign)):
        areImp.append(False)
    for i in range(len(nasign)):
        okRead.append(False)
    try:
        #apertura del AstroNova.dep para pasarlo a ASN
        with open(name + ".dep", "r") as leer_file, open(name + ".ASM", "w") as write_file:
            head_asn(write_file)
            content_count = 1
            body_asn(write_file)
            makeASN(write_file, leer_file, nasign, vasign, areImp, okRead, operacionesOrden, content_count)
    except EnvironmentError:
        print("No se encontró el archivo")
    
    #---------------------------FINALMENTE PRESENTAMOS LA TABLA DE RESULTADOS------------------------------------
    tableResults(idasign, nasign, tasign, vasign, areImp, okRead)

    
