import os
import urllib.parse
import html

# Definir funciones de codificación
def html_encode(s):
    return html.escape(s)

def url_encode(s):
    return urllib.parse.quote(s)

def decimal_encode(s):
    return ''.join(f'&#{"ord(char)"};' for char in s)

def spicing_modifier_letters(s):
    # Esta es una simplificación, debes ajustar según la lógica específica de codificación que desees.
    return ''.join(chr(ord(char) + 0xFEE0) if '!' <= char <= '~' else char for char in s)

# Leer payloads de payload.txt
with open('payload.txt', 'r') as file:
    original_payloads = file.read().splitlines()

# Comparar con otros archivos y obtener payloads únicos
unique_payloads = set(original_payloads)

for filename in os.listdir('.'):
    if filename.endswith('.txt') and filename != 'payload.txt':
        with open(filename, 'r') as file:
            file_payloads = set(file.read().splitlines())
            unique_payloads = unique_payloads.union(file_payloads)

# Escribir payloads únicos en validación_payloads.txt
with open('validación_payloads.txt', 'w') as file:
    for payload in unique_payloads:
        file.write(f"{payload}\n")

# Realizar codificaciones y escribir en payloads_encoded.txt
with open('payloads_encoded.txt', 'w') as file:
    for payload in unique_payloads:
        file.write(f"{payload}\n")
        file.write(f"{url_encode(payload)}\n")
        file.write(f"{html_encode(payload)}\n")
        file.write(f"{decimal_encode(payload)}\n")
        file.write(f"{spicing_modifier_letters(payload)}\n")
        file.write("\n")  # Separador entre payloads

print("Proceso completado.")
