import sa

admi={'david':12345}
class Almacen():
    def __init__(self):
        sa.crear()
        self.menu()
    def menu(self):
        print('Bienvenido a inventario de exito')
        print()
        self.a=int(input('1.Ingresar producto.\n2.Ver productos.\n3.Modificar producto.\n4.Borrar producto.\n'))
        if self.a==1:
            self.Ingreso()
        elif self.a==2:
            self.Ver()
        elif self.a==3:
            self.Modificar()
        elif self.a==4:
            self.Borrar()
        else:
            print('.|.')
            print('dijite un valor correcto')
            print()
            self.menu()
    def Ingreso(self):
        sa.ingreso()
        self.menu()
    def Ver(self):
        sa.ver()
        self.menu()
    def Modificar(self):
        sa.actualisar()
        self.menu()
    def Borrar(self):
        sa.borrar()
        self.menu()
a=input('usuario:')
b=int(input('contraseña:'))
for i in admi:
    if(a==i and b==admi[a]):
        print('correcto')
        a=Almacen()
