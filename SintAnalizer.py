
import re

class AnSiA():
    def obtener_columna(self, token):
        columna = -1
        if token == "ID":
            columna = 0
        elif token == "+":
            columna = 1
        elif token == "-":
            columna = 2
        elif token == "*":
            columna = 3
        elif token == "/":
            columna = 4
        elif token == "(":
            columna = 5
        elif token == ")":
            columna = 6
        elif token == "$":
            columna = 7
        elif token == "E":
            columna = 8
        elif token == "T":
            columna = 9
        elif token == "F":
            columna = 10
        
        return columna

    def analizarExpresionMatematica(self, cadena):
        pila = [0]
        regex = r'([A-Za-z_][A-Za-z0-9_]*|\d+|[-+*/()])'
        tokens = re.findall(regex, cadena)
        tokens.append("$")
        cadena = cadena.upper()
        number = 0

        gramatica = [
            {"E+T": "E"}, {"E-T": "E"}, {"T": "E"}, {"T*F": "T"},
            {"T/F": "T"}, {"F": "T"}, {"(E)": "F"}, {"ID": "F"},
        ]

        accion = [
            ["D5", " ", " ", " ", " ", "D4", " ", " ",  "1", "2", "3"], [" ",  "D6", "D7", " ", " ", " ",  " ", "ACCEPT", " ", " ", " "], 
            [" ",  "R3", "R3", "D8", "D9", " ", "R3", "R3", " ", " ", " "],[" ",  "R6", "R6", "R6", "R6", " ", "R6", "R6", " ", " ", " "],  
            ["D5", " ", " ", " ", " ", "D4", " ", " ", "10", "2", "3"],[" ",  "R8", "R8", "R8", "R8", " ", "R8", "R8", " ", " ", " "],  
            ["D5", " ", " ", " ", " ", "D4", " ", " ", " ", "11", "3"], ["D5", " ", " ", " ", " ", "D4", " ", " ", " ", "12", "3"],  
            ["D5", " ", " ", " ", " ", "D4", " ", " ", " ", " ", "13"], ["D5", " ", " ", " ", " ", "D4", " ", " ", " ", " ", "14"],  
            [" ",  "D6", "D7", " ", " ", " ", "D15", " ", " ", " ", " "], [" ",  "R1", "R1", "D8", "D9", " ", "R1", "R1", " ", " ", " "],  
            [" ",  "R2", "R2", "D8", "D9", " ", "R2", "R2", " ", " ", " "], [" ",  "R4", "R4", "R4", "R4", " ", "R4", "R4", " ", " ", " "],  
            [" ",  "R5", "R5", "R5", "R5", " ", "R5", "R5", " ", " ", " "], [" ",  "R7", "R7", "R7", "R7", " ", "R7", "R7", " ", " ", " "]   
        ]
        
        for i in range(len(tokens)):
            if re.match(r'^[A-Za-z_][A-Za-z0-9_]*$', tokens[i]) or tokens[i].isdigit():
                tokens[i] = "ID"


        if len(tokens) > 0:
            token_actual = tokens[number]
            number += 1 
        else:
            print("cadena vacia")

        while True and len(tokens) > 0:
            estado_actual = pila[len(pila) - 1]
            accion_actual = accion[estado_actual][self.obtener_columna(token_actual)]

            if accion_actual[0] == "D":
                pila.append(int(accion_actual[1:]))
                token_actual = tokens[number]
                number += 1 
            elif accion_actual[0] == "R":
                indice_regla = int(accion_actual[1:]) - 1
                regla = list(gramatica[indice_regla].keys())[0]
                
                if regla == "ID":
                    pila.pop()
                else:
                    for _ in range(len(regla)):
                        pila.pop()

                nuevo_estado = pila[len(pila) - 1]

                simbolo = gramatica[indice_regla].get(regla)
            
                pila.append(int(accion[nuevo_estado][self.obtener_columna(simbolo)]))

                
            elif accion_actual == "ACCEPT":
                return(True)
                break
            else:
                print("Error: expresion matematica no valida")
                return(False)
                break
