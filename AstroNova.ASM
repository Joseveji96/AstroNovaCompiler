include MACROS.INC
pila    segment para stack 'stack'
        dw 500 dup(?)
pila    ends

datos   segment para public 'data'
    empty       db      13, 10, '$'
datos  ends 
extra   segment para public 'data'
extra   ends

public  pp
assume  cs:codigo,ds:datos,es:extra,ss:pila

codigo  segment para public 'code'
pp      proc    far
   push ds
   mov  ax,0
   push ax
   mov  ax,datos
   mov  ds,ax
   mov  ax,extra
   mov  es,ax
    esc_cadena db '  la variable galaxy es una cadena$'
    esc_b db '  true$'
    text_1 db '  Hola Mundo$'
    leer_cadena db 254,?,254 dup('$')
    esc_first db '  0$'
    leer_first db 254,?,254 dup('$')
    esc_third db '  25$'
    leer_third db 254,?,254 dup('$')
    IMPRIMIR esc_cadena, empty
    IMPRIMIR esc_cadena, empty
    IMPRIMIR esc_b, empty
    IMPRIMIR text_1, empty
    LEER leer_cadena, empty
    IMPRIMIR leer_cadena, empty
    IMPRIMIR esc_first, empty
    LEER leer_first, empty
    LEER leer_first, empty
    IMPRIMIR leer_first, empty
    IMPRIMIR esc_third, empty
    IMPRIMIR esc_third, empty
    LEER leer_third, empty
    IMPRIMIR leer_third, empty
   ret 
pp   endp 
codigo ends 
   end pp 
