from flaskext.mysql import MySQL

#########################################################################################
#Funciones para la conexion a la base de datos
def crear_conexion(conexion=None,cursor=None,mysql=None):
    conexion = mysql.connect()
    cursor = conexion.cursor()
    return conexion, cursor

def cerrar_conexion(conexion, cursor):
    cursor.close()
    conexion.close()
    
    
def ejecutar_query(query, args=None):
    conexion, cursor = crear_conexion()
    cursor.execute(query, args)
    conexion.commit()
    cerrar_conexion(conexion, cursor)
#########################################################################################