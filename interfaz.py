import tkinter
import acciones

#funciones tkinter
def inicioSecion(host, user, password):
    "Documentar"
    variables = {"host":host, "user":user,"password":password}
    inicio = acciones.inicioSesion(variables)
    labelExitosamente.config(text = "")
    labelExitosamente.config(text = inicio[1])
    labelExitosamente.place(x=220, y=100)
    basesDatos()
    return inicio[0]

def basesDatos():
    """Documentar"""
    basesDatos = acciones.basesDatos()
    if(basesDatos == False):
        labelErrorConsulta.config(text = 'Error en la consulta')
        labelErrorConsulta.place(x=199, y=120)
    else:
        labelErrorConsulta.config(text = "")
        labelErrorConsulta.place(x=199, y=120)
        #LLenar la tabla de base de datos
        databaseFrame.delete(0,tkinter.END)
        labelBaseDatos = tkinter.Label(root, text = 'Seleccione una base de datos:')
        labelBaseDatos.place(x=199, y=120)
        for database in basesDatos:   
            databaseFrame.insert(databaseFrame.size() + 1, database)

def imprimirBatch(seleccion):
    """Documentar"""
    print(str(seleccion)[1:-2])
    batchhistoryFrame.delete(0,tkinter.END)
    datos = acciones.batchHistory(int(str(seleccion)[1:-2]))
    labelConsulta = tkinter.Label(root, text = '')
    batchhistoryFrame.delete(0,tkinter.END)
    labelConsulta.config(text = 'Seleccione un batch:')
    labelConsulta.place(x=220, y=240)
    header = ("                                    " + "Inicio de operación" + "            " + "fin de operación")
    batchhistoryFrame.insert(batchhistoryFrame.size() + 1, header)
    for indice in range(0,len(datos[1])):   
        data = ("                                    " + str(datos[0][indice]) + "            " + str(datos[1][indice]))
        batchhistoryFrame.insert(batchhistoryFrame.size() + 1, data)

def imprimirTrend(basedatos,trend):
    """"""
    print(str(basedatos)[1:-2])
    print(str(trend)[1:-2])
    datos = acciones.trend(int(str(basedatos)[1:-2]), int(str(trend)[1:-2])-1)
    trendFrame.delete(0,tkinter.END)
    header = ("                           Fecha           " + "                   " + "time_stamp_ms" + "            " + "Valores obtenidos")
    trendFrame.insert(trendFrame.size() + 1, header)
    for indice in range(0,len(datos[0])):   
        data = ("           " +  str(datos[0][indice]) +"            " + "                       " +  str(datos[1][indice]) + "            "+ "            " + "            " + str(datos[2][indice]))
        trendFrame.insert(trendFrame.size() + 1, data)
    
def excel(basedatos, trend):
    """"""
    datos = acciones.exportacion(int(str(basedatos)[1:-2]),int(str(trend)[1:-2])-1)
    print(datos)
#Inicializar tkinter
root = tkinter.Tk()
root.title('sqlDicap')
root.geometry("550x700")
root.resizable(False, False)

#variables de inicio de secion
variables = acciones.inicioSesion("")
vHost = tkinter.StringVar()
vUser = tkinter.StringVar()
vPassword = tkinter.StringVar()
vHost.set(variables["host"])
vUser.set(variables["user"])
vPassword.set(variables["password"])

#labels inico de secion
labelHost = tkinter.Label(root, text = "Host mysql")
labelHost.place(x=40, y=10)
entradaHost = tkinter.Entry(root, textvariable = vHost)
entradaHost.place(x=40, y=40)
labelUser = tkinter.Label(root, text = "Usuario mysql")
labelUser.place(x=225, y=10)
entradaUser = tkinter.Entry(root, textvariable = vUser)
entradaUser.place(x=225, y=40)
labelPassword = tkinter.Label(root, text = "Contraseña mysql")
labelPassword.place(x=400, y=10)
entradaPassword = tkinter.Entry(root, textvariable = vPassword)
entradaPassword.place(x=400, y=40)

#boton login
botonConector = tkinter.Button(root, text = "Conectarse a la base de datos", command = lambda: inicioSecion(entradaHost.get(), entradaUser.get(), entradaPassword.get()))
botonConector.place(x=200, y=65)
labelExitosamente = tkinter.Label(root, text = "")


#listbox de base de datos
fcons = tkinter.Frame(root)
databaseFrame = tkinter.Listbox(fcons, width = 25, height = 4, selectmode = tkinter.BROWSE, exportselection=False)
labelErrorConsulta = tkinter.Label(root, text = '')

#Render de la base de datos
fcons.place(x = 199, y = 140)
scrollbar = tkinter.Scrollbar(fcons, orient = tkinter.VERTICAL) 
#adjuntar el scrollbar a la base de datos   
databaseFrame.pack(side= tkinter.LEFT, fill=tkinter.Y)
scrollbar.config(command= databaseFrame.yview)
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
databaseFrame.config(yscrollcommand=scrollbar.set)

#Boton de seleccion de la base de datos
botonBaseDatos = tkinter.Button(root, text = "Elegir", command = lambda: imprimirBatch(databaseFrame.curselection()))
botonBaseDatos.place(x=255, y=210)

#listbox para el historial de batch
fcons2 = tkinter.Frame(root)
batchhistoryFrame = tkinter.Listbox(fcons2, width = 75, height = 7, selectmode = tkinter.BROWSE, exportselection=False)
 #para renderizar el batch
fcons2.place(x = 50, y = 260)
scrollbar2 = tkinter.Scrollbar(fcons2, orient = tkinter.VERTICAL) 
#adjuntar scrollbar al batch    
batchhistoryFrame.pack(side= tkinter.LEFT, fill=tkinter.Y)
scrollbar2.config(command= batchhistoryFrame.yview)
scrollbar2.pack(side=tkinter.RIGHT, fill=tkinter.Y)
batchhistoryFrame.config(yscrollcommand=scrollbar2.set)

#seleccion del batch
batchselection = tkinter.Button(root, text = "Elegir", command = lambda: imprimirTrend(databaseFrame.curselection(), batchhistoryFrame.curselection()))
batchselection.place(x=255, y=380)

#listbox para los trends
fcons3 = tkinter.Frame(root)
trendFrame = tkinter.Listbox(fcons3, width = 75, height = 7, selectmode = tkinter.BROWSE, exportselection=False)
 #para el render del trend
fcons3.place(x = 50, y = 440)
scrollbar3 = tkinter.Scrollbar(fcons3, orient = tkinter.VERTICAL) 
#adjuntar el scrollbar al trend    
trendFrame.pack(side= tkinter.LEFT, fill=tkinter.Y)
scrollbar3.config(command= trendFrame.yview)
scrollbar3.pack(side=tkinter.RIGHT, fill=tkinter.Y)
trendFrame.config(yscrollcommand=scrollbar3.set)

#boton para la exportacion de excel
exportExcel = tkinter.Button(root, text = "Exportar", command = lambda: excel(databaseFrame.curselection(), batchhistoryFrame.curselection()))
exportExcel.place(x=245, y=560)

root.mainloop()
