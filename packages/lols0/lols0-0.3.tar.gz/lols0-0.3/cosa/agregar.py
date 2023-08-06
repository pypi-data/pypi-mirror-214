import sqlite3
import time
class agrgar():
    def __init__(self):
        self.agrgar()

    def agrgar(self):
        self.ejempl = sqlite3.connect("notass.db")
        cursor = self.ejempl.cursor()
        apellido= input("Apellido del estudiante: ")
        nombre= input("Nombre del estudiante: ")
        codigo= input("Código del estudiante: ")
        primer= eval(input("ingrese la nota y multipliquela por el porcentaje correpondiente: "))
        segundo= eval(input("ingrese la nota y multipliquela por el porcentaje correpondiente: "))
        tercero= eval(input("ingrese la nota y multipliquela por el porcentaje correspondiente: "))
        cuarto= eval(input("ingrese la nota y multipliquela por el porsentaje correspondiente: "))
        asistencia = eval(input("ingrese la nota y multipliquela por el porsentaje correspondiente: "))
        quiz = eval(input("ingrese la nota y multipliquela por el porsentaje correspondiente: "))
        fecha= time.strftime("%d/%m/%y")
        lista=[(apellido, nombre,codigo,primer,segundo,tercero,cuarto,asistencia,quiz,fecha)]
        cursor.executemany("INSERT INTO DATOS  values (NULL,?,?,?,?,?,?,?,?,?,?)",lista)
        self.ejempl.commit()
        print ("Los datos fueron agregados con éxito")
        cursor.close()
        time.sleep(2)
        print()
       