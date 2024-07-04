import os
import urllib.parse
import html

# Codificaciones para caracteres especiales
especiales = ['(', ')', '<', '>', '[', ']', '{', '}', '"', "'", '/']

# Leer los payloads del archivo
def leer_payloads(archivo):
    with open('payload.txt', 'r', encoding='utf-8') as f:
        return f.readlines()

# Realizar URL Encode de todo el payload
def url_encode_completo(payload):
    return urllib.parse.quote(payload, safe='')

# Realizar HTML Encode de todo el payload
def html_encode_completo(payload):
    return html.escape(payload, quote=True)

# Generar variaciones codificadas de un payload
def generar_variaciones(payload):
    variaciones = {
        'original': payload,
        'url_encode_completo': url_encode_completo(payload),
        'html_encode_completo': html_encode_completo(payload),
        'variaciones_url': [],
        'variaciones_html': [],
    }
    
    # Para URL y HTML Encode por caracteres especiales
    for especial in especiales:
        if especial in payload:
            variado_url = payload.replace(especial, urllib.parse.quote(especial, safe=''))
            variado_html = payload.replace(especial, html.escape(especial, quote=True))
            variaciones['variaciones_url'].append(variado_url)
            variaciones['variaciones_html'].append(variado_html)
    
    return variaciones

# Procesar cada payload y escribir las variaciones en el archivo de salida
def procesar_payloads(payloads, archivo_salida):
    with open(archivo_salida, 'w', encoding='utf-8') as salida:
        for payload in payloads:
            payload = payload.strip()
            variaciones = generar_variaciones(payload)
            salida.write(f"Original: {variaciones['original']}\n")
            salida.write(f"URL Encode Completo: {variaciones['url_encode_completo']}\n")
            salida.write(f"HTML Encode Completo: {variaciones['html_encode_completo']}\n")
            for var in variaciones['variaciones_url']:
                salida.write(f"Variación URL: {var}\n")
            for var in variaciones['variaciones_html']:
                salida.write(f"Variación HTML: {var}\n")
            salida.write("\n")

# Rutas de archivos
archivo_payloads = 'payloads.txt'
archivo_salida = 'output/encoded_variants.txt'

# Crear la carpeta output si no existe
if not os.path.exists('output'):
    os.makedirs('output')

# Ejecutar el proceso
payloads = leer_payloads(archivo_payloads)
procesar_payloads(payloads, archivo_salida)

print(f"Variaciones de payloads guardadas en: {archivo_salida}")

