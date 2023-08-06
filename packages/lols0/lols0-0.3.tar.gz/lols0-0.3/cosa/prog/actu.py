import sqlite3
import time
class AC():
    def __init__(self):
        self.actuali()

    def actuali(self):
        alf = int(input('''¿Qué dato desea cambiar?
                    1. Nombre
                    2. Apellido
                    3. Código
                    4. Primer corte
                    5. Segundo corte
                    6. Tercer corte
                    7. Cuarto corte
                    8. Asistencia
                    9. Quiz\n'''))
    
        if alf in range(1, 10):
            nombre_actual = input("Ingrese el codigo del estudiante a actualizar: ")
            nuevo_dato = input("Ingrese el nuevo dato: ")

            self.ejemplo = sqlite3.connect("notass.db")
            cursor = self.ejemplo.cursor()

        if alf == 1:
            query = "UPDATE DATOS SET nombre = ? WHERE codigo = ?"
        elif alf == 2:
            query = "UPDATE DATOS SET apellido = ? WHERE codigo = ?"
        elif alf == 3:
            query = "UPDATE DATOS SET codigo = ? WHERE codigo = ?"
        elif alf == 4:
            query = "UPDATE DATOS SET primer = ? WHERE codigo = ?"
        elif alf == 5:
            query = "UPDATE DATOS SET segundo = ? WHERE codigo = ?"
        elif alf == 6:
            query = "UPDATE DATOS SET tercer = ? WHERE codigo = ?"
        elif alf == 7:
            query = "UPDATE DATOS SET cuarto = ? WHERE codigo = ?"
        elif alf == 8:
            query = "UPDATE DATOS SET asistencia = ? WHERE codigo = ?"
        elif alf == 9:
            query = "UPDATE DATOS SET quiz = ? WHERE codigo = ?"

        cursor.execute(query, (nuevo_dato, nombre_actual))
        self.ejemplo.commit()
        cursor.close()
        print("Dato actualizado correctamente.")