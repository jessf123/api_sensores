from flask import Flask, jsonify, request
import psycopg2
from datetime import datetime
import os

# URL de conexión a PostgreSQL en Render
URL = "postgresql://jesse:NuIyzDWW4PVYHCF7HVRjPrKdMdzGbdi0@dpg-d0d4vq15pdvs73f7o7ag-a.oregon-postgres.render.com/pokemones_nqom"

app = Flask(__name__)

@app.route("/")
def introduccion():
    return "Esta es una API para mi estación meteorológica"

# Endpoint para recibir datos desde el ESP32
@app.route("/RecibirDatos", methods=["POST"])
def recibir_datos_sensores():
    data = request.get_json()
    fecha = datetime.now()
    
    # Lectura de valores recibidos (verifica que estos nombres coincidan con el JSON que envías desde MicroPython)
    gas = data.get("Gas")
    luz = data.get("Luz")
    lluvia = data.get("Lluvia")
    humedad_suelo = data.get("HumedadSuelo")
    temperatura = data.get("Temperatura")
    humedad_ambiente = data.get("HumedadAmbiente")
    
    # Guardar en base de datos
    conn = psycopg2.connect(URL)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO Sensores1(fecha, gas, luz, lluvia, humedad_suelo, temperatura, humedad_ambiente)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (fecha, gas, luz, lluvia, humedad_suelo, temperatura, humedad_ambiente))
    conn.commit()
    cursor.close()
    conn.close()
    return "Dato recibido correctamente", 201

# Endpoint para ver todos los datos registrados
@app.route("/verDatos")
def ver_datos():
    conn = psycopg2.connect(URL)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Sensores1 ORDER BY fecha DESC")
    datos = cursor.fetchall()
    conn.close()
    
    # Ajustar según el orden real de las columnas en la tabla Sensores1
    return jsonify([
        {
            "Id": x[0],
            "Fecha": x[1],
            "Gas": x[2],
            "Luz": x[3],
            "Lluvia": x[4],
            "HumedadSuelo": x[5],
            "Temperatura": x[6],
            "HumedadAmbiente": x[7],
        } for x in datos
    ])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
