import sqlite3
import time
class Borr():
    def __init__(self):
        self.bor()

    def bor(self):
        self.ri=input("ingrese el codigo del estudiante a eliminar")
        ca=[]
        ca.append(self.ri)
        self.ejempl=sqlite3.connect("notass.db")
        cursor=self.ejempl.cursor()
        cursor.execute("DELETE FROM DATOS WHERE codigo=(?)",ca)
        datos=cursor.fetchall()
        self.ejempl.commit()
        cursor.close()
        time.sleep(2)
        print(datos)
        print("base de datos actualizada")
        