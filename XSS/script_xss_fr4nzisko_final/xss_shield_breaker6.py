import os
import urllib.parse
import html

# Codificaciones para caracteres especiales
especiales = ['(', ')', '<', '>', '[', ']', '{', '}', '"', "'", '/']

# Funciones de codificación
def url_encode_completo(payload):
    return urllib.parse.quote(payload, safe='')

def html_encode_completo(payload):
    return html.escape(payload, quote=True)

def decimal_encode(payload):
    return ''.join(f'&#{ord(c)};' for c in payload)

def spicing_modifier_letters(payload):
    replacements = {
        '(': 'U+207D', ')': 'U+207E', '<': 'U+003C', '>': 'U+003E',
        '[': 'U+005B', ']': 'U+005D', '{': 'U+007B', '}': 'U+007D',
        '"': 'U+0022', "'": 'U+0027', '/': 'U+002F',
    }
    return ''.join(replacements.get(c, c) for c in payload)

# Leer los payloads del archivo
def leer_payloads(archivo):
    with open('payload.txt', 'r', encoding='utf-8') as f:
        return f.readlines()

# Generar variaciones codificadas de un payload, manteniendo un orden
def generar_variaciones(payload):
    variaciones = [payload]  # Iniciar con el payload original

    # Agregar codificaciones completas primero
    variaciones.append(url_encode_completo(payload))
    variaciones.append(html_encode_completo(payload))
    variaciones.append(decimal_encode(payload))
    variaciones.append(spicing_modifier_letters(payload))
    
    # Generar variaciones por caracteres especiales, evitando duplicados
    variaciones_set = set(variaciones)  # Usar un conjunto para manejar duplicados
    for especial in especiales:
        if especial in payload:
            variado_url = payload.replace(especial, urllib.parse.quote(especial, safe=''))
            variado_html = payload.replace(especial, html.escape(especial, quote=True))
            variado_decimal = payload.replace(especial, f'&#{ord(especial)};')
            variado_spicing = payload.replace(especial, spicing_modifier_letters(especial))
            variaciones_set.update([variado_url, variado_html, variado_decimal, variado_spicing])
    
    # Convertir el conjunto de nuevo a lista para mantener el orden y excluir el original al final
    variaciones_finales = list(variaciones_set)
    variaciones_finales.sort(key=lambda x: (len(x), x))  # Ordenar por longitud y luego alfabéticamente
    
    return variaciones_finales

# Procesar cada payload y escribir las variaciones en el archivo de salida
def procesar_payloads(payloads, archivo_salida):
    with open(archivo_salida, 'w', encoding='utf-8') as salida:
        for payload in payloads:
            payload = payload.strip()
            variaciones = generar_variaciones(payload)
            for var in variaciones:
                salida.write(f"{var}\n")
            salida.write("\n")

# Configuración de archivos y ejecución del proceso
archivo_payloads = 'payloads.txt'
archivo_salida = 'output/encoded_variants.txt'

# Crear la carpeta output si no existe
if not os.path.exists('output'):
    os.makedirs('output')

# Ejecutar el proceso
payloads = leer_payloads(archivo_payloads)
procesar_payloads(payloads, archivo_salida)

print(f"Variaciones de payloads guardadas en: {archivo_salida}")
