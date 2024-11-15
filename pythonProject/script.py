import re
import json
import matplotlib.pyplot as plt
from collections import Counter
from datetime import datetime



def leer_logs(ruta_archivo):
    with open(ruta_archivo, 'r') as file:
        logs = file.readlines()
    return logs



def extraer_datos(logs):
    patron_ip = r'(\d{1,3}\.){3}\d{1,3}'
    patron_fecha = r'\d{2}/\w{3}/\d{4}(:\d{2}){3}'
    patron_metodo = r'GET|POST|PUT|DELETE'
    patron_recurso = r'"(GET|POST|PUT|DELETE) (.+?) HTTP\/\d\.\d"'
    patron_codigo = r'\s(\d{3})\s'

    datos_extraidos = []
    for linea in logs:
        ip = re.search(patron_ip, linea)
        fecha = re.search(patron_fecha, linea)
        metodo = re.search(patron_metodo, linea)
        recurso = re.search(patron_recurso, linea)
        codigo = re.search(patron_codigo, linea)

        if ip and fecha and metodo and recurso and codigo:
            registro = {
                "ip": ip.group(),
                "fecha": fecha.group(),
                "metodo": metodo.group(),
                "recurso": recurso.group(2),
                "codigo": codigo.group(1)
            }
            datos_extraidos.append(registro)

    return datos_extraidos



def guardar_json(datos, ruta_salida):
    with open(ruta_salida, 'w') as file:
        json.dump(datos, file, indent=4)



def visualizar_datos(datos):
    # Distribución de métodos de solicitud HTTP
    metodos = [entry['metodo'] for entry in datos]
    conteo_metodos = Counter(metodos)

    plt.figure(figsize=(10, 5))
    plt.bar(conteo_metodos.keys(), conteo_metodos.values())
    plt.title('Distribución de métodos de solicitud HTTP')
    plt.xlabel('Método')
    plt.ylabel('Frecuencia')
    plt.savefig("metodo_http.png")


    fechas = [entry['fecha'] for entry in datos if entry['codigo'].startswith('4') or entry['codigo'].startswith('5')]
    fechas_formato = [datetime.strptime(fecha[:11], "%d/%b/%Y") for fecha in fechas]
    conteo_fechas = Counter(fechas_formato)

    plt.figure(figsize=(10, 5))
    plt.bar(conteo_fechas.keys(), conteo_fechas.values())
    plt.title('Frecuencia de errores por día')
    plt.xlabel('Fecha')
    plt.ylabel('Errores')
    plt.xticks(rotation=45)
    plt.savefig("errores_por_dia.png")


    recursos = [entry['recurso'] for entry in datos]
    conteo_recursos = Counter(recursos).most_common(10)  # Top 10 recursos más accedidos

    recursos, frecuencias = zip(*conteo_recursos)
    plt.figure(figsize=(10, 5))
    plt.bar(recursos, frecuencias)
    plt.title('Top 10 recursos más accedidos')
    plt.xlabel('Recurso')
    plt.ylabel('Frecuencia')
    plt.xticks(rotation=45)
    plt.savefig("recursos_mas_accedidos.png")



if __name__ == "__main__":
    logs = leer_logs("logs.txt")  # Asegúrate de que el archivo logs.txt esté en el mismo directorio
    datos = extraer_datos(logs)
    guardar_json(datos, "data.json")
    visualizar_datos(datos)
