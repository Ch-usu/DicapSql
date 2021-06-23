import lecturaEscritura
import accionesSql
from datetime import datetime


def inicioSesion(variables):
    """Documentar"""
    if(variables == ""):
        return lecturaEscritura.leerVariablesUsuario()
    else:
        nuevasVariables = lecturaEscritura.escribirVariablesUsuario(variables)
        coneccion = accionesSql.coneccionSql(nuevasVariables)
        if( "No es posible conectarse" in str(coneccion)):
            return [coneccion, "No es posible conectarse"]
        else:
            return [coneccion, "Coneccion exitosa"]

def basesDatos():
    """Escribir documentacion"""
    variables = lecturaEscritura.leerVariablesUsuario()
    coneccion = accionesSql.coneccionSql(variables)
    if("error" in str(coneccion)):
        return False
    else:
        bd = accionesSql.consultaBD(coneccion)
        return bd

def longitudes(seleccion):
    """Documentar"""
    variables = lecturaEscritura.leerVariablesUsuario()
    coneccion = accionesSql.coneccionSql(variables)
    bd = accionesSql.consultaBD(coneccion)
    tablas = accionesSql.consultaTablas(coneccion,bd[seleccion])
    dictLargos = {}
    for tabla in tablas:
        dictLargos[tabla] = len(accionesSql.consultaDatos(coneccion,bd[seleccion],tabla)[0])
    
    return dictLargos

def batchHistory(seleccion):
    """Escribir documentacion"""
    variables = lecturaEscritura.leerVariablesUsuario()
    coneccion = accionesSql.coneccionSql(variables)
    bd = accionesSql.consultaBD(coneccion)
    dictLargos = longitudes(seleccion)
    batch = max(dictLargos, key= dictLargos.get)
    datos = accionesSql.consultaDatos(coneccion,bd[seleccion],batch)
    inicio = []
    medio = ""
    fin = []
    stringInicio = ""
    stringFin = ""
    stringPalabraInicio = ""
    stringPalabraFin = ""
    listaInicioLimpio = []
    listaFinLimpio = []
    for indice in range(0, len(datos)):
        listInicio = datos[indice][datos[indice].find("datetime.datetime")+18:datos[1].find("datetime.datetime")+18+22].split()
        medio = datos[indice][datos[indice].find("datetime.datetime") + 18 + 22:]
        listFin = medio[medio.find("datetime.datetime")+18:medio.find("datetime.datetime")+18+22].split()
        listaInicioLimpio.clear()
        for palabra in listInicio:
            stringPalabraInicio = ""
            for letra in palabra:
                if letra.isnumeric():
                    stringPalabraInicio += letra
            listaInicioLimpio.append(stringPalabraInicio)
        for index in range(0, len(listaInicioLimpio)):
            numeroInicio = listaInicioLimpio[index]
            if len(listaInicioLimpio[index]) == 1:
                listaInicioLimpio[index] = '0' + numeroInicio
        stringInicio = '{}-{}-{} {}:{}:{}'.format(listaInicioLimpio[0],listaInicioLimpio[1],listaInicioLimpio[2],listaInicioLimpio[3],listaInicioLimpio[4], listaInicioLimpio[5])
        inicio.append(stringInicio)
        listaFinLimpio.clear()
        for palabra in listFin:
            stringPalabraFin = ""
            for letra in palabra:
                if letra.isnumeric():
                    stringPalabraFin += letra
            listaFinLimpio.append(stringPalabraFin)
        for index in range(0, len(listaFinLimpio)):
            numeroFin = listaFinLimpio[index]
            if len(listaFinLimpio[index]) == 1:
                listaFinLimpio[index] = '0' + numeroFin
        stringFin = '{}-{}-{} {}:{}:{}'.format(listaFinLimpio[0],listaFinLimpio[1],listaFinLimpio[2],listaFinLimpio[3],listaFinLimpio[4], listaFinLimpio[5])
        fin.append(stringFin)
    return [inicio,fin,bd[seleccion]]

def trend(seleccionBd,seleccionT):
    """Documentar"""
    datosBatch = batchHistory(seleccionBd)
    dictLargos = longitudes(seleccionBd)
    trend = min(dictLargos, key= dictLargos.get)
    variables = lecturaEscritura.leerVariablesUsuario()
    coneccion = accionesSql.coneccionSql(variables)
    consulta = trend +" WHERE Time_Stamp BETWEEN " + "\'" + datosBatch[0][seleccionT] + "\'" + " and " + "\'" + datosBatch[1][seleccionT] + "\'" + ";"
    datos = accionesSql.consultaDatos(coneccion, datosBatch[2], consulta)
    datosLimpios = []
    datoTrend = []
    for indice in range(0, len(datos)):
        stringLimpia = datos[indice][datos[indice].find("datetime.datetime")+18:datos[1].find("datetime.datetime")+18+22].split()
        for palabra in stringLimpia:
            stringDato = ""
            for letra in palabra:
                 if letra.isnumeric():
                     stringDato += letra
            datosLimpios.append(stringDato)
        for index in range(0, len(datosLimpios)):
            numeroFin = datosLimpios[index]
            if len(datosLimpios[index]) == 1:
                datosLimpios[index] = '0' + numeroFin
        stringDato = '{}-{}-{} {}:{}:{}'.format(datosLimpios[0],datosLimpios[1],datosLimpios[2],datosLimpios[3],datosLimpios[4], datosLimpios[5])
        datoTrend.append(stringDato)
    tiempoMs = [x[44:47] for x in datos]
    valor = [x[48:51] for x in datos]
    for indice in range(0, len(tiempoMs)): 
        iterate = ''
        for letra in tiempoMs[indice]:
            if letra.isnumeric():
                iterate += letra
        tiempoMs[indice] = iterate
        itera = ''
        for letra in valor[indice]:
            if letra.isnumeric():
                itera += letra
        valor[indice] = itera
    return [datoTrend, tiempoMs, valor]

def exportacion(seleccionBd, seleccionT):
    """Documentar"""
    batchInico = batchHistory(seleccionBd)[0][seleccionT]
    batchFin = batchHistory(seleccionBd)[1][seleccionT]
    baseDatos = batchHistory(seleccionBd)[2]
    dictLargos = longitudes(seleccionBd)
    trend = min(dictLargos, key= dictLargos.get)
    variables = lecturaEscritura.leerVariablesUsuario()
    coneccion = accionesSql.coneccionSql(variables)
    consulta = "SELECT * FROM " + trend +" WHERE Time_Stamp BETWEEN " + "\'" + batchInico + "\'" + " and " + "\'" + batchFin + "\'" 
    datos = accionesSql.lecturaSql(coneccion, baseDatos, consulta)
    filenumber = lecturaEscritura.excelEnnumeration(batchInico[0:10] + "_" + batchFin[0:10]) 
    datos['Time_Stamp'] = datos['Time_Stamp'].dt.strftime('%m-%d-%Y %H:%M:%S')
    datos.to_excel(batchInico[0:10] + "_" + batchFin[0:10] + "_" + str(filenumber) +".xlsx" , sheet_name = batchInico[0:10] + "_" + batchFin[0:10]+"_"+str(filenumber) + ".xlsx")
    return datos

