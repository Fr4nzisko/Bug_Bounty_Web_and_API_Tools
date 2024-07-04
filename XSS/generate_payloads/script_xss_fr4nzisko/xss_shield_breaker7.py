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

# Recolectar y unificar payloads de todos los archivos .txt, eliminando duplicados
def recolectar_payloads_unificados(directorio):
    payloads_unificados = set()
    for archivo in os.listdir(directorio):
        if archivo.endswith('.txt') and archivo != 'encoded_variants.txt':
            with open(os.path.join(directorio, archivo), 'r', encoding='utf-8') as f:
                payloads_unificados.update(f.read().splitlines())
    return list(payloads_unificados)

# Generar variaciones codificadas de un payload, manteniendo un orden
def generar_variaciones(payload):
    variaciones = [payload]  # Iniciar con el payload original

    # Agregar codificaciones completas
    variaciones.append(url_encode_completo(payload))
    variaciones.append(html_encode_completo(payload))
    variaciones.append(decimal_encode(payload))
    variaciones.append(spicing_modifier_letters(payload))
    
    variaciones_set = set(variaciones)  # Usar un conjunto para manejar duplicados
    for especial in especiales:
        if especial in payload:
            variaciones_set.update([
                payload.replace(especial, urllib.parse.quote(especial, safe='')),
                payload.replace(especial, html.escape(especial, quote=True)),
                payload.replace(especial, f'&#{ord(especial)};'),
                payload.replace(especial, spicing_modifier_letters(especial))
            ])
    
    return list(variaciones_set)

# Procesar cada payload unificado y escribir las variaciones en el archivo de salida
def procesar_payloads_unificados(payloads, archivo_salida):
    with open(archivo_salida, 'w', encoding='utf-8') as salida:
        for payload in payloads:
            variaciones = generar_variaciones(payload.strip())
            for var in variaciones:
                salida.write(f"{var}\n")
            salida.write("\n")

# Configuración de archivos y ejecución del proceso
directorio_actual = os.getcwd()
payloads_unificados = recolectar_payloads_unificados(directorio_actual)
archivo_salida = os.path.join('output', 'encoded_variants.txt')

# Crear la carpeta output si no existe
os.makedirs('output', exist_ok=True)

# Ejecutar el proceso
procesar_payloads_unificados(payloads_unificados, archivo_salida)

print(f"Variaciones de payloads guardadas en: {archivo_salida}")
