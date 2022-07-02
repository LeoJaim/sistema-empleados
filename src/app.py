from sqlite3 import Cursor
from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flaskext.mysql import MySQL
from datetime import datetime 
import os
from flask import send_from_directory,url_for

app = Flask(__name__)
mysql = MySQL()

app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'Minolta10*'
app.config['MYSQL_DATABASE_DB'] = 'empleados'
mysql.init_app(app)

FOLDER = os.path.join('uploads')
app.config['FOLDER']=FOLDER

@app.route('/uploads/<filname>')
def uploads(filname):
    return send_from_directory(app.config['FOLDER'], filname)

@app.route('/')
def index():
    conn=mysql.connect()
    cursor=conn.cursor()
    
    sql = "SELECT id,nombre,correo,foto FROM empleados"
    cursor.execute(sql)
    
    return render_template('empleados/index.html', empleados=cursor)

@app.route('/alta_emp')
def alta_emp():
    return render_template('empleados/create.html')

@app.route('/create', methods=['POST'])
def create():
    _nombre = request.form['nombre']
    _correo = request.form['correo']
    _foto = request.files['foto']
    now = datetime.now()
    tiempo = now.strftime("%Y-%m-%d %H:%M:%S")
    if _foto.filename != '':
        newNamePhoto = tiempo + _foto.filename
        _foto.save("uploads/" + newNamePhoto)
    else: newNamePhoto = 'default.png'
    
    conn=mysql.connect()
    cursor=conn.cursor()
    sql = "INSERT INTO empleados (id,nombre,correo,foto) VALUES (NULL,%s,%s,%s)"
    data = (_nombre,_correo,newNamePhoto)
    cursor.execute(sql, data)
    conn.commit()
    return redirect('/')    

@app.route('/edit/<int:id>')
def edit(id):
    conn=mysql.connect()
    cursor=conn.cursor()
    
    sql = "SELECT id,nombre,correo,foto FROM empleados WHERE id=%s"
    data = (id,)
    cursor.execute(sql, data)
    empleados = cursor.fetchall()
    return render_template('empleados/edit.html', empleados=empleados)

@app.route('/upd_emp', methods=['POST'])
def update():
    #Traigo los datos del formulario
    _nombre = request.form['nombre']
    _correo = request.form['email']
    _foto = request.files['foto']
    id = request.form['id']
    conn = mysql.connect()
    cursor = conn.cursor()
    #Actualizo todos los datos menos la foto
    sql = "UPDATE empleados SET nombre=%s,correo=%s WHERE id=%s"
    data = (_nombre,_correo,id)
    cursor.execute(sql, data)
    conn.commit()
    #Trato la foto específicamente
    now = datetime.now()
    tiempo = now.strftime("%Y-%m-%d %H:%M:%S")
    if _foto.filename != '':
        newNamePhoto = tiempo + _foto.filename
        _foto.save("uploads/" + newNamePhoto)
        cursor.execute("SELECT foto FROM empleados WHERE id=%s", id)
        row = cursor.fetchall()
        try: 
            os.remove(os.path.join(app.config['FOLDER'], row[0][0]))
        except:
            pass
        cursor.execute("UPDATE empleados SET foto=%s WHERE id=%s", (newNamePhoto, id))
        conn.commit()
    return redirect('/')

@app.route('/delete/<int:id>')
def delete(id):
    conn=mysql.connect()
    cursor=conn.cursor()
    sql = "DELETE FROM empleados WHERE id=%s"
    data = (id,)
    #Borro la foto
    cursor.execute("SELECT foto FROM empleados WHERE id=%s", id)
    row = cursor.fetchall()
    if row.count != 0:
        try: 
            os.remove(os.path.join(app.config['FOLDER'], row[0][0]))
        except:
            pass
    cursor.execute(sql, data)
    conn.commit()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
