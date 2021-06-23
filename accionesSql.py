import mysql.connector
import pandas.io.sql as sql


def coneccionSql(variables):
    """Asume variables como un diccionario que contiene {"host": "", "user":"", "password":""}
    y retorna en caso de exito la conneccion y caso contrario un string que indica el error"""
    try:
        coneccion = mysql.connector.connect(
            host = variables["host"],
            user = variables["user"],
            password = variables["password"])
        return coneccion
    except mysql.connector.Error as err :
        return 'No es posible conectarse',err
    
def consultaBD(coneccion):
    """Asume que la coneccion fue correctamente establecida, retorna en caso de correcta consulta
    una lista de strings de las bases de datos, caso contrario retorna el error que surgio"""
    consulta = coneccion.cursor()
    try:
        consulta.execute('SHOW DATABASES')
        baseDatos = consulta.fetchall()
        baseDatosLimpia = [str(x)[2:-3] for x in baseDatos]
        consulta.close()
        return baseDatosLimpia
    except mysql.connector.Error as err:
        return 'Error en la consulta SHOW DATABASES', err
    
def consultaTablas(coneccion, baseDatos):
    """Asume que la coneccion fue correctamente establecida y a base de datos como una string que 
    contiene el nombre de la base de datos escogida, retorna en caso de correcta consulta
    una lista de strings de las tablas existentes en la base de datos
    , caso contrario retorna el error que surgio"""
    consulta = coneccion.cursor()
    try:
        consulta.execute('USE ' + baseDatos)
        consulta.execute('SHOW TABLES')
        tablas = consulta.fetchall()
        tablasLimpias = [str(x)[2:-3] for x in tablas]
        consulta.close()
        return tablasLimpias
    except  mysql.connector.Error as err:
        return 'Error en la consulta', err

def consultaDatos(coneccion, baseDatos, tabla):
    """Asume que la coneccion fue correctamente establecida, a base de datos como una string que 
    contiene el nombre de la base de datos escogida, y tabla como una string que contiene 
    el nombre de las tabla escogida. Retorna en caso de correcta consulta
    una lista de strings de los datos de la tabla escogida,
    caso contrario retorna el error que surgio"""
    consulta = coneccion.cursor()
    try:
        consulta.execute('USE ' + baseDatos)
        consulta.execute('SELECT * FROM ' + tabla)
        datos = consulta.fetchall()
        datosLimpios = [str(x) for x in datos]
        consulta.close()
        return datosLimpios
    except mysql.connector.Error as err:
        return 'Error en la consulta', err

def lecturaSql(coneccion, baseDatos, consulta):
    """Documentar"""
    query = coneccion.cursor()
    try:
        query.execute('USE ' + baseDatos)
        datos = sql.read_sql(consulta,coneccion)
        return datos
    except mysql.connector.Error as err:
        return 'Error en la consulta', err