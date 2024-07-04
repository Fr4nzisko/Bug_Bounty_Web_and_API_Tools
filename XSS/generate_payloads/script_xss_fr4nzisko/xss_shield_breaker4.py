import os
import urllib.parse
import html

import os

# Codificaciones para caracteres especiales
url_codificaciones = {
    '(': '%28', ')': '%29', '<': '%3C', '>': '%3E',
    '[': '%5B', ']': '%5D', '{': '%7B', '}': '%7D',
    '"': '%22', "'": '%27', '/': '%2F',
}
html_codificaciones = {
    '(': '&#40;', ')': '&#41;', '<': '&lt;', '>': '&gt;',
    '[': '&#91;', ']': '&#93;', '{': '&#123;', '}': '&#125;',
    '"': '&quot;', "'": '&#39;', '/': '&#47;',
}
decimal_codificaciones = {
    '(': '&#40;', ')': '&#41;', '<': '&#60;', '>': '&#62;',
    '[': '&#91;', ']': '&#93;', '{': '&#123;', '}': '&#125;',
    '"': '&#34;', "'": '&#39;', '/': '&#47;',
}
spicing_modifier_letters = {
    '(': 'U+207D', ')': 'U+207E', '<': 'U+003C', '>': 'U+003E',
    '[': 'U+005B', ']': 'U+005D', '{': 'U+007B', '}': 'U+007D',
    '"': 'U+0022', "'": 'U+0027', '/': 'U+002F',
}

# Mapeo de caracteres de apertura a sus correspondientes caracteres de cierre y viceversa
parejas_caracteres = {'(': ')', '{': '}', '[': ']', '<': '>'}
parejas_caracteres_inverso = {v: k for k, v in parejas_caracteres.items()}

# Función para leer y agregar payloads de todos los archivos .txt en el directorio actual
def agregar_payloads(directorio):
    payloads_agregados = set()
    for archivo in os.listdir(directorio):
        if archivo.endswith('.txt'):
            with open(os.path.join(directorio, archivo), 'r', encoding='utf-8') as f:
                payloads_agregados.update(f.read().splitlines())
    return payloads_agregados

# Función de codificación mejorada para manejar anidamientos y pares incompletos
def codificar_payload(payload, codificaciones):
    pila = []
    resultado = list(payload)
    
    def codificar_en_posicion(pos, caracter, codificaciones):
        if caracter in codificaciones:
            resultado[pos] = codificaciones[caracter]

    for i, char in enumerate(payload):
        if char in parejas_caracteres:
            pila.append((char, i))
        elif char in parejas_caracteres_inverso and pila:
            ultimo_abierto, pos_abierto = pila[-1]
            if parejas_caracteres_inverso[char] == ultimo_abierto:
                pila.pop()
                codificar_en_posicion(pos_abierto, ultimo_abierto, codificaciones)
                codificar_en_posicion(i, char, codificaciones)
    
    # Codificar caracteres de apertura sin cierre
    while pila:
        abierto, pos_abierto = pila.pop()
        codificar_en_posicion(pos_abierto, abierto, codificaciones)

    return ''.join(resultado)

# Ejecutar todo el proceso
directorio_actual = os.getcwd()
payloads_agregados = agregar_payloads(directorio_actual)

# Preparar carpeta output
carpeta_output = os.path.join(directorio_actual, 'output')
os.makedirs(carpeta_output, exist_ok=True)

# Archivo de salida
ruta_archivo_codificados = os.path.join(carpeta_output, 'encoded.txt')
with open(ruta_archivo_codificados, 'w', encoding='utf-8') as archivo_salida:
    for payload in payloads_agregados:
        url_encoded = codificar_payload(payload, url_codificaciones)
        html_encoded = codificar_payload(payload, html_codificaciones)
        decimal_encoded = codificar_payload(payload, decimal_codificaciones)
        spicing_encoded = codificar_payload(payload, spicing_modifier_letters)
        
        # Escribir el payload original y sus versiones codificadas en el archivo
        archivo_salida.write(f"Original: {payload}\n")
        archivo_salida.write(f"URL Encoded: {url_encoded}\n")
        archivo_salida.write(f"HTML Encoded: {html_encoded}\n")
        archivo_salida.write(f"Decimal Encoded: {decimal_encoded}\n")
        archivo_salida.write(f"Spicing Modifier Letters: {spicing_encoded}\n\n")

print(f"Payloads codificados guardados en: {ruta_archivo_codificados}")
