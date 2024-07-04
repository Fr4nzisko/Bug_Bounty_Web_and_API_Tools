import os 
import re
from urllib.parse import quote


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

# Función para generar variaciones de 'alert' con diferentes variables
def generar_variaciones_alert(texto, combinaciones):
    # Buscar todas las ocurrencias de 'alert'
    ocurrencias = [(m.start(0), m.end(0)) for m in re.finditer('alert', texto)]
    nuevo_texto = texto
    desplazamiento = 0
    
    for inicio, fin in ocurrencias:
        for combinacion in combinaciones:
            # Construir la variación de 'alert' con la combinación actual
            variacion = "+".join([quote(part) for part in combinacion])
            # Insertar la variación en el texto
            nuevo_texto = nuevo_texto[:inicio+desplazamiento] + variacion + nuevo_texto[fin+desplazamiento:]
            desplazamiento += len(variacion) - (fin - inicio)  # Ajustar el desplazamiento para la siguiente inserción
    
    return nuevo_texto

# Generar combinaciones de las partes de 'alert' con URLEncode
# Aquí, simplemente usamos algunas combinaciones de ejemplo. Deberías expandir esto según tus necesidades.
combinaciones = [
    ('%61%6C', 'e', '%72%74'),  # URLEncode para 'al', 'e', 'rt'
    ('a', 'l', 'e', 'r', 't'),  # Sin URLEncode, como control
    # Agrega aquí más combinaciones según lo necesites
]

# Leer el archivo llamado payload.txt en lugar de archivo_original.txt
with open('payload.txt', 'r') as archivo:
    contenido = archivo.read()


# Aplicar las variaciones
contenido_modificado = generar_variaciones_alert(contenido, combinaciones)

# Guardar el contenido modificado en un nuevo archivo
with open('archivo_modificado.txt', 'w') as archivo_modificado:
    archivo_modificado.write(contenido_modificado)
