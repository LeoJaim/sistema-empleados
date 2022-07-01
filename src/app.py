from sqlite3 import Cursor
from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flaskext.mysql import MySQL


app = Flask(__name__)
mysql = MySQL()

app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'Minolta10*'
app.config['MYSQL_DATABASE_DB'] = 'empleados'
mysql.init_app(app)

@app.route('/')
def index():
    conn=mysql.connect()
    cursor=conn.cursor()
    
    sql = "SELECT nombre,correo,foto FROM empleados"
    cursor.execute(sql)
    
    return render_template('empleados/index.html', empleados=cursor)

@app.route('/alta_emp')
def alta_emp():
    return render_template('empleados/create.html')

@app.route('/create', methods=['POST'])
def create():
    _nombre = request.form['nombre']
    _correo = request.form['correo']
    _foto = request.form['foto']
    conn=mysql.connect()
    cursor=conn.cursor()
    sql = "INSERT INTO empleados (id,nombre,correo,foto) VALUES (NULL,%s,%s,%s)"
    cursor.execute(sql, (_nombre,_correo,_foto))
    conn.commit()
    return redirect('/')    



if __name__ == '__main__':
    app.run(debug=True)
