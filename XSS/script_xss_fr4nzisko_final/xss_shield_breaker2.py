import os
import urllib.parse
import html

# Leer payloads de 'payload.txt'
def leer_payloads(archivo):
    with open(archivo, 'r') as file:
        return set(file.read().splitlines())

payloads_principal = leer_payloads('payload.txt')

# Comparar con otros archivos .txt y unificar los payloads
for archivo in os.listdir('.'):
    if archivo.endswith('.txt') and archivo != 'payload.txt':
        payloads_principal = payloads_principal.union(leer_payloads(archivo))

# Ahora tenemos un conjunto de payloads únicos en payloads_principal
with open('validacion_payloads.txt', 'w') as validacion_file:
    for payload in payloads_principal:
        validacion_file.write(f"{payload}\n")

def incremental_encode(payload, encode_function):
    encoded_payloads = []
    for i in range(len(payload)):
        if i == 0:
            encoded_payloads.append(encode_function(payload[0]) + payload[1:])
        else:
            encoded_payloads.append(encoded_payloads[-1][:i] + encode_function(payload[i]) + payload[i+1:])
    return encoded_payloads

def html_encode(char):
    return html.escape(char)

def url_encode(char):
    return urllib.parse.quote(char)

def decimal_encode(char):
    return f"&#{ord(char)};"

def spicing_modifier_letters(char):
    # Esta es una simplificación; ajusta según necesidad.
    return chr(ord(char) + 0xFEE0) if '!' <= char <= '~' else char

# Usar `incremental_encode` para cada payload y cada método de codificación
with open('encoded.txt', 'w') as encoded_file:
    for payload in payloads_principal:
        # URL Encode
        for encoded in incremental_encode(payload, url_encode):
            encoded_file.write(f"{encoded}\n")
        # HTML Encode - Repite el proceso con html_encode en lugar de url_encode
        # Decimal Encode - Repite con decimal_encode
        # Spicing Modifier Letters - Repite con spicing_modifier_letters
        encoded_file.write("\n")  # Separa los diferentes payloads
