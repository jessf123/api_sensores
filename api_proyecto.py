from flask import Flask, jsonify, request, render_template
import psycopg2
from datetime import datetime
import os

URL = "postgresql://jesse:NuIyzDWW4PVYHCF7HVRjPrKdMdzGbdi0@dpg-d0d4vq15pdvs73f7o7ag-a.oregon-postgres.render.com/pokemones_nqom"

app = Flask(__name__)

@app.route("/")
def introduccion():
    return "Esta es una api de mi estacion meteorologica"

@app.route("/RecibirDatos", methods=["POST"])
def recibir_datos_sensores():
    try:
        data = request.get_json()

        fecha = datetime.now()
        gas = data.get("Gas")
        luz = data.get("Luz")
        lluvia = data.get("Lluvia")
        humedad_suelo = data.get("HumedadSuelo")
        temperatura = data.get("Temperatura")
        humedad_ambiente = data.get("HumedadAmbiente")

        conn = psycopg2.connect(URL)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO Sensores1(fecha, gas, luz, lluvia, humedad_suelo, temperatura, humedad_ambiente) VALUES (%s,%s,%s,%s,%s,%s,%s)",
            (fecha, gas, luz, lluvia, humedad_suelo, temperatura, humedad_ambiente)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return "Dato recibido"
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/verDatos")
def ver_datos():
    try:
        conn = psycopg2.connect(URL)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Sensores1 ORDER BY fecha DESC LIMIT 100")
        datos = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify([{
            "Id": x[0],
            "Fecha": x[1].strftime("%Y-%m-%d %H:%M:%S"),
            "Gas": x[2],
            "Luz": x[3],
            "Lluvia": x[4],
            "HumedadSuelo": float(x[5]),
            "Temperatura": x[6],
            "HumedadAmbiente": x[7]
        } for x in datos])
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route("/datosHtml")
def datos_html():
    try:
        conn = psycopg2.connect(URL)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Sensores1 ORDER BY fecha DESC LIMIT 100")
        filas = cursor.fetchall()
        cursor.close()
        conn.close()

        # Convertimos cada fila en un diccionario con texto interpretado
        datos = []
        for fila in filas:
            id_, fecha, gas, luz, lluvia, humedad_suelo, temp, hum = fila
            datos.append({
                "id": id_,
                "fecha": fecha.strftime("%Y-%m-%d %H:%M:%S"),
                "aire": "Contaminado" if gas > 2000 else "Aceptable",
                "luz": "Está oscuro" if luz < 1000 else "Está claro",
                "lluvia": "Está lloviendo" if lluvia < 2000 else "No hay lluvia",
                "humedad_suelo": round(humedad_suelo, 1),
                "temp": temp,
                "hum": hum
            })

        return render_template("tabla_datos.html", datos=datos)
    except Exception as e:
        return f"Error: {e}"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
