from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os

app = Flask(__name__)

# Ruta de la base de datos
DB_PATH = 'database.db'

# Crear la base de datos y la tabla si no existen
def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS registros (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            campo1 TEXT NOT NULL,
            campo2 TEXT NOT NULL,
            campo3 TEXT NOT NULL,
            cantidad REAL NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/', methods=['GET', 'POST'])
def index():
    buscar_cantidad = request.args.get('buscar_cantidad', None)

    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'create':
            campo1 = request.form['campo1']
            campo2 = request.form['campo2']
            campo3 = request.form['campo3']
            cantidad = float(request.form['cantidad'])
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO registros (campo1, campo2, campo3, cantidad)
                VALUES (?, ?, ?, ?)
            ''', (campo1, campo2, campo3, cantidad))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))
        elif action == 'delete':
            id = request.form['id']
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute('DELETE FROM registros WHERE id = ?', (id,))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))
        elif action == 'edit':
            id = request.form['id']
            campo1 = request.form['campo1']
            campo2 = request.form['campo2']
            campo3 = request.form['campo3']
            cantidad = float(request.form['cantidad'])
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE registros
                SET campo1 = ?, campo2 = ?, campo3 = ?, cantidad = ?
                WHERE id = ?
            ''', (campo1, campo2, campo3, cantidad, id))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    # Consultar registros (filtrados si hay búsqueda)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    if buscar_cantidad:
        try:
            cantidad_buscar = float(buscar_cantidad)
            cursor.execute('SELECT * FROM registros WHERE cantidad = ?', (cantidad_buscar,))
        except ValueError:
            cursor.execute('SELECT * FROM registros')
    else:
        cursor.execute('SELECT * FROM registros')
    registros = cursor.fetchall()
    conn.close()
    return render_template('index.html', registros=registros)

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)


