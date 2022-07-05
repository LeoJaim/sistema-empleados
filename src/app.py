from flask import Flask
from flask import render_template,request,redirect,url_for
from flask import send_from_directory,flash
from flaskext.mysql import MySQL
from datetime import datetime 
import os


app = Flask(__name__)

app.secret_key = 'super secret key'

mysql = MySQL()

#Variables de entorno para la conexion a la base de datos
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'Minolta10*'
app.config['MYSQL_DATABASE_DB'] = 'empleados'
#Inicializo la conexion a la base de datos
mysql.init_app(app)

UPLOADS = os.path.join('src/uploads')
app.config['UPLOADS']=UPLOADS

@app.route('/fotousuario/<path:nombreFoto>', methods=['GET'],endpoint='uploads')
def uploads(nombreFoto):
    return send_from_directory(os.path.join('uploads'), nombreFoto) #os.path.join('uploads')
@app.route('/')
def index():
    conn=mysql.connect()
    cursor=conn.cursor()
    
    sql = "SELECT id,nombre,correo,foto FROM empleados where estado=1"
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
    _estado = True
    now = datetime.now()
    tiempo = now.strftime("%Y%H%M%S")
    if _foto.filename != '':
        newNamePhoto = tiempo + _foto.filename
        _foto.save("src/uploads/" + newNamePhoto)
    else: newNamePhoto = 'default.jpg'
    
    conn=mysql.connect()
    cursor=conn.cursor()
    sql = "INSERT INTO empleados (id,nombre,correo,foto,estado) VALUES (NULL,%s,%s,%s,%s)"
    data = (_nombre,_correo,newNamePhoto,_estado)
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
    _estado = request.form['estado']
    id = request.form['id']
    conn = mysql.connect()
    cursor = conn.cursor()
    #Actualizo todos los datos menos la foto
    sql = "UPDATE empleados SET nombre=%s,correo=%s,estado=%s WHERE id=%s"
    data = (_nombre,_correo,id,_estado)
    cursor.execute(sql, data)
    conn.commit()
    #Trato la foto específicamente
    
    if _foto.filename != '':
        now = datetime.now()
        tiempo = now.strftime("%Y%H%M%S")
        nuevoNombreFoto = tiempo + _foto.filename
        _foto.save("src/uploads/" + nuevoNombreFoto)
        cursor.execute("SELECT foto FROM empleados WHERE id=%s", id)
        row = cursor.fetchall()
        if row[0][0] != 'default.jpg':
            os.remove(os.path.join(app.config['UPLOADS'], row[0][0]))
        cursor.execute("UPDATE empleados SET foto=%s WHERE id=%s", (nuevoNombreFoto, id))
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
    if row[0][0] != "default.jpg":
        try: 
            os.remove(os.path.join(app.config['UPLOADS'], row[0][0]))
        except:
            flash('No se pudo borrar la foto o no tenía foto el empleado')
    else:
        flash('No tenía foto el empleado')
    cursor.execute(sql, data)
    conn.commit()
    return redirect('/')
@app.route('/inactive/<int:id>')
def inactive(id):
    conn=mysql.connect()
    cursor=conn.cursor()
    sql = "UPDATE empleados SET estado=0 WHERE id=%s"
    data = (id,)
    cursor.execute(sql, data)
    conn.commit()
    return redirect('/')


@app.route('/ina_emp')
def inactive_emp():
    conn=mysql.connect()
    cursor=conn.cursor()
    
    sql = "SELECT id,nombre,correo,foto FROM empleados where estado=0"
    cursor.execute(sql)
    
    return render_template('empleados/inactive.html', empleados=cursor)


@app.route('/active/<int:id>')
def active(id):
    conn=mysql.connect()
    cursor=conn.cursor()
    sql = "UPDATE empleados SET estado=1 WHERE id=%s"
    data = (id,)
    cursor.execute(sql, data)
    conn.commit()
    return redirect('/ina_emp')


if __name__ == '__main__':
    app.run(debug=True)
