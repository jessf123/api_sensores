import psycopg2

URL = "postgresql://jesse:NuIyzDWW4PVYHCF7HVRjPrKdMdzGbdi0@dpg-d0d4vq15pdvs73f7o7ag-a.oregon-postgres.render.com/pokemones_nqom"

conn = psycopg2.connect(URL)
cursor = conn.cursor()

cursor.execute("DROP TABLE IF EXISTS Sensores1;")
cursor.execute("DROP TABLE IF EXISTS Actuadores;")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Sensores1 (
    id SERIAL PRIMARY KEY,
    fecha TIMESTAMP,
    gas INTEGER,
    luz INTEGER,
    lluvia INTEGER,
    humedad_suelo REAL,
    temperatura INTEGER,
    humedad_ambiente INTEGER
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Actuadores (
    id SERIAL PRIMARY KEY,
    Motor1 BOOLEAN
)
""")

cursor.execute("INSERT INTO Actuadores (Motor1) VALUES (FALSE);")

conn.commit()
cursor.close()
conn.close()

print(" Tablas creadas correctamente.")
