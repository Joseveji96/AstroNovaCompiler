import re
from Utils import ValidarImpLeer

def head_asn(write_file):
        write_file.write("include MACROS.INC\n"
                        "pila    segment para stack 'stack'\n"
                        "        dw 500 dup(?)\n"
                        "pila    ends\n"
                        "\n"
                        "datos   segment para public 'data'\n"
                        "    empty       db      13, 10, '$'\n")
        
def body_asn(write_file):
        write_file.write("datos  ends \n"
                        "extra   segment para public 'data'\n"
                        "extra   ends\n\n"
                        "public  pp\n"
                        "assume  cs:codigo,ds:datos,es:extra,ss:pila\n\n"
                        "codigo  segment para public 'code'\n"
                        "pp      proc    far\n"
                        "   push ds\n"
                        "   mov  ax,0\n"
                        "   push ax\n"
                        "   mov  ax,datos\n"
                        "   mov  ds,ax\n"
                        "   mov  ax,extra\n"
                        "   mov  es,ax\n")
        

def makeASN(write_file, leer_file, nameAsignation, valueAsignation, impEnable, readEnable, operacionesOrden, content_count):
        for line in leer_file:
            find = False
            aux = line.strip().split()
            validar = ValidarImpLeer(line)

            if validar != "ninguna":
                for index, i in enumerate(nameAsignation):
                    if i in line and validar == "imprimir" and not impEnable[index]:
                        write_file.write(f"    esc_{i} db '  {valueAsignation[index]}$'\n")
                        impEnable[index] = True
                        operacionesOrden.append(f"IMPRIMIR esc_{i}, empty")
                        find = True
                    elif i in line and validar == "imprimir" and readEnable[index] == False:
                        operacionesOrden.append(f"IMPRIMIR esc_{i}, empty")
                        find = True
                    elif i in line and validar == "leer" and readEnable[index] == False:
                        write_file.write(f"    leer_{i} db 254,?,254 dup('$')\n")
                        readEnable[index] = True
                        operacionesOrden.append(f"LEER leer_{i}, empty")
                        impEnable[index] = True
                        find = True 
                    elif i in line and validar == "imprimir" and impEnable[index] == True and readEnable[index] == True:
                        operacionesOrden.append(f"IMPRIMIR leer_{i}, empty")
                        find = True
                    elif i in line and validar == "leer" and readEnable[index] == True:
                        operacionesOrden.append(f"LEER leer_{i}, empty")
                        find = True


                if find == False and validar == "imprimir":
                    match = re.search(r'"([^"]+)"', line)
                    if match:
                        texto_entre_comillas = match.group(1)
                        write_file.write(f"    text_{content_count} db '  {texto_entre_comillas}$'\n")
                        operacionesOrden.append(f"IMPRIMIR text_{content_count}, empty")
                        content_count += 1 
                    else:
                        print("ERROR: no se encontró ninguna cadena para ASM")

    

        for i in range(len(operacionesOrden)):
            write_file.write("    "+operacionesOrden[i] + "\n")

        write_file.write("   ret \n"
                        "pp   endp \n"
                        "codigo ends \n"
                        "   end pp \n")



