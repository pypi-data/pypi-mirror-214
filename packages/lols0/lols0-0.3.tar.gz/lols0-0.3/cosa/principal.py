import sqlite3
import time
import agregar
import ver_datos
import buscar
import borrar
import actu
def add_one(number):
    return number + 1
class Ejemplo():
    def __init__(self):
        self.ejemplo = sqlite3.connect("notass.db")
        cursor = self.ejemplo.cursor()
        #Acá se supera el error de crear la tabla y generarel mensaje la tabla ya existe
        cursor.execute('''CREATE TABLE IF NOT EXISTS DATOS (ID INTEGER PRIMARY KEY AUTOINCREMENT,apellido TEXT , nombre TEXT, codigo TEXT, primer VARCHAR,  segundo VARCHAR, tercer VARCHAR, cuarto VARCHAR, asistencia VARCHAR, quiz VARCHAR ,fecha TEXT)''') 
        cursor.close()
        print('tabla de datos creada con éxito')

    def menu(self):
        try:
            self.a=int(input('''
            ingrese una de las opciones:
            1:Agregar un dato a la base de datos
            2:Ver los datos guardados
            3:Buscar datos de la base de datos
            4:Borrar datos de la base de datos
            5:actualizar
            6:salir\n'''))
            a=self.a
        except:
            print('el valor ingresado debe ser númerico')
        if a==1:
            self.agrega()
        elif a==2:
            self.ver()
        elif a==3:
            self.buscar()
        elif a==4:
            self.borrar()
        elif a==6:
            exit()
        elif a==5:
            self.actualizar()
        else:
            print('la opción no se encuentra en menu dado, intente de nuevo')
            print()
            print()
            self.menu()
    
    def agrega(self):
        print("hola")
        agregar.agrgar()
        #apellido= input("Apellido del estudiante: ")
        # nombre= input("Nombre del estudiante: ")
        # codigo= input("Código del estudiante: ")
        # primer= eval(input("ingrese la nota y multipliquela por el porcentaje correpondiente: "))
        # segundo= eval(input("ingrese la nota y multipliquela por el porcentaje correpondiente: "))
        # tercero= eval(input("ingrese la nota y multipliquela por el porcentaje correspondiente: "))
        # cuarto= eval(input("ingrese la nota y multipliquela por el porsentaje correspondiente: "))
        # asistencia = eval(input("ingrese la nota y multipliquela por el porsentaje correspondiente: "))
        # quiz = eval(input("ingrese la nota y multipliquela por el porsentaje correspondiente: "))
        # fecha= time.strftime("%d/%m/%y")
        self.menu()
    def ver(self):
        
        ver_datos.Ver()
        
        self.menu()
    def buscar(self):
        buscar.Bus()
        self.menu()

    def borrar(self):
        borrar.Borr()
        self.menu()
    
    def actualizar(self):
        actu.AC()
        self.menu()




z=Ejemplo()
z.menu()