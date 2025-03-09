import requests
import numpy as np
from datetime import datetime

# Configuración
API_URL = "http://192.168.33.10:5000/consumo"

# Número total de minutos simulados (1440) y duración de la simulación (24 min en tiempo real)
TOTAL_MINUTOS = 1440  # 24 horas * 60 minutos
DURACION_SIMULACION_REAL = 24 * 60  # 24 minutos * 60 segundos = 1440 segundos

TIPO_CONTADOR = "CONT-012"
NUM_SERIE = "1234567890"
TITULAR = "Carlos Torá Giner"
LOCALIDAD = "Alicante"
MUNICIPIO = "Mutxamel"
CODIGO_POSTAL = "03110"
DIRECCION = "Calle Falsa 123"



# Definir parámetros de consumo
B = 0.05 

# Parámetros de los picos de consumo
A1, mu1, sigma1 = 3.0, 7.5, 0.5  # Matutino
A2, mu2, sigma2 = 2.4, 14.0, 0.7  # Mediodía
A3, mu3, sigma3 = 3.6, 21.0, 0.6  # Nocturno

# Función Gaussiana
def gaussian(t, A, mu, sigma):
    return A * np.exp(-((t - mu)**2) / (2 * sigma**2))

# Generar el vector de tiempo para el día simulado (1440 minutos)
t = np.linspace(0, 24, TOTAL_MINUTOS)

# Calcular consumo total
consumo_total = (
    B +
    gaussian(t, A1, mu1, sigma1) +
    gaussian(t, A2, mu2, sigma2) +
    gaussian(t, A3, mu3, sigma3)
)

now = datetime.now()
hora = now.minute
# Calculamos la hora simulada basándonos en el minuto actual
hora_simulada = hora % 24  # ⬅
minuto = hora_simulada * 60  # ⬅️ Convertimos la "hora simulada" a minutos base

# 🔹 Simular 60 minutos en 60 segundos
for i in range(60):
    minuto_actual = minuto + i 
    # concatenamos hora y minuto para obtener la hora simulada mas i con 2 digitos
    hora_simulada_str = str(hora).zfill(2) + ":" + str(i).zfill(2) + ":00"

    consumo_actual = consumo_total[minuto]
        # Enviar el consumo al servidor Flask
    data = {"HoraConsumo": hora_simulada_str, "Consumo": consumo_actual, "TipoContador": TIPO_CONTADOR, "NumSerie": NUM_SERIE, 
            "Titular": TITULAR, "Localidad": LOCALIDAD, "Municipio": MUNICIPIO, 
            "CodigoPostal": CODIGO_POSTAL, "Direccion": DIRECCION}

    try:
        response = requests.post(API_URL, json=data)
        print(f"Hora: {hora_simulada_str} ({minuto}/1440) - Consumo: {consumo_actual:.4f} - Respuesta: {response.status_code}")
    except Exception as e:
        print(f"Error enviando dato: {e}")