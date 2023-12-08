import re
from Utils import ValidarImpLeer

def head_asn(write_file):
    # Escribe las primeras líneas del archivo de salida
        write_file.write("include MACROS.INC\n"
                        "pila    segment para stack 'stack'\n"
                        "        dw 500 dup(?)\n"
                        "pila    ends\n"
                        "\n"
                        "datos   segment para public 'data'\n"
                        "    empty       db      13, 10, '$'\n")
        
def body_asn(write_file):
    # Escribe las líneas del segmento de datos y código
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
        

def makeASN(wf, lf, asign, valueAsignation, imp, read, alineacion, cc):
    # Recorremos cada línea en el archivo de entrada
    for line in lf:
        detect  = False  # Variable para rastrear si se encontró una operación válida en la línea
        comp  = ValidarImpLeer(line)  # Determinamos si la línea es de imprimir o leer

        if comp  == "imprimir":
            # Buscamos variables para imprimir en la línea
            for index, i in enumerate(asign):
                if i in line and not imp[index]:
                    wf.write(f"    esc_{i} db '  {valueAsignation[index]}$'\n")
                    imp[index] = True
                    alineacion.append(f"IMPRIMIR esc_{i}, empty")
                    detect  = True
                elif i in line and imp[index] and read[index]:
                    # Si ya se imprimió o leyó esta variable, la añadimos nuevamente para mantener consistencia
                    alineacion.append(f"IMPRIMIR leer_{i}, empty")
                    detect  = True

            # Si no se encontraron variables para imprimir, revisamos si hay una cadena directa
            if not detect :
                match = re.search(r'"([^"]+)"', line)
                if match:
                    texto_entre_comillas = match.group(1)
                    wf.write(f"    text_{cc} db '  {texto_entre_comillas}$'\n")
                    alineacion.append(f"IMPRIMIR text_{cc}, empty")
                    cc += 1
                else:
                    print("ERROR: no se encontró ninguna cadena para ASM")

        elif comp  == "leer":
            # Buscamos variables para leer en la línea
            for index, i in enumerate(asign):
                if i in line and not read[index]:
                    wf.write(f"    leer_{i} db 254,?,254 dup('$')\n")
                    read[index] = True
                    alineacion.append(f"LEER leer_{i}, empty")
                    imp[index] = True
                    detect  = True

            # Si no se encontraron variables para leer, revisamos si ya se leyó e imprimió la variable
            if not detect  and imp[index] and read[index]:
                alineacion.append(f"LEER leer_{i}, empty")
                detect  = True

    # Escribimos las operaciones generadas en el archivo de salida
    for i in range(len(alineacion)):
        wf.write("    " + alineacion[i] + "\n")

    # Escribimos el bloque final del archivo ASM
    wf.write("   ret \n"
             "pp   endp \n"
             "codigo ends \n"
             "   end pp \n")



