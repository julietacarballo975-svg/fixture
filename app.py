from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def conectar():
    conexion = sqlite3.connect('database.db')
    # Permite acceder a las columnas por su nombre (ej: partido['grupo'])
    conexion.row_factory = sqlite3.Row
    return conexion

def crear_tabla():
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS partidos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        grupo TEXT,
        local TEXT,
        visitante TEXT,
        gol_local INTEGER,
        gol_visitante INTEGER,
        estadio TEXT,
        ciudad TEXT,
        fecha TEXT,
        hora TEXT,
        bandera_local TEXT,
        bandera_visitante TEXT,
        imagen_estadio TEXT
    )
    ''')
    conexion.commit()

    # Cambiado para usar un alias ('total') y evitar problemas con row_factory
    cursor.execute("SELECT COUNT(*) AS total FROM partidos")
    fila = cursor.fetchone()
    cantidad = fila['total']

    if cantidad == 0:
        partidos = [
            ('A', 'Argentina', 'México', 0, 0, 'Estadio Azteca', 'Ciudad de México', '11/06/2026', '21:00', 'https://flagcdn.com/w320/ar.png', 'https://flagcdn.com/w320/mx.png', 'https://upload.wikimedia.org/wikipedia/commons/6/66/Estadio_Azteca.jpg'),
            ('B', 'Brasil', 'Francia', 0, 0, 'MetLife Stadium', 'New Jersey', '12/06/2026', '20:00', 'https://flagcdn.com/w320/br.png', 'https://flagcdn.com/w320/fr.png', 'https://upload.wikimedia.org/wikipedia/commons/9/92/MetLife_Stadium.jpg')
        ]
        cursor.executemany('''
            INSERT INTO partidos (grupo, local, visitante, gol_local, gol_visitante, estadio, ciudad, fecha, hora, bandera_local, bandera_visitante, imagen_estadio)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', partidos)
        conexion.commit()
    conexion.close()

# RUTA PRINCIPAL
@app.route('/')
def index():
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM partidos")
    partidos = cursor.fetchall()
    conexion.close()
    return render_template('index.html', partidos=partidos)

# RUTA PARA ACTUALIZAR GOLES
@app.route('/actualizar/<int:id>', methods=['POST'])
def actualizar(id):
    # Validamos que si el input llega vacío desde el HTML se guarde un 0 por defecto
    gol_local = request.form.get('gol_local', 0)
    gol_visitante = request.form.get('gol_visitante', 0)
    
    if gol_local == "": gol_local = 0
    if gol_visitante == "": gol_visitante = 0
    
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute('''
        UPDATE partidos 
        SET gol_local = ?, gol_visitante = ? 
        WHERE id = ?
    ''', (gol_local, gol_visitante, id))
    conexion.commit()
    conexion.close()
    return redirect('/')

if __name__ == "__main__":
    crear_tabla()  # Nos aseguramos de crear la tabla al arrancar
    app.run(debug=True)