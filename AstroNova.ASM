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
    esc_b db '  AstroNova$'
    esc_a db '  5$'
    leer_a db 254,?,254 dup('$')
    leer_b db 254,?,254 dup('$')
    IMPRIMIR esc_b, empty
    IMPRIMIR esc_a, empty
    LEER leer_a, empty
    LEER leer_b, empty
   ret 
pp   endp 
codigo ends 
   end pp 
