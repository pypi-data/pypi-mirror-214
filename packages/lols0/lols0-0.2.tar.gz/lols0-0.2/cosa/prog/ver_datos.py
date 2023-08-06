import sqlite3
import time
class Ver():
    def __init__(self):
        self.ver_n()
    def ver_n(self):
        self.ejempl=sqlite3.connect("notass.db")
        cursor=self.ejempl.cursor()
        cursor.execute("SELECT * FROM DATOS")
        #fetchall este método devuelve los datos guardados en cursor.
        datos=cursor.fetchall()
        self.ejempl.commit()
        cursor.close()
        time.sleep(2)
        print(datos)