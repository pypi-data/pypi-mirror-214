import sqlite3
import time
class Bus():
    def __init__(self):
        self.ejemplo = sqlite3.connect("notass.db")
        
        self.busq()

    def busq(self):
        try:
            self.a=int(input('''
            ingrese una de las opciones:
            1:buscar por nombre
            2:buscar por apellido
            3:buscar por codigo
            4:salir\n'''))
            a=self.a
        except:
            print('el valor ingresado debe ser númerico')
        if a==1:
            self.nom()
        elif a==2:
            self.app()
        elif a==3:
            self.cod()
        
        else:
            print('la opción no se encuentra en menu dado, intente de nuevo')
            print()
            print()
            
    
        
        
    def nom(self):   
        self.g=input("ingrese el nombre a buscar")
        vio=[]
        vio.append(self.g)
        self.ejempl=sqlite3.connect("notass.db")
        cursor=self.ejemplo.cursor()
    
        
        cursor.execute("SELECT * FROM DATOS WHERE nombre=(?)",vio)
        datos=cursor.fetchall()
        self.ejempl.commit()
        cursor.close()
        time.sleep(2)
        print(datos)

    def app(self):
        self.g=input("ingrese el apellido a buscar")
        vio=[]
        vio.append(self.g)
        self.ejempl=sqlite3.connect("notass.db")
        cursor=self.ejemplo.cursor()
    
        
        cursor.execute("SELECT * FROM DATOS WHERE apellido=(?)",vio)
        datos=cursor.fetchall()
        self.ejempl.commit()
        cursor.close()
        time.sleep(2)
        print(datos)
        #self.menu()
    
    def cod(self):
        self.g=input("ingrese el codigo a buscar")
        vio=[]
        vio.append(self.g)
        self.ejempl=sqlite3.connect("notass.db")
        cursor=self.ejemplo.cursor()
    
        cursor.execute("SELECT * FROM DATOS WHERE codigo=(?)",vio)
        datos=cursor.fetchall()
        self.ejempl.commit()
        cursor.close()
        time.sleep(2)
        print(datos)