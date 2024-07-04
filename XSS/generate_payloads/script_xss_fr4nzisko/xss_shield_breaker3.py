import os
import urllib.parse
import html

# Crear la carpeta de salida si no existe
if not os.path.exists('output'):
    os.makedirs('output')

def leer_payloads(archivo):
    with open(archivo, 'r') as file:
        return set(file.read().splitlines())

# Cargar el archivo principal
payloads_principal = leer_payloads('payload.txt')

# Comparar con otros archivos .txt para encontrar payloads únicos
for archivo in os.listdir('.'):
    if archivo.endswith('.txt') and archivo != 'payload.txt':
        payloads_principal = payloads_principal.union(leer_payloads(archivo))

# Guardar payloads únicos en un archivo
with open('output/validacion_payloads.txt', 'w') as archivo_validacion:
    for payload in payloads_principal:
        archivo_validacion.write(f"{payload}\n")
# Diccionario para mapear caracteres especiales a sus codificaciones
caracteres_codificacion = {
    '(': {'url': '%28', 'html': '&#40;', 'decimal': '&#40;', 'spicing': 'U+207D'},
    ')': {'url': '%29', 'html': '&#41;', 'decimal': '&#41;', 'spicing': 'U+207E'},
    # Agregar el resto de los caracteres aquí siguiendo el mismo patrón
}

def codificar_caracter(caracter, metodo):
    if caracter in caracteres_codificacion:
        return caracteres_codificacion[caracter][metodo]
    else:
        return caracter

def codificar_payload(payload, metodo):
    resultado = []
    for char in payload:
        resultado.append(codificar_caracter(char, metodo))
    return ''.join(resultado)

# Leer payloads únicos para codificación
with open('output/validacion_payloads.txt', 'r') as archivo:
    payloads_unicos = archivo.readlines()

# Aplicar codificaciones a cada payload
codificaciones = ['url', 'html', 'decimal', 'spicing']
with open('output/encoded.txt', 'w') as archivo_codificado:
    for payload in payloads_unicos:
        payload = payload.strip()
        for metodo in codificaciones:
            payload_codificado = codificar_payload(payload, metodo)
            archivo_codificado.write(f"{metodo} encoded: {payload_codificado}\n")
        archivo_codificado.write("\n")
