from flask import Flask, jsonify, request
import psycopg2
from datetime import datetime

URL="postgresql://jesse:NuIyzDWW4PVYHCF7HVRjPrKdMdzGbdi0@dpg-d0d4vq15pdvs73f7o7ag-a.oregon-postgres.render.com/pokemones_nqom"

app= Flask(__name__)

app.route("/")
def introduccion():
    return(
        "Esta es una api de mi estacion meteorologica"
    )

@app.route("/RecibirDatos", methods=["POST"])
def recibir_datos_sensores():
    data=request.get_json()
    #fecha = data.get("fecha")#La del ESP32
    fecha = datetime.now()#La de mi servidor
    temp1 = data.get("Temperatura1")                
    temp2 = data.get("Temperatura2")
    Hum1 = data.get("Humedad1")
    Hum2 = data.get("Humedad2")
    dist = data.get("Distancia")

    conn = psycopg2.connect(URL)
    cursor= conn.cursor()

    cursor.execute(
    "INSERT INTO Sensores1(fecha,Temperatura1, Temperatura2, Humedad1, Humedad2, Distancia) VALUES (%s,%s,%s,%s,%s,%s)", (fecha, temp1,temp2,Hum1,Hum2,dist))
    conn.commit()
    cursor.close()
    conn.close()
    return "Dato recibido"