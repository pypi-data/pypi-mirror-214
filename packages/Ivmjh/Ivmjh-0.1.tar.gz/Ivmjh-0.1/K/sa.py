import sqlite3
def crear():
    ejemplo = sqlite3.connect("almacen.db")
    cursor = ejemplo.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS DATOS (ID INTEGER PRIMARY KEY AUTOINCREMENT,Producto TEXT , Cantidad TEXT, Precio TEXT)''') 
    cursor.close()
    print('tabla de datos creada con éxito')
def ingreso():
    ejemplo = sqlite3.connect("almacen.db")
    cursor = ejemplo.cursor()
    apellido= input("Nombre del producto: ")
    nombre= input("Cantidad: ")
    codigo= input("Precio unitario: ")
    
    lista=[(apellido, nombre,codigo)]
    cursor.executemany("INSERT INTO DATOS  values (NULL,?,?,?)",lista)
    ejemplo.commit()
    print ("Los datos fueron agregados con éxito")
    cursor.close()
def ver():
    ejemplo=sqlite3.connect("almacen.db")
    cursor=ejemplo.cursor()
    cursor.execute("SELECT * FROM DATOS")
    datos=cursor.fetchall()
    ejemplo.commit()
    cursor.close()
    print(datos)
def actualisar():
    ejemplo=sqlite3.connect("almacen.db")
    cursor=ejemplo.cursor()
    codigo=str(input('producto que se va a realisar la actualisacion:\n'))
    men=int(input('''1.cantidad.\n2.nombre.\n3.precio.'''))
    if men==1:
        apellido=str(input('cantidad a actualizar:\n'))
        cursor.execute('UPDATE DATOS SET Cantidad=? WHERE Producto=?',(apellido,codigo))
        ejemplo.commit()
        cursor.close()
        print('Datos actualizados con exito!')
        
    elif men==2:
        apellido=str(input('nombre a actualizar:\n'))
        cursor.execute('UPDATE DATOS SET Producto=? WHERE Producto=?',(apellido,codigo))
        ejemplo.commit()
        cursor.close()
        print('Datos actualizados con exito!')
        
    elif self.men==3:
        self.apellido=str(input('precio a actualizar:\n'))
        cursor.execute('UPDATE DATOS Precio =? WHERE Producto=?',(apellido,codigo))
        ejemplo.commit()
        cursor.close()
        print('Datos actualizados con exito!')
        
def borrar():
    ejemplo=sqlite3.connect("almacen.db")
    cursor=self.ejemplo.cursor()
    self.codigo=int(input('producto que desea borrar'))
    cursor.execute("DELETE FROM DATOS WHERE Producto=?",(self.codigo,))
    datos=cursor.fetchall()
    ejemplo.commit()
    cursor.close()
    print(datos)
    print("El dato seleccionado fue borrado con éxito de la tabla de datos")
